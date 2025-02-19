cd /d "%~dp0"
if not exist "env\" (
    echo Creating virtual environment...
    python -m venv env
)
call env\Scripts\activate.bat
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
echo Starting application...
python app.py
pause
