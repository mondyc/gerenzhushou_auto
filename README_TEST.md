# 灵犀·晓伴自动化测试工具

## 功能概述

该测试工具用于"灵犀·晓伴"应用程序的自动化测试，支持以下测试类型：
- 安装/卸载测试
- 启动测试
- UI界面测试
- 基本功能测试

## 支持平台

- **Windows**: 使用pywinauto框架
- **Mac/Linux**: 使用PyAutoGUI框架（跨平台基础操作）

## 安装依赖

### 1. 安装Python依赖

```bash
pip install -r requirements_test.txt
```

或手动安装：

```bash
pip install pywinauto
pip install pyautogui
pip install pillow
```

### 2. Windows额外配置

pywinauto需要启用辅助功能：

```powershell
# 对于Windows 10/11，确保辅助功能已启用
```

## 目录结构

```
gerenzhushou_v2/
├── test_suxiaoban.py          # 主测试脚本
├── requirements_test.txt      # 依赖包列表
├── package/                   # 包含安装文件
│   └── suxiaoban-*-setup.exe.zip
├── test_logs/                 # 测试日志目录（自动创建）
└── README_TEST.md            # 本文档
```

## 使用方法

### 快速开始

```bash
python test_suxiaoban.py
```

### 测试流程

1. **查找安装文件**: 在package目录中查找 `suxiaoban-*-setup.exe.zip`
2. **安装测试**: 执行应用程序安装
3. **启动测试**: 启动已安装的应用程序
4. **UI测试**: 检查主窗口和界面元素
5. **功能测试**: 测试基本功能（菜单、快捷键等）
6. **卸载测试**: 卸载应用程序

### 测试结果

测试完成后，会生成：
- 测试日志: `test_logs/test_YYYYMMDD_HHMMSS.log`
- 测试截图: `test_logs/screenshot_YYYYMMDD_HHMMSS.png` (跨平台)
- 控制台输出测试结果摘要

## 配置说明

### 修改配置

可以在 `test_suxiaoban.py` 中修改 `TestConfig` 类的配置：

```python
class TestConfig:
    def __init__(self):
        self.timeout = 30           # 超时时间（秒）
        self.retry_count = 3        # 重试次数
        self.install_dir = Path.home() / "AppData" / "Local" / "Suxiaoban"  # 安装目录
```

### 自定义测试

可以继承 `TestRunner` 类创建自定义测试：

```python
class MyCustomTestRunner(WindowsTestRunner):
    def test_custom_feature(self):
        """自定义测试"""
        test_name = "自定义测试"
        try:
            # 测试逻辑
            self.log_test_result(test_name, True, "测试通过")
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {e}")
```

## 故障排查

### 问题1: pywinauto找不到窗口

解决: 检查应用程序是否正确启动，增加等待时间

```python
time.sleep(10)  # 增加等待时间
```

### 问题2: 权限错误

解决: 以管理员身份运行测试脚本

```bash
# 右键 -> 以管理员身份运行
```

### 问题3: 安装文件未找到

解决: 确保 `package` 目录中存在 `suxiaoban-*-setup.exe.zip` 文件

## 注意事项

1. 首次运行前请确保已安装所有依赖
2. Windows平台建议以管理员身份运行
3. 测试过程中请勿操作鼠标和键盘
4. 测试会自动关闭应用程序，建议保存好未保存的工作
5. 如需中断测试，按 `Ctrl+C`

## 扩展开发

### 添加新的测试用例

1. 在对应的Runner类中添加新方法
2. 使用 `self.log_test_result()` 记录测试结果
3. 在 `run_all_tests()` 中调用新方法

### 集成CI/CD

可以集成到GitHub Actions或其他CI/CD工具中：

```yaml
name: Automated Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements_test.txt
      - name: Run tests
        run: python test_suxiaoban.py
```

## 联系方式

如有问题或建议，请联系开发团队。
