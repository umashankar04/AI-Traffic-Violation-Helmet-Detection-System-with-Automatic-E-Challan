@echo off
REM Quick Start Script - One-command system setup
REM Run: start.bat

echo ==================================================
echo 🚨 Traffic Violation Detection System - Setup
echo ==================================================
echo.

REM Check Python version
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 is required but not installed. Aborting.
    exit /b 1
)
python --version
echo ✓ Python found
echo.

REM Create virtual environment
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
echo    This may take a few minutes on first run...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

REM Setup environment
echo [5/6] Setting up environment...
if not exist ".env" (
    copy .env.example .env
    echo ⚠ .env file created. Please edit with your configuration.
) else (
    echo ✓ .env file exists
)
echo.

REM Download models
echo [6/6] Preparing model structure...
python scripts/download_datasets.py --prepare --download-models 2>nul || true
echo ✓ Models prepared
echo.

echo ==================================================
echo ✅ Setup Complete!
echo ==================================================
echo.
echo 📝 Next Steps:
echo.
echo 1️⃣  Start Backend API:
echo    python -m uvicorn backend.app.main:app --reload
echo.
echo 2️⃣  Start Dashboard (new terminal):
echo    streamlit run frontend/streamlit_app/app.py
echo.
echo 3️⃣  Test the system:
echo    curl http://localhost:8000/api/docs
echo.
echo 4️⃣  Or use Docker:
echo    docker-compose up -d
echo.
echo 📖 Documentation:
echo    - README.md - Project overview
echo    - docs\GETTING_STARTED.md - Detailed setup
echo    - docs\API.md - API reference
echo.
echo 💡 Pro Tips:
echo    • Download datasets: python scripts/download_datasets.py --guide
echo    • Train models: python scripts/train_helmet_model.py --help
echo    • Run tests: pytest tests\ -v
echo.
echo 🎯 Common Issues?
echo    See docs\GETTING_STARTED.md#troubleshooting
echo.
pause
