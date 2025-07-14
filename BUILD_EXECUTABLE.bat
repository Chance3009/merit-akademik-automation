@echo off
echo ========================================
echo   Merit Akademik Automation Builder
echo ========================================
echo.

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo.
echo Creating distribution package...
python create_distribution.py
if errorlevel 1 (
    echo ERROR: Failed to create distribution package
    pause
    exit /b 1
)

echo.
echo ========================================
echo   DISTRIBUTION PACKAGE CREATED!
echo ========================================
echo.
echo Your distribution package is ready in:
echo   - MeritAkademikAutomation_Distribution/ (folder)
echo   - MeritAkademikAutomation_v*.zip (zip file)
echo.
echo 🎁 TO DISTRIBUTE TO FACULTY STAFF:
echo   1. Copy the entire folder or zip file to target computers
echo   2. Extract zip file if using zip distribution
echo   3. Double-click 'Start_Merit_Akademik.bat'
echo   4. Open browser to http://localhost:5000
echo.
echo ✅ FEATURES INCLUDED:
echo   - Bundled Chrome browser (no installation needed)
echo   - Real-time progress tracking
echo   - Error handling and failed matrics export
echo   - Professional user interface
echo   - Complete documentation
echo.
echo 📋 SYSTEM REQUIREMENTS:
echo   - Windows 10/11 (64-bit)
echo   - Internet connection for eKolej access
echo   - No additional software installation required
echo.
pause 