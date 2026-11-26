@echo off
cd /d "%~dp0"

echo Installing FarmDoc dependencies...

python -m venv .venv

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip

python -m pip install -r requirements.txt

echo Installation finished. Check for errors above.
pause
