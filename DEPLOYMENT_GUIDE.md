# Merit Akademik Automation System - Deployment Guide

## Overview

This guide covers the deployment process for the Merit Akademik Automation System, a tool for automating entries in the UPM eKolej system.

## Prerequisites

- Windows 10/11 (64-bit)
- Python 3.8 or higher
- Internet connection (for initial setup)
- eKolej system access

## Deployment Steps

### 1. Build the Application

#### Automated Build (Recommended)
```powershell
# Open PowerShell as Administrator
cd path\to\merit-akademik
python build.py
```

#### Manual Build
```powershell
pip install -r requirements.txt
pyinstaller build_executable.spec
```

### 2. Distribution Package

After building, locate the package in `dist/MeritAkademikAutomation/`:

```
MeritAkademikAutomation/
├── MeritAkademikAutomation.exe
├── uploads/
├── screenshots/
├── chrome-bin/
└── [support files]
```

### 3. Installation

1. Copy the entire `MeritAkademikAutomation` folder to target computer
2. Ensure Chrome browser is installed
3. Double-click `MeritAkademikAutomation.exe`
4. Access via browser at `http://localhost:5000`

## Configuration

### Development
```python
# config.py
DEBUG = True
SELENIUM_HEADLESS = False
```

### Production
```python
# config.py
DEBUG = False
SELENIUM_HEADLESS = True
```

## Usage Guide

1. Launch application
2. Enter eKolej credentials
3. Upload Excel/CSV with matric numbers
4. Select processing options
5. Monitor automation progress
6. Review results

## Troubleshooting

### Port 5000 Conflict
- Close other applications using port 5000
- Restart the application

### Chrome Issues
- Verify Chrome installation
- Check chrome-bin folder integrity

### Login Problems
- Verify network connectivity
- Ensure eKolej system access
- Check credentials

### File Processing
- Use .xlsx or .csv format
- Verify file permissions
- Check file structure

## System Requirements

### Minimum
- Windows 10 (64-bit)
- 4GB RAM
- 100MB disk space
- Internet connection

### Recommended
- Windows 11 (64-bit)
- 8GB RAM
- 500MB disk space
- Stable network connection

## Support Resources

- Error screenshots: `screenshots/` folder
- Failed entries: `uploads/failed_matrics_*.csv`
- Application logs: Command line output

## Security Notes

- Application runs locally
- No external data transmission
- Secure credential handling
- Automatic file cleanup

## Contact

For technical support, contact system administrator with:
1. Error screenshots
2. Failed records
3. Detailed error message 