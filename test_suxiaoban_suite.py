"""
灵犀·晓伴自动化测试示例脚本

本脚本展示如何编写具体的测试用例
"""

import os
import time
from test_suxiaoban import WindowsTestRunner, CrossPlatformTestRunner, TestConfig


class SuxiaobanTestSuite(WindowsTestRunner):
    """灵犀·晓伴测试套件"""
    
    def test_file_menu(self) -> bool:
        """测试文件菜单"""
        self.logger.info("测试文件菜单")
        test_name = "文件菜单测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("打开文件菜单...")
            main_window.type_keys("%F", set_foreground=False)
            time.sleep(1)
            
            self.log_test_result(test_name, True, "文件菜单测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_edit_menu(self) -> bool:
        """测试编辑菜单"""
        self.logger.info("测试编辑菜单")
        test_name = "编辑菜单测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("打开编辑菜单...")
            main_window.type_keys("%E", set_foreground=False)
            time.sleep(1)
            
            self.log_test_result(test_name, True, "编辑菜单测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_help_menu(self) -> bool:
        """测试帮助菜单"""
        self.logger.info("测试帮助菜单")
        test_name = "帮助菜单测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("打开帮助菜单...")
            main_window.type_keys("%H", set_foreground=False)
            time.sleep(1)
            
            self.log_test_result(test_name, True, "帮助菜单测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_shortcuts(self) -> bool:
        """测试快捷键功能"""
        self.logger.info("测试快捷键功能")
        test_name = "快捷键测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            shortcuts = [
                ("Ctrl+O", "打开文件"),
                ("Ctrl+S", "保存文件"),
                ("Ctrl+P", "打印"),
                ("Ctrl+Q", "退出")
            ]
            
            for shortcut, desc in shortcuts:
                self.logger.info(f"测试快捷键: {shortcut} ({desc})")
                main_window.type_keys(f"^{shortcut[-1]}", set_foreground=False)
                time.sleep(0.5)
            
            self.log_test_result(test_name, True, f"测试了 {len(shortcuts)} 个快捷键")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_window_controls(self) -> bool:
        """测试窗口控制功能"""
        self.logger.info("测试窗口控制功能")
        test_name = "窗口控制测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("测试最小化...")
            main_window.minimize()
            time.sleep(1)
            
            self.logger.info("测试恢复...")
            main_window.restore()
            time.sleep(1)
            
            self.logger.info("测试最大化...")
            main_window.maximize()
            time.sleep(1)
            
            self.logger.info("测试恢复...")
            main_window.restore()
            time.sleep(1)
            
            self.log_test_result(test_name, True, "窗口控制测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_resize_window(self) -> bool:
        """测试窗口大小调整"""
        self.logger.info("测试窗口大小调整")
        test_name = "窗口调整测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            self.logger.info("设置窗口大小为 800x600...")
            main_window.set_window_position(0, 0)
            main_window.set_window_size(800, 600)
            time.sleep(1)
            
            rect = main_window.rectangle()
            self.logger.info(f"当前窗口大小: {rect.width()}x{rect.height()}")
            
            self.log_test_result(test_name, True, "窗口调整测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_app_stability(self) -> bool:
        """测试应用稳定性（长时间运行）"""
        self.logger.info("测试应用稳定性")
        test_name = "稳定性测试"
        
        try:
            if not self.app:
                self.log_test_result(test_name, False, "应用程序未启动")
                return False
            
            main_window = self.app.window()
            
            test_duration = 10  # 测试时长（秒）
            self.logger.info(f"进行 {test_duration} 秒稳定性测试...")
            
            for i in range(test_duration):
                self.logger.info(f"稳定性测试进行中... {i+1}/{test_duration} 秒")
                time.sleep(1)
                
                if not main_window.exists():
                    raise Exception("应用程序意外关闭")
            
            self.log_test_result(test_name, True, f"稳定性测试通过 ({test_duration}秒)")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def run_custom_tests(self):
        """运行自定义测试套件"""
        self.logger.info("=" * 60)
        self.logger.info("开始自定义测试套件")
        self.logger.info("=" * 60)
        
        self.test_file_menu()
        self.test_edit_menu()
        self.test_help_menu()
        self.test_shortcuts()
        self.test_window_controls()
        self.test_resize_window()
        self.test_app_stability()
        
        self.print_summary()


class CrossPlatformTestSuite(CrossPlatformTestRunner):
    """跨平台测试套件"""
    
    def test_mouse_operations(self) -> bool:
        """测试鼠标操作"""
        self.logger.info("测试鼠标操作")
        test_name = "鼠标操作测试"
        
        try:
            screen_width, screen_height = self.pyautogui.size()
            self.logger.info(f"屏幕分辨率: {screen_width}x{screen_height}")
            
            center_x, center_y = screen_width // 2, screen_height // 2
            
            self.logger.info(f"移动鼠标到中心 ({center_x}, {center_y})")
            self.pyautogui.moveTo(center_x, center_y, duration=1)
            time.sleep(1)
            
            self.log_test_result(test_name, True, "鼠标操作测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def test_screenshot(self) -> bool:
        """测试截图功能"""
        self.logger.info("测试截图功能")
        test_name = "截图测试"
        
        try:
            screenshot_path = self.config.log_dir / f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
            self.pyautogui.screenshot(str(screenshot_path))
            self.logger.info(f"截图已保存: {screenshot_path}")
            
            self.log_test_result(test_name, True, "截图测试通过")
            return True
            
        except Exception as e:
            self.log_test_result(test_name, False, f"测试失败: {str(e)}")
            return False
    
    def run_custom_tests(self):
        """运行跨平台自定义测试套件"""
        self.logger.info("=" * 60)
        self.logger.info("开始跨平台自定义测试套件")
        self.logger.info("=" * 60)
        
        self.test_mouse_operations()
        self.test_screenshot()
        
        self.print_summary()


def main():
    """主函数"""
    config = TestConfig()
    
    print("=" * 60)
    print("灵犀·晓伴自动化测试工具 - 测试套件示例")
    print("=" * 60)
    print(f"当前平台: {config.platform}")
    print("=" * 60)
    
    if config.platform == "Windows":
        runner = SuxiaobanTestSuite(config)
        
        print("\n请选择测试模式:")
        print("1. 基础测试（安装、启动、UI、功能、卸载）")
        print("2. 自定义测试套件（菜单、快捷键、窗口控制等）")
        print("3. 完整测试（基础测试 + 自定义测试）")
        
        choice = input("\n请输入选择 (1/2/3): ").strip()
        
        if choice == "1":
            runner.run_all_tests()
        elif choice == "2":
            setup_file = runner.find_setup_file()
            if setup_file:
                runner.launch_application()
                runner.run_custom_tests()
                runner.uninstall_application()
            else:
                print("未找到安装文件，请先运行基础测试")
        elif choice == "3":
            runner.run_all_tests()
            runner.run_custom_tests()
        else:
            print("无效的选择")
    else:
        runner = CrossPlatformTestSuite(config)
        runner.run_custom_tests()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n测试被用户中断")
        import sys
        sys.exit(1)
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)
