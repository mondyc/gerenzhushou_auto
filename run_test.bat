@echo off
chcp 65001 >nul
echo ========================================
echo 灵犀·晓伴自动化测试工具
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)
echo Python环境检查通过
echo.

echo [2/3] 检查并安装依赖...
if exist requirements_test.txt (
    pip install -r requirements_test.txt
) else (
    echo 警告: 未找到requirements_test.txt
    echo 请手动安装: pywinauto pyautogui pillow
)
echo.

echo [3/3] 启动测试...
echo.
python test_suxiaoban.py
echo.

echo ========================================
echo 测试完成
echo ========================================
pause
