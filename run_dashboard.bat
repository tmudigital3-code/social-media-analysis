@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Professional Social Media Analytics Platform
echo  Enterprise Dashboard Launcher v2.0
echo ========================================
echo.

echo 🖥️  System Information:
echo ======================
systeminfo | findstr /C:"OS Name" /C:"OS Version" /C:"System Type"
echo Python Version:
python --version 2>nul || echo Python not found in PATH
echo.

REM Check if running in virtual environment
echo 🔍 Environment Check:
echo ==================
if defined VIRTUAL_ENV (
    echo ✅ Running in virtual environment: %VIRTUAL_ENV%
) else (
    echo ⚠️  Not running in virtual environment
    echo 💡 Recommendation: Use virtual environment for isolation
)
echo.

REM Kill any existing Streamlit processes
echo 🛑 Stopping existing Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo 🚀 Starting Professional Dashboard...
echo ========================================

REM Check if required files exist
echo 🔎 Validating Installation...
if not exist "professional_dashboard.py" (
    echo ❌ Error: professional_dashboard.py not found!
    echo 💡 Please ensure you're in the correct directory.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ⚠️  Warning: requirements.txt not found
) else (
    echo ✅ Requirements file located
)

echo.
echo 📊 Platform Information:
echo =====================
findstr /C:"Professional Social Media Analytics" README.md >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Platform: Professional Social Media Analytics v2.0
) else (
    echo ✅ Platform: Social Media Analytics Dashboard
)

echo.
echo 🌐 Access Information:
echo ===================
echo Local Access:    http://localhost:8510
echo Network Access:  http://[YOUR_IP]:8510
echo.
echo 💡 Pro Tips:
echo    - Data files go in the 'data' or 'uploads' folders
    - Reports will be generated in the 'reports' folder
    - Check README.md for detailed instructions

echo.
echo ⏳ Initializing Dashboard (this may take a moment)...
echo Press Ctrl+C to stop the dashboard
echo ========================================
echo.

REM Start the dashboard with enhanced configuration
streamlit run professional_dashboard.py --server.port 8510 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection true

:cleanup
echo.
echo 🧹 Cleaning up...
taskkill /F /IM streamlit.exe 2>nul

echo.
echo 👋 Dashboard session ended.
echo.
pause
