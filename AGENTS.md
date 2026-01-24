# AI 代理编码指南 (Agentic Coding Guidelines)

本文档为在 `gerenzhushou_auto` 仓库中工作的 AI 代理提供指导。请遵循这些准则以确保代码库的一致性、可靠性和可维护性。

## 1. 环境与命令

### 环境设置
本项目依赖于 `requirements_test.txt` 中指定的 Python 包。
- **安装依赖：**
  ```bash
  pip install -r requirements_test.txt
  ```

### 运行测试
本项目使用基于 `pywinauto` 和 `pyautogui` 的自定义测试运行器，而非标准的 `pytest` 或 `unittest` 框架。

- **运行完整测试套件：**
  ```bash
  python test_suxiaoban_suite.py
  ```
  或者在 Windows 上：
  ```bash
  run_test.bat
  ```

- **运行主测试脚本：**
  ```bash
  python test_suxiaoban.py
  ```

- **运行示例：**
  ```bash
  python test_examples.py
  ```

- **运行单个测试：**
  由于使用的是自定义运行器类 (`SuxiaobanTestSuite`)，没有直接的 CLI 参数来运行单个测试方法。要运行特定的测试（例如 `test_file_menu`），你需要创建一个临时脚本或修改执行代码块：
  ```python
  # 运行单个测试的示例代码片段
  from test_suxiaoban import TestConfig
  from test_suxiaoban_suite import SuxiaobanTestSuite

  config = TestConfig()
  runner = SuxiaobanTestSuite(config)
  runner.start_application()
  runner.test_file_menu()  # 调用特定的测试方法
  runner.close_application()
  ```

### 代码检查与格式化
项目中没有特定的 linter 配置（如 `.flake8` 或 `pyproject.toml`）。但是，请严格遵守 Python 标准最佳实践：
- **风格：** 推荐遵循 PEP 8。
- **类型检查：** 必须使用 Python 类型提示（参见下方指南）。

---

## 2. 代码风格指南

### 语言与文档
- **语言：** 代码库主要使用 **中文** 编写注释、文档字符串 (docstrings) 和日志消息。请在所有描述性文本中保持这一约定。
- **文档字符串：** 类和函数使用三引号 (`"""`)。
  ```python
  def find_setup_file(self) -> Optional[str]:
      """查找安装文件"""
      # ...
  ```

### 导入规范 (Imports)
请按以下顺序分组导入：
1.  **标准库：** `os`, `sys`, `time`, `logging`, `platform`
2.  **类型提示：** `typing`, `pathlib`
3.  **第三方库：** `pywinauto`, `pyautogui`, `pillow`
4.  **本地应用：** `test_suxiaoban` (导入基类时)

示例：
```python
import os
import time
import logging
from typing import Optional

from pywinauto.application import Application

from test_suxiaoban import TestConfig
```

### 命名约定
- **类 (Classes)：** CamelCase (例如 `TestConfig`, `WindowsTestRunner`)。
- **函数/方法 (Functions/Methods)：** snake_case (例如 `log_test_result`, `install_application`)。
- **变量 (Variables)：** snake_case (例如 `setup_file`, `main_window`)。
- **常量 (Constants)：** UPPER_CASE (如果引入全局常量)。

### 类型提示 (Type Hinting)
大量使用 `typing` 模块以确保代码清晰。
- 对于可能为 `None` 的值，使用 `Optional[Type]`。
- 尽可能使用 `pathlib.Path` 代替字符串表示文件路径，尽管 `pywinauto` API 可能需要字符串（使用 `str(path)` 转换）。

示例：
```python
def install_application(self, setup_file: str) -> bool:
    # 实现代码
```

### 路径处理
- **始终** 使用 `pathlib.Path` 进行路径操作。
- 构造路径时应基于 `__file__` 的相对路径，以确保可移植性。
- **严禁** 硬编码绝对路径（如 `C:\Users\...`）。请使用 `Path.home()` 或相对路径。

示例：
```python
self.test_dir = Path(__file__).parent
self.log_dir = self.test_dir / "test_logs"
```

### 日志记录 (Logging)
- 不要使用 `print()`。请使用配置好的 `self.logger` 实例。
- 日志级别：普通步骤使用 `info`，失败使用 `error`。
- 格式通常为：`[PASS/FAIL] 测试名称: 消息`。

示例：
```python
self.logger.info("正在查找窗口...")
self.logger.error(f"未找到文件: {file_path}")
```

### 错误处理
- 在 UI 交互代码（`pywinauto`/`pyautogui` 调用）周围使用 `try...except` 块，以防止程序崩溃。
- 在测试方法中捕获通用的 `Exception`，记录失败并返回 `False`，而不是让测试套件崩溃。

示例：
```python
try:
    # UI 交互
    main_window.type_keys("%F")
    return True
except Exception as e:
    self.log_test_result(test_name, False, f"测试失败: {str(e)}")
    return False
```

### 项目结构感知
- **安装包目录：** 安装程序应位于 `package/`。
- **日志目录：** 日志写入 `test_logs/`。
- **核心类：**
    - `TestConfig`: 配置（路径，超时）。
    - `TestRunner`: 基类。
    - `WindowsTestRunner`: 使用 `pywinauto` 的具体实现。

## 3. Cursor / Copilot 规则
*未发现特定的 .cursorrules 或 .github/copilot-instructions.md。请严格遵循上述指南。*

## 4. AI 代理最佳实践
1.  **先读后写：** 修改文件前，务必先读取文件内容以了解上下文。
2.  **保持语言统一：** 如果现有注释是中文，请继续使用中文编写新注释。
3.  **安全操作：** 由于这是与操作系统交互（安装/卸载）的测试套件，使用删除命令时要格外小心。在调用 `rm` 或 `shutil.rmtree` 之前务必验证路径。
4.  **等待时间：** UI 自动化通常不稳定。请尊重现有的 `time.sleep()` 调用，或者更好的是使用 `pywinauto` 的 `wait()` 方法来提高稳定性。
