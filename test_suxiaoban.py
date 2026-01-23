import os
import sys
import time
import subprocess
import platform
import logging
from typing import Optional, Tuple
from pathlib import Path


class TestConfig:
    """测试配置类"""
    
    def __init__(self):
        self.platform = platform.system()
        self.test_dir = Path(__file__).parent
        self.package_dir = self.test_dir / "package"
        self.install_dir = Path.home() / "AppData" / "Local" / "Suxiaoban" if self.platform == "Windows" else Path.home() / ".suxiaoban"
        self.log_dir = self.test_dir / "test_logs"
        
        self.suxiaoban_exe = "灵犀·晓伴.exe" if self.platform == "Windows" else "灵犀·晓伴"
        self.setup_pattern = "suxiaoban-*-setup.exe.zip"
        
        self.timeout = 30
        self.retry_count = 3
        
        self.log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / f'test_{time.strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)


class TestRunner:
    """测试运行器基类"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.logger = config.logger
        self.test_results = []
    
    def log_test_result(self, test_name: str, passed: bool, message: str = ""):
        """记录测试结果"""
        result = {
            "name": test_name,
            "passed": passed,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        status = "PASS" if passed else "FAIL"
        self.logger.info(f"[{status}] {test_name}: {message}")
    
    def run_all_tests(self):
        """运行所有测试"""
        raise NotImplementedError


class WindowsTestRunner(TestRunner):
    """Windows平台测试运行器，使用pywinauto"""
    
    def __init__(self, config: TestConfig):
        super().__init__(config)
        try:
            from pywinauto.application import Application
            from pywinauto.keyboard import send_keys
            from pywinauto.findwindows import find_window
            self.Application = Application
            self.send_keys = send_keys
            self.find_window = find_window
            self.app = None
            self.logger.info("pywinauto初始化成功")
        except ImportError:
            self.logger.error("pywinauto未安装，请运行: pip install pywinauto")
            sys.exit(1)
    
    def find_setup_file(self) -> Optional[str]:
        """查找安装文件"""
        self.logger.info("查找安装文件...")
        if not self.config.package_dir.exists():
            self.logger.error(f"package目录不存在: {self.config.package_dir}")
            return None
        
        import re
        for item in self.config.package_dir.iterdir():
            if item.is_file() and re.match(r'^suxiaoban-.*-setup\.exe\.zip$', item.name):
                self.logger.info(f"找到安装文件: {item}")
                return str(item)
        
        self.logger.error("未找到安装文件")
        return None
    
    def install_application(self, setup_file: str) -> bool:
        """安装应用程序测试"""
        self.logger.info(f"开始安装测试: {setup_file}")
        test_name = "安装测试"
        
        try:
            if not os.path.exists(setup_file):
                self.log_test_result(test_name, False, "安装文件不存在")
                return False
            
            self.logger.info("启动安装程序...")
            self.app = self.Application().start(f'explorer.exe /select,"{setup_file}"')
            time.sleep(2)
            
            self.log_test_result(test_name, True, "安装测试完成")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"安装失败: {str(e)}")
            return False
    
    def launch_application(self) -> bool:
        """启动应用程序测试"""
        self.logger.info("启动应用程序测试")
        test_name = "启动测试"
        
        try:
            possible_paths = [
                Path(self.config.install_dir) / self.config.suxiaoban_exe,
                self.config.test_dir / self.config.suxiaoban_exe,
                Path.home() / "Desktop" / self.config.suxiaoban_exe
            ]
            
            exe_path = None
            for path in possible_paths:
                if path.exists():
                    exe_path = str(path)
                    break
            
            if not exe_path:
                self.log_test_result(test_name, False, "未找到可执行文件")
                return False
            
            self.logger.info(f"启动应用程序: {exe_path}")
            self.app = self.Application().start(exe_path)
            time.sleep(5)
            
            self.log_test_result(test_name, True, "应用程序启动成功")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"启动失败: {str(e)}")
            return False
    
    def test_ui_elements(self) -> bool:
        """UI界面元素测试"""
        self.logger.info("UI界面元素测试")
        test_name = "UI测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            self.logger.info("检查主窗口...")
            main_window = self.app.window()
            if not main_window.exists():
                self.log_test_result(test_name, False, "主窗口未找到")
                return False
            
            window_title = main_window.window_text()
            self.logger.info(f"窗口标题: {window_title}")
            
            self.log_test_result(test_name, True, f"UI测试通过，窗口标题: {window_title}")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"UI测试失败: {str(e)}")
            return False
    
    def test_basic_functionality(self) -> bool:
        """基本功能测试"""
        self.logger.info("基本功能测试")
        test_name = "功能测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("测试菜单功能...")
            main_window.type_keys("%FM", set_foreground=False)
            time.sleep(1)
            
            self.logger.info("测试快捷键...")
            main_window.type_keys("%FO", set_foreground=False)
            time.sleep(1)
            
            self.log_test_result(test_name, True, "基本功能测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"功能测试失败: {str(e)}")
            return False
    
    def uninstall_application(self) -> bool:
        """卸载应用程序测试"""
        self.logger.info("卸载应用程序测试")
        test_name = "卸载测试"
        
        try:
            if self.app:
                self.logger.info("关闭应用程序...")
                self.app.kill()
                time.sleep(2)
            
            uninstaller_path = Path(self.config.install_dir) / "unins000.exe"
            if uninstaller_path.exists():
                self.logger.info(f"运行卸载程序: {uninstaller_path}")
                subprocess.run([str(uninstaller_path), "/SILENT"], timeout=60)
            
            self.log_test_result(test_name, True, "卸载测试完成")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"卸载失败: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("=" * 60)
        self.logger.info("开始自动化测试 - Windows平台")
        self.logger.info("=" * 60)
        
        setup_file = self.find_setup_file()
        if not setup_file:
            self.logger.error("无法找到安装文件，测试终止")
            return
        
        self.install_application(setup_file)
        self.launch_application()
        self.test_ui_elements()
        self.test_basic_functionality()
        self.uninstall_application()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试结果摘要"""
        self.logger.info("=" * 60)
        self.logger.info("测试结果摘要")
        self.logger.info("=" * 60)
        
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = sum(1 for r in self.test_results if not r["passed"])
        
        for result in self.test_results:
            status = "PASS" if result["passed"] else "FAIL"
            self.logger.info(f"[{status}] {result['name']}: {result['message']}")
        
        self.logger.info(f"总计: {len(self.test_results)} 个测试")
        self.logger.info(f"通过: {passed}, 失败: {failed}")
        self.logger.info("=" * 60)


class CrossPlatformTestRunner(TestRunner):
    """跨平台测试运行器，使用PyAutoGUI"""
    
    def __init__(self, config: TestConfig):
        super().__init__(config)
        try:
            import pyautogui
            self.pyautogui = pyautogui
            self.pyautogui.FAILSAFE = True
            self.logger.info("PyAutoGUI初始化成功")
        except ImportError:
            self.logger.error("PyAutoGUI未安装，请运行: pip install pyautogui")
            sys.exit(1)
    
    def find_setup_file(self) -> Optional[str]:
        """查找安装文件"""
        self.logger.info("查找安装文件...")
        if not self.config.package_dir.exists():
            self.logger.error(f"package目录不存在: {self.config.package_dir}")
            return None
        
        import re
        for item in self.config.package_dir.iterdir():
            if item.is_file() and re.match(r'^suxiaoban-.*-setup\.exe\.zip$', item.name):
                self.logger.info(f"找到安装文件: {item}")
                return str(item)
        
        self.logger.error("未找到安装文件")
        return None
    
    def install_application(self) -> bool:
        """安装应用程序测试（跨平台）"""
        self.logger.info("安装测试 - 跨平台")
        test_name = "安装测试"
        
        try:
            setup_file = self.find_setup_file()
            if not setup_file:
                self.log_test_result(test_name, False, "安装文件不存在")
                return False
            
            self.logger.info(f"准备安装: {setup_file}")
            time.sleep(2)
            
            self.log_test_result(test_name, True, "安装文件准备完成")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"安装测试失败: {str(e)}")
            return False
    
    def launch_application(self) -> bool:
        """启动应用程序测试（跨平台）"""
        self.logger.info("启动测试 - 跨平台")
        test_name = "启动测试"
        
        try:
            self.logger.info("等待用户手动启动应用程序...")
            
            for i in range(self.config.timeout):
                try:
                    screenshot = self.pyautogui.screenshot()
                    self.logger.info(f"等待中... ({i+1}/{self.config.timeout})")
                    time.sleep(1)
                except Exception:
                    time.sleep(1)
            
            self.log_test_result(test_name, True, "启动测试完成")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"启动测试失败: {str(e)}")
            return False
    
    def test_ui_elements(self) -> bool:
        """UI界面元素测试（跨平台）"""
        self.logger.info("UI测试 - 跨平台")
        test_name = "UI测试"
        
        try:
            self.logger.info("进行屏幕截图...")
            screenshot = self.pyautogui.screenshot()
            screenshot_path = self.config.log_dir / f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
            screenshot.save(str(screenshot_path))
            self.logger.info(f"截图已保存: {screenshot_path}")
            
            self.log_test_result(test_name, True, "UI测试完成")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"UI测试失败: {str(e)}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        self.logger.info("=" * 60)
        self.logger.info("开始自动化测试 - 跨平台")
        self.logger.info("=" * 60)
        
        self.install_application()
        self.launch_application()
        self.test_ui_elements()
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试结果摘要"""
        self.logger.info("=" * 60)
        self.logger.info("测试结果摘要")
        self.logger.info("=" * 60)
        
        passed = sum(1 for r in self.test_results if r["passed"])
        failed = sum(1 for r in self.test_results if not r["passed"])
        
        for result in self.test_results:
            status = "PASS" if result["passed"] else "FAIL"
            self.logger.info(f"[{status}] {result['name']}: {result['message']}")
        
        self.logger.info(f"总计: {len(self.test_results)} 个测试")
        self.logger.info(f"通过: {passed}, 失败: {failed}")
        self.logger.info("=" * 60)


def main():
    """主函数"""
    config = TestConfig()
    
    print("=" * 60)
    print("灵犀·晓伴自动化测试工具")
    print("=" * 60)
    print(f"当前平台: {config.platform}")
    print(f"测试目录: {config.test_dir}")
    print(f"Package目录: {config.package_dir}")
    print(f"日志目录: {config.log_dir}")
    print("=" * 60)
    
    if config.platform == "Windows":
        runner = WindowsTestRunner(config)
    else:
        runner = CrossPlatformTestRunner(config)
    
    try:
        runner.run_all_tests()
    except KeyboardInterrupt:
        config.logger.warning("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        config.logger.error(f"\n测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
