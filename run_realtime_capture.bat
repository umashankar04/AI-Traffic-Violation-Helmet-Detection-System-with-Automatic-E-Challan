@echo off
REM Real-Time Traffic Violation Capture System - Start Script

echo.
echo ========================================
echo  Real-Time Traffic Violation Detector
echo  with Automatic E-Challan Generation
echo ========================================
echo.

REM Get Python path
set PYTHON="C:\Users\UMASHANKAR\AppData\Local\Programs\Python\Python314\python.exe"

REM Check if Python exists
if not exist %PYTHON% (
    echo Error: Python 3.14 not found at %PYTHON%
    echo Please install Python 3.14 or update the path in this script
    pause
    exit /b 1
)

REM Change to project directory
cd /d "%~dp0"

echo Checking Python installation...
%PYTHON% --version

echo.
echo Installing/updating required packages...
%PYTHON% -m pip install --upgrade pip -q
%PYTHON% -m pip install -q fastapi uvicorn opencv-python ultralytics easyocr python-multipart psycopg2-binary pydantic-settings

echo.
echo ========================================
echo  Starting API Server
echo ========================================
echo.
echo API Server URL: http://127.0.0.1:8001
echo Web Interface: http://127.0.0.1:8001/webcam
echo API Docs: http://127.0.0.1:8001/api/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the API server
%PYTHON% -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001 --reload

pause
