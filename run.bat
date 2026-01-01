@echo off
echo ====================================
echo  Minecraft 2D Mining Game - Python
echo ====================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.7+
    pause
    exit /b
)

echo.
echo Checking dependencies...
pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] pygame not found. Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting game...
python main.py

pause
