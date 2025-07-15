"""
Configuration settings for Merit Akademik automation system
"""
import os
import sys
from pathlib import Path

# Version information
APP_VERSION = "1.0.8"  # Updated: Changed login URL to upmid/login.php
APP_TITLE = f"Merit Akademik Automation System v{APP_VERSION}"

# Application settings
SECRET_KEY = 'merit-akademik-automation'
DEBUG = False  # Set to False for production

# Folder configurations - Dynamic path for executable


def get_base_path():
    """Get the base path for the application."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_PATH = get_base_path()
UPLOAD_FOLDER = os.path.join(BASE_PATH, 'data', 'uploads')
SCREENSHOTS_FOLDER = os.path.join(BASE_PATH, 'data', 'screenshots')
ALLOWED_EXTENSIONS = {'xlsx', 'csv'}

# eKolej system settings
LOGIN_URL = "https://ekolej.upm.edu.my/upmid/login.php"

# Selenium settings
SELENIUM_TIMEOUT = 10
SELENIUM_WAIT_TIME = 1
SELENIUM_HEADLESS = True  # Set to True for production

# Dynamic options generation


def generate_academic_years():
    """Generate academic years dynamically."""
    from datetime import datetime
    current_year = datetime.now().year

    # Generate 1 years back, current, and 1 years forward
    years = []
    for i in range(-1, 1):
        year = current_year + i
        academic_year = f"{year}/{year+1}"
        years.append((academic_year, academic_year))

    return years


def generate_semester_options():
    """Generate semester options dynamically."""
    from datetime import datetime
    current_year = datetime.now().year

    semesters = []
    for i in range(-1, 1):
        year = current_year + i
        academic_year = f"{year}/{year+1}"
        # Add both semesters for each academic year
        semesters.extend([
            (f"{academic_year}-1", f"{academic_year} - Semester 1"),
            (f"{academic_year}-2", f"{academic_year} - Semester 2"),
        ])

    return semesters


# Available options for the form
SESI_OPTIONS = generate_academic_years()
SEMESTER_OPTIONS = generate_semester_options()

ACHIEVEMENT_OPTIONS = [
    ('3', 'CGPA 3.75 - 4.00'),
    ('4', 'GPA Kepujian Dekan'),
    ('2', 'Pemegang Anugerah Akademik Peringkat Fakulti/Kolej'),
    ('1', 'Pemegang Anugerah Akademik Peringkat Universiti'),
]

# Create necessary directories


def create_directories():
    """Create required directories if they don't exist."""
    for folder in [UPLOAD_FOLDER, SCREENSHOTS_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)


# Initialize directories when config is imported
create_directories()
