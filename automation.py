"""
Selenium automation module for Merit Akademik system
"""

import os
import sys
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from config import LOGIN_URL, SELENIUM_WAIT_TIME, SELENIUM_HEADLESS, SCREENSHOTS_FOLDER, UPLOAD_FOLDER


class MeritAkademikAutomation:
    """Main automation class for Merit Akademik system."""

    def __init__(self):
        """Initialize the automation with selenium webdriver."""
        self.driver = None
        self.progress_callback = None
        self.setup_driver()

    def setup_driver(self):
        """Setup Chrome webdriver with bundled Chrome binaries."""
        options = Options()

        # Get the base path (works for both script and executable)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Path to bundled Chrome binaries
        chrome_bin_path = os.path.join(base_path, "chrome-bin")
        chrome_exe = os.path.join(chrome_bin_path, "chrome.exe")
        chromedriver_exe = os.path.join(chrome_bin_path, "chromedriver.exe")

        # Verify Chrome binaries exist
        if not os.path.exists(chrome_exe):
            raise FileNotFoundError(
                f"Chrome executable not found at: {chrome_exe}")
        if not os.path.exists(chromedriver_exe):
            raise FileNotFoundError(
                f"ChromeDriver executable not found at: {chromedriver_exe}")

        print(f"Using Chrome binary: {chrome_exe}")
        print(f"Using ChromeDriver: {chromedriver_exe}")

        # Set Chrome binary location
        options.binary_location = chrome_exe

        # Configure Chrome options for better compatibility
        if SELENIUM_HEADLESS:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-plugins")
        options.add_argument("--disable-images")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

        # Additional Chrome options for stability and certificate handling
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-insecure-localhost")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Initialize Chrome driver
        service = Service(chromedriver_exe)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(SELENIUM_WAIT_TIME)

    def set_progress_callback(self, callback):
        """Set callback function for progress updates."""
        self.progress_callback = callback

    def update_progress(self, current, total, message):
        """Update progress through callback if available."""
        if self.progress_callback:
            self.progress_callback(current, total, message)

    def login(self, username, password):
        """
        Login to the eKolej system.

        Args:
            username (str): eKolej username
            password (str): eKolej password

        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self.driver.get(LOGIN_URL)

            # Wait for login form to be present
            wait = WebDriverWait(self.driver, 10)

            # Try different possible selectors for username field
            username_selectors = [
                (By.NAME, "user"),
                (By.ID, "user"),
                (By.NAME, "username"),
                (By.ID, "username"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]

            username_field = None
            for by, selector in username_selectors:
                try:
                    username_field = wait.until(
                        EC.presence_of_element_located((by, selector))
                    )
                    break
                except:
                    continue

            if not username_field:
                raise Exception("Could not find username field")

            # Try different possible selectors for password field
            password_selectors = [
                (By.NAME, "pass"),
                (By.ID, "pass"),
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]

            password_field = None
            for by, selector in password_selectors:
                try:
                    password_field = wait.until(
                        EC.presence_of_element_located((by, selector))
                    )
                    break
                except:
                    continue

            if not password_field:
                raise Exception("Could not find password field")

            # Clear and fill the fields
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)

            # Try different possible selectors for login button
            login_button_selectors = [
                (By.XPATH, "//input[@type='submit' and @value='Log Masuk']"),
                (By.XPATH, "//button[contains(text(), 'Log Masuk')]"),
                (By.XPATH, "//input[@type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.CSS_SELECTOR, "button[type='submit']")
            ]

            login_button = None
            for by, selector in login_button_selectors:
                try:
                    login_button = wait.until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    break
                except:
                    continue

            if not login_button:
                raise Exception("Could not find login button")

            # Click login button
            login_button.click()

            # Wait for login to complete and check result
            time.sleep(2)

            # Check if login was successful
            if "login" in self.driver.current_url.lower():
                self.driver.save_screenshot(os.path.join(
                    SCREENSHOTS_FOLDER, "login_failed.png"))
                return False

            return True

        except Exception as e:
            self.driver.save_screenshot(os.path.join(
                SCREENSHOTS_FOLDER, "login_error.png"))
            raise Exception(f"Login failed: {str(e)}")

    def navigate_to_merit_akademik(self):
        """Navigate to the Merit Akademik page."""
        try:
            # Find Merit menu
            merit_menu_selectors = [
                "//a[.//span[contains(text(), 'Merit')]]",
                "//a[.//i[contains(@class, 'ion-ribbon-b')]]",
                "//a[.//b[contains(@class, 'caret')] and .//span[contains(text(), 'Merit')]]"
            ]

            merit_menu = None
            for selector in merit_menu_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    for element in elements:
                        if "Merit" in element.text:
                            merit_menu = element
                            break
                    if merit_menu:
                        break
                except Exception:
                    continue

            if not merit_menu:
                self.driver.save_screenshot(os.path.join(
                    SCREENSHOTS_FOLDER, "menu_not_found.png"))
                raise Exception("Could not find Merit menu")

            # Click Merit menu
            self.driver.execute_script("arguments[0].click();", merit_menu)
            time.sleep(SELENIUM_WAIT_TIME)

            # Find and click Merit Akademik submenu
            merit_akademik_selectors = [
                "//ul[contains(@class, 'sub-menu')]//a[contains(text(), 'Merit Akademik')]",
                "//li//a[contains(text(), 'Merit Akademik')]"
            ]

            merit_akademik_link = None
            for selector in merit_akademik_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        merit_akademik_link = elements[0]
                        break
                except Exception:
                    continue

            if not merit_akademik_link:
                self.driver.save_screenshot(os.path.join(
                    SCREENSHOTS_FOLDER, "submenu_not_found.png"))
                raise Exception("Could not find Merit Akademik submenu")

            # Click Merit Akademik submenu
            self.driver.execute_script(
                "arguments[0].click();", merit_akademik_link)
            time.sleep(2)

            return True

        except Exception as e:
            self.driver.save_screenshot(os.path.join(
                SCREENSHOTS_FOLDER, "navigation_error.png"))
            raise Exception(f"Navigation failed: {str(e)}")

    def find_tambah_button(self):
        """Find the Tambah (Add) button on the page."""
        tambah_selectors = [
            "//button[contains(translate(text(), 'TAMBAH', 'tambah'), 'tambah')]",
            "//a[contains(translate(text(), 'TAMBAH', 'tambah'), 'tambah')]",
            "//input[contains(translate(@value, 'TAMBAH', 'tambah'), 'tambah')]",
            "//i[contains(@class, 'fa-plus')]/ancestor::button",
            "//button[@id='btnTambah']",
            "//button[contains(@class, 'btn-success')]"
        ]

        for selector in tambah_selectors:
            try:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    return elements[0]
            except Exception:
                continue

        # If still not found, check for plus icons
        try:
            plus_icons = self.driver.find_elements(
                By.XPATH, "//i[contains(@class, 'fa-plus')]")
            if plus_icons:
                return plus_icons[0].find_element(By.XPATH, "./..")
        except Exception:
            pass

        return None

    def process_single_matric(self, matric, sesi, semester, achievement):
        """
        Process a single matric number.

        Args:
            matric (str): Student matric number
            sesi (str): Academic session
            semester (str): Semester
            achievement (str): Achievement level

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Find and click Tambah button
            tambah_btn = self.find_tambah_button()
            if not tambah_btn:
                raise Exception("Could not find Tambah button")

            self.driver.execute_script("arguments[0].click();", tambah_btn)
            time.sleep(SELENIUM_WAIT_TIME)

            # Select matric number
            select_matric = Select(
                self.driver.find_element(By.ID, "a_matric_no"))
            select_matric.select_by_value(matric)
            time.sleep(SELENIUM_WAIT_TIME)

            # Select sesi
            select_sesi = Select(self.driver.find_element(By.ID, "a_session"))
            select_sesi.select_by_value(sesi)
            time.sleep(SELENIUM_WAIT_TIME)

            # Select semester
            select_sem = Select(self.driver.find_element(By.ID, "a_semester"))
            select_sem.select_by_value(semester)
            time.sleep(SELENIUM_WAIT_TIME)

            # Select achievement
            select_ach = Select(
                self.driver.find_element(By.ID, "a_achievement"))
            select_ach.select_by_value(achievement)
            time.sleep(SELENIUM_WAIT_TIME)

            # Save the record
            save_btn = self.driver.find_element(
                By.XPATH, "//a[contains(@class, 'btn') and contains(@class, 'btn-xs') and contains(@class, 'btn-primary')]"
            )
            self.driver.execute_script("arguments[0].click();", save_btn)
            time.sleep(2)  # Wait for save to complete

            return True

        except Exception as e:
            # Save screenshot for critical errors only
            self.driver.save_screenshot(os.path.join(
                SCREENSHOTS_FOLDER, f"matric_error_{matric}.png"))
            raise Exception(f"Failed to process matric {matric}: {str(e)}")

    def process_matric_list(self, matric_list, sesi, semester, achievement):
        """
        Process a list of matric numbers with progress reporting.

        Args:
            matric_list (list): List of matric numbers
            sesi (str): Academic session
            semester (str): Semester
            achievement (str): Achievement level

        Returns:
            dict: Results with success_count, error_count, and failed_matrics
        """
        success_count = 0
        error_count = 0
        failed_matrics = []
        total_count = len(matric_list)

        print(f"[INFO] Starting to process {total_count} matric numbers...")

        for index, matric in enumerate(matric_list, 1):
            try:
                # Report progress
                self.update_progress(index, total_count,
                                     f"Processing matric {matric}")
                print(f"[INFO] Processing {index}/{total_count}: {matric}")

                self.process_single_matric(matric, sesi, semester, achievement)
                success_count += 1
                print(f"[SUCCESS] Successfully processed {matric}")

            except Exception as e:
                error_count += 1
                failed_matrics.append(matric)
                print(f"[ERROR] Error processing matric {matric}: {str(e)}")

                # Continue with next matric even if one fails
                continue

        # Final progress report
        self.update_progress(
            total_count, total_count, f"Completed: {success_count} success, {error_count} errors")

        print(
            f"[INFO] Processing complete: {success_count} successful, {error_count} errors")

        return {
            'success_count': success_count,
            'error_count': error_count,
            'failed_matrics': failed_matrics
        }

    def save_failed_matrics(self, failed_matrics, sesi, semester, achievement):
        """Save failed matrics to a CSV file."""
        if not failed_matrics:
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        failed_df = pd.DataFrame({
            'matric_number': failed_matrics,
            'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")] * len(failed_matrics),
            'sesi': [sesi] * len(failed_matrics),
            'semester': [semester] * len(failed_matrics),
            'achievement': [achievement] * len(failed_matrics)
        })

        failed_file = os.path.join(
            UPLOAD_FOLDER, f"failed_matrics_{timestamp}.csv")
        failed_df.to_csv(failed_file, index=False)
        return failed_file

    def quit(self):
        """Close the webdriver."""
        if self.driver:
            self.driver.quit()

    def __del__(self):
        """Ensure webdriver is closed when object is destroyed."""
        self.quit()
 