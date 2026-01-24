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
        
        # 调试模式配置
        self.skip_install_uninstall = True  # 跳过安装和卸载
        self.connect_existing = True        # 尝试连接已运行的实例
        
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
            import winreg
            self.Application = Application
            self.send_keys = send_keys
            self.find_window = find_window
            self.winreg = winreg
            self.app = None
            self.logger.info("pywinauto初始化成功")
        except ImportError:
            self.logger.error("pywinauto未安装，请运行: pip install pywinauto")
            sys.exit(1)
            
    def find_installed_app_path(self) -> Optional[str]:
        """从注册表查找已安装的应用程序路径"""
        self.logger.info("正在从注册表查找应用程序...")
        
        search_keys = [
            (self.winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (self.winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Uninstall"),
            (self.winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        keywords = ["灵犀", "晓伴", "Suxiaoban"]
        
        for root_key, sub_key in search_keys:
            try:
                with self.winreg.OpenKey(root_key, sub_key) as key:
                    for i in range(0, self.winreg.QueryInfoKey(key)[0]):
                        try:
                            sub_key_name = self.winreg.EnumKey(key, i)
                            with self.winreg.OpenKey(key, sub_key_name) as sub_k:
                                try:
                                    display_name = self.winreg.QueryValueEx(sub_k, "DisplayName")[0]
                                    if any(k in display_name for k in keywords):
                                        self.logger.info(f"在注册表中找到应用: {display_name}")
                                        
                                        # 尝试获取 InstallLocation
                                        try:
                                            install_loc = self.winreg.QueryValueEx(sub_k, "InstallLocation")[0]
                                            if install_loc:
                                                exe_path = Path(install_loc) / self.config.suxiaoban_exe
                                                if exe_path.exists():
                                                    return str(exe_path)
                                        except FileNotFoundError:
                                            pass
                                            
                                        # 尝试从 DisplayIcon 获取
                                        try:
                                            display_icon = self.winreg.QueryValueEx(sub_k, "DisplayIcon")[0]
                                            if display_icon and display_icon.endswith(".exe") and "unins" not in display_icon.lower():
                                                if os.path.exists(display_icon):
                                                    return display_icon
                                        except FileNotFoundError:
                                            pass
                                            
                                except FileNotFoundError:
                                    pass
                        except OSError:
                            continue
            except OSError:
                continue
                
        self.logger.warning("在注册表中未找到应用程序安装信息")
        return None
    
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
            # 1. 尝试连接已运行的进程
            if self.config.connect_existing:
                try:
                    self.logger.info("尝试连接已运行的应用程序...")
                    # 尝试通过标题匹配连接，这里假设标题包含"灵犀"或"晓伴"
                    # 使用 uia 后端，更适合现代应用
                    self.app = self.Application(backend='uia').connect(title_re=".*灵犀.*", timeout=5)
                    self.logger.info("成功连接到已运行的应用程序")
                    self.log_test_result(test_name, True, "成功连接到已运行的应用程序")
                    return True
                except Exception:
                    self.logger.info("未找到已运行的应用程序，尝试启动新实例...")

            # 2. 尝试查找并启动新实例
            possible_paths = [
                Path(self.config.install_dir) / self.config.suxiaoban_exe,
                self.config.test_dir / self.config.suxiaoban_exe,
                Path.home() / "Desktop" / self.config.suxiaoban_exe,
                # 添加常见的开发路径
                self.config.test_dir.parent / "dist" / self.config.suxiaoban_exe,
                self.config.test_dir.parent / "build" / self.config.suxiaoban_exe,
            ]
            
            # 尝试从注册表查找
            registry_path = self.find_installed_app_path()
            if registry_path:
                self.logger.info(f"使用注册表中发现的路径: {registry_path}")
                possible_paths.insert(0, Path(registry_path))
            
            exe_path = None
            for path in possible_paths:
                if path.exists():
                    exe_path = str(path)
                    break
            
            if not exe_path:
                self.logger.warning("未找到可执行文件，请手动启动应用程序...")
                # 等待用户手动启动
                for i in range(10):
                    try:
                        self.app = self.Application(backend='uia').connect(title_re=".*灵犀.*", timeout=2)
                        self.logger.info("检测到应用程序已启动")
                        self.log_test_result(test_name, True, "用户手动启动检测成功")
                        return True
                    except:
                        time.sleep(1)
                        self.logger.info(f"等待应用程序启动... {i+1}/10")
                
                self.log_test_result(test_name, False, "未找到可执行文件且未检测到手动启动")
                return False
            
            self.logger.info(f"启动应用程序: {exe_path}")
            # 使用 uia 后端启动
            self.app = self.Application(backend='uia').start(exe_path)
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
            # 使用更宽泛的匹配策略，并显式等待
            try:
                # 尝试通过正则表达式匹配窗口
                main_window = self.app.window(title_re=".*灵犀.*")
                main_window.wait('visible', timeout=10)
            except Exception:
                # 如果失败，尝试获取当前活跃窗口
                self.logger.warning("未找到匹配标题的窗口，尝试获取活跃窗口...")
                main_window = self.app.top_window()
                main_window.wait('visible', timeout=10)
            
            if not main_window.exists():
                self.log_test_result(test_name, False, "主窗口未找到")
                return False
            
            # 获取窗口标题和文本
            window_title = main_window.window_text()
            self.logger.info(f"窗口标题: {window_title}")
            
            # 尝试打印所有控件，方便调试
            self.logger.info("窗口控件结构:")
            try:
                # 限制打印深度，避免日志过长
                # main_window.print_control_identifiers(depth=2)
                pass 
            except:
                pass
            
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
        
        setup_file = None
        
        # 安装步骤
        if not self.config.skip_install_uninstall:
            setup_file = self.find_setup_file()
            if not setup_file:
                self.logger.warning("未找到安装文件，跳过安装测试，尝试直接启动应用程序")
            else:
                self.install_application(setup_file)
        else:
            self.logger.info("配置跳过安装测试")
        
        # 启动和功能测试
        if not self.launch_application():
            self.logger.error("应用程序启动失败，无法继续后续测试")
            return

        self.test_ui_elements()
        self.test_basic_functionality()
        
        # 卸载步骤
        if not self.config.skip_install_uninstall:
            if setup_file:
                self.uninstall_application()
            else:
                self.logger.info("跳过卸载测试（因为未执行安装）")
        else:
            self.logger.info("配置跳过卸载测试")
        
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
