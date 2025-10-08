@echo off
echo 🐍 Setting up Python environment...

cd /d "%~dp0\..\backend"
if not exist "%CD%" (
    echo Error: Backend directory not found at %CD%
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python dependencies...
pip install -r requirements-complete.txt

echo ✅ Python environment setup complete!