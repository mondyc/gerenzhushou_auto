"""
快速使用示例

本文件包含各种自动化测试的快速使用示例
"""

from test_suxiaoban import WindowsTestRunner, TestConfig
from test_suxiaoban_suite import SuxiaobanTestSuite
from test_report_generator import TestReportGenerator


def example_1_basic_test():
    """示例1: 基础测试"""
    print("\n=== 示例1: 基础测试 ===\n")
    
    config = TestConfig()
    runner = WindowsTestRunner(config)
    runner.run_all_tests()


def example_2_custom_test():
    """示例2: 自定义测试"""
    print("\n=== 示例2: 自定义测试 ===\n")
    
    config = TestConfig()
    runner = SuxiaobanTestSuite(config)
    runner.run_custom_tests()


def example_3_full_test_with_report():
    """示例3: 完整测试 + 生成报告"""
    print("\n=== 示例3: 完整测试 + 生成报告 ===\n")
    
    config = TestConfig()
    runner = SuxiaobanTestSuite(config)
    
    runner.run_all_tests()
    runner.run_custom_tests()
    
    report_gen = TestReportGenerator(config.log_dir)
    report_gen.generate_all_reports(runner.test_results)


def example_4_specific_test():
    """示例4: 运行特定测试"""
    print("\n=== 示例4: 运行特定测试 ===\n")
    
    config = TestConfig()
    runner = SuxiaobanTestSuite(config)
    
    setup_file = runner.find_setup_file()
    if setup_file:
        runner.install_application(setup_file)
        runner.launch_application()
        runner.test_ui_elements()
        runner.test_shortcuts()
        runner.uninstall_application()
        
        runner.print_summary()
    else:
        print("未找到安装文件")


def example_5_continuous_testing():
    """示例5: 连续测试（循环测试）"""
    print("\n=== 示例5: 连续测试 ===\n")
    
    config = TestConfig()
    
    test_count = 3
    print(f"将进行 {test_count} 次循环测试\n")
    
    all_results = []
    
    for i in range(test_count):
        print(f"\n=== 第 {i+1}/{test_count} 次测试 ===\n")
        
        runner = SuxiaobanTestSuite(config)
        runner.run_all_tests()
        all_results.extend(runner.test_results)
        
        if i < test_count - 1:
            print("\n等待5秒后继续...\n")
            import time
            time.sleep(5)
    
    print("\n=== 所有测试完成 ===\n")
    
    report_gen = TestReportGenerator(config.log_dir)
    report_gen.generate_all_reports(all_results)


def main():
    """主函数"""
    print("=" * 60)
    print("灵犀·晓伴自动化测试 - 快速使用示例")
    print("=" * 60)
    
    examples = [
        ("基础测试", example_1_basic_test),
        ("自定义测试", example_2_custom_test),
        ("完整测试 + 报告", example_3_full_test_with_report),
        ("特定测试", example_4_specific_test),
        ("连续测试", example_5_continuous_testing)
    ]
    
    print("\n请选择要运行的示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. 退出")
    
    try:
        choice = input("\n请输入选择: ").strip()
        
        if choice == "0":
            print("退出")
            return
        
        if choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("无效的选择")
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
