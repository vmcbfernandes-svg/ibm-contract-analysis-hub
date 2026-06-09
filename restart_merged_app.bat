@echo off
echo ========================================
echo Stopping all Streamlit processes...
echo ========================================

REM Kill all Python processes running Streamlit
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *streamlit*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Starting Merged Contract Analysis App
echo ========================================
echo.
echo The app will open in your browser at http://localhost:8501
echo.
echo You should see 6 pages in the sidebar:
echo   - Home
echo   - Upload ^& Analyze
echo   - Dashboard
echo   - Chat Assistant (NEW!)
echo   - Reports
echo   - Settings
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

cd /d "%~dp0"
python -m streamlit run contract_analysis_app.py

pause

@REM Made with Bob
