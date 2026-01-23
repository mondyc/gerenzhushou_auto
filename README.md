# 灵犀·晓伴自动化测试工具

## 项目简介

本项目用于"灵犀·晓伴"应用程序的自动化测试，支持Windows和跨平台测试。

## 项目结构

```
gerenzhushou_auto/
├── test_suxiaoban.py           # 主测试脚本
├── test_suxiaoban_suite.py     # 测试套件
├── test_examples.py           # 快速使用示例
├── test_report_generator.py    # 测试报告生成器
├── requirements_test.txt       # 依赖包列表
├── run_test.bat                # Windows快速启动脚本
├── README_TEST.md             # 详细使用说明
├── README.md                  # 本文件
└── test_logs/                 # 测试日志目录（自动生成）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements_test.txt
```

### 2. 运行测试

**方式一：使用批处理文件（Windows）**
```
双击 run_test.bat
```

**方式二：使用Python命令**
```bash
python test_suxiaoban.py
```

**方式三：运行测试套件**
```bash
python test_suxiaoban_suite.py
```

**方式四：查看示例**
```bash
python test_examples.py
```

## 功能特性

- ✅ 安装/卸载测试
- ✅ 启动测试
- ✅ UI界面测试
- ✅ 基本功能测试
- ✅ 菜单测试
- ✅ 快捷键测试
- ✅ 窗口控制测试
- ✅ 稳定性测试
- ✅ 自动生成测试报告（HTML/JSON）

## 依赖说明

- `pywinauto==0.6.8` - Windows GUI自动化
- `pyautogui==0.9.54` - 跨平台GUI自动化
- `pillow==10.1.0` - 图像处理

## 详细文档

请查看 `README_TEST.md` 获取详细使用说明和配置选项。

## 测试报告

测试完成后，会在 `test_logs/` 目录生成：
- 测试日志文件：`test_YYYYMMDD_HHMMSS.log`
- HTML测试报告：`test_report_YYYYMMDD_HHMMSS.html`
- JSON测试报告：`test_report_YYYYMMDD_HHMMSS.json`
- 截图文件：`screenshot_YYYYMMDD_HHMMSS.png`

## 注意事项

1. 首次运行前请确保已安装所有依赖
2. Windows平台建议以管理员身份运行
3. 测试过程中请勿操作鼠标和键盘
4. 如需中断测试，按 `Ctrl+C`

## 版本历史

- v1.0.0 (2025-01-23) - 初始版本

## 许可证

内部使用
