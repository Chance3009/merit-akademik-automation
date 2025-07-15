# Merit Akademik Automation System

## Overview

A web application that automates Merit Akademik entries in the UPM eKolej system. Built with Flask and Selenium for efficient batch processing.

## Project Structure

```
merit-akademik/
├── app.py                 # Flask application
├── automation.py          # Selenium automation  
├── config.py              # Configuration
├── utils.py               # Utilities
├── run.py                 # App entry point
├── build.py               # Build script
├── requirements.txt       # Dependencies
├── build_executable.spec  # PyInstaller config
├── data/                  # Data directories
│   ├── uploads/          # Excel/CSV files
│   └── screenshots/      # Error screenshots
├── dist/                  # Build output
├── chrome-bin/           # Bundled Chrome binaries
├── .gitignore            # Git ignore rules
└── README.md             # Documentation
```

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python run.py
```

## Production Build

```bash
python build.py
```

## Application Features

- Excel/CSV file processing for batch entries
- Real-time progress monitoring
- Error tracking and reporting
- Configurable academic sessions
- Headless browser automation
- Screenshot-based error logging

## Configuration

### Development Mode
```python
# config.py
DEBUG = True
SELENIUM_HEADLESS = False
```

### Production Mode
```python
# config.py
DEBUG = False
SELENIUM_HEADLESS = True
```

## System Requirements

### Development
- Python 3.8+
- Google Chrome
- Windows 10/11
- 4GB RAM minimum

### Production
- Windows 10/11 (64-bit)
- Google Chrome browser
- 4GB RAM minimum
- 100MB disk space

## File Management

- `data/uploads/`: Excel/CSV files and failed records
- `data/screenshots/`: Error debugging screenshots
- `dist/`: Production build output
- `chrome-bin/`: Bundled Chrome browser binaries

## Security Features

- Local-only processing
- No external data transmission
- User-provided credentials only
- Automatic file cleanup

## Common Issues

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