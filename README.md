# Merit Akademik Automation System

## Overview

A web application that automates Merit Akademik entries in the UPM eKolej system. Built with Flask and Selenium for efficient batch processing.

## Project Structure

```
merit-akademik/
├── app.py                  # Main Flask application
├── automation.py           # Selenium automation logic
├── config.py              # Configuration settings
├── utils.py               # Utility functions
├── requirements.txt       # Dependencies
├── build.py              # Build script
├── BUILD_EXECUTABLE.bat   # Windows build script
├── launcher.py           # Application launcher
└── build_executable.spec  # PyInstaller configuration
```

## Development Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

## Production Build

### Option 1: Using Build Script (Recommended)
```bash
python build.py
```

### Option 2: Using Batch File (Windows)
```bash
BUILD_EXECUTABLE.bat
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

- `/uploads`: Excel/CSV files and failed records
- `/screenshots`: Error debugging screenshots
- `/dist`: Production build output

## Security Features

- Local-only processing
- No external data transmission
- User-provided credentials only
- Automatic file cleanup

## Common Issues

1. Port 5000 in use:
   - Close other applications
   - Check for running instances

2. Chrome driver issues:
   - Verify Chrome installation
   - Check chrome-bin folder

3. Login failures:
   - Verify network connection
   - Check eKolej accessibility

## Support

- Check `screenshots/` for error images
- Review `uploads/failed_matrics_*.csv` for failed entries
- See error messages in web interface

## License

Internal use only - UPM Faculty  