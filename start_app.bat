@echo off
echo ========================================================
echo Starting Mutual Fund FAQ Assistant (Investora)...
echo ========================================================
cd /d "%~dp0"

echo Starting FastAPI Backend server on port 8001...
start "Mutual Fund Assistant Backend" cmd /k ".venv\Scripts\python.exe -m src.main"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo Opening browser...
start http://127.0.0.1:8001/

echo.
echo Application running at: http://127.0.0.1:8001/
echo You can keep this window open or close it.
