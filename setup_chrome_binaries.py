#!/usr/bin/env python3
"""
Setup script to download and configure Chrome binaries for Merit Akademik automation.
This creates a portable chrome-bin folder with Chrome and ChromeDriver.
"""

import os
import sys
import zipfile
import requests
import shutil
from pathlib import Path


def check_existing_chrome_binaries():
    """Check if Chrome binaries already exist and are valid."""
    chrome_bin_dir = Path("chrome-bin")

    if not chrome_bin_dir.exists():
        print("📁 chrome-bin folder does not exist")
        return False

    chrome_exe = chrome_bin_dir / "chrome.exe"
    chromedriver_exe = chrome_bin_dir / "chromedriver.exe"
    version_file = chrome_bin_dir / "version.txt"

    # Check if essential files exist
    if not chrome_exe.exists():
        print("❌ chrome.exe not found")
        return False

    if not chromedriver_exe.exists():
        print("❌ chromedriver.exe not found")
        return False

    # Check file sizes (should be reasonable)
    chrome_size = chrome_exe.stat().st_size
    driver_size = chromedriver_exe.stat().st_size

    if chrome_size < 1000000:  # Less than 1MB is suspicious
        print(f"❌ chrome.exe seems too small ({chrome_size:,} bytes)")
        return False

    if driver_size < 1000000:  # Less than 1MB is suspicious
        print(f"❌ chromedriver.exe seems too small ({driver_size:,} bytes)")
        return False

    # Check version file
    if version_file.exists():
        print("✅ Chrome binaries already exist and appear valid:")
        with open(version_file, 'r') as f:
            content = f.read()
            print(f"   {content.strip()}")
        print(f"   - chrome.exe: {chrome_size:,} bytes")
        print(f"   - chromedriver.exe: {driver_size:,} bytes")
        return True

    print("⚠️  Chrome binaries exist but no version info found")
    return False


def download_file(url, filename):
    """Download a file from URL."""
    print(f"📥 Downloading {filename}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(
                        f"   Progress: {percent:.1f}% ({downloaded:,}/{total_size:,} bytes)", end='\r')

        print(f"\n✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Error downloading {filename}: {e}")
        return False


def extract_zip(zip_path, extract_to):
    """Extract a zip file to a directory."""
    print(f"📦 Extracting {zip_path.name}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ Extracted to {extract_to}")


def setup_chrome_binaries(force_reinstall=False):
    """Download and setup Chrome binaries for bundling."""

    # Check if binaries already exist
    if not force_reinstall and check_existing_chrome_binaries():
        print("✅ Chrome binaries are already set up and valid!")
        print("💡 Use --force to re-download anyway")
        return True

    if force_reinstall:
        print("🔄 Force reinstall requested - removing existing binaries...")
        chrome_bin_dir = Path("chrome-bin")
        if chrome_bin_dir.exists():
            shutil.rmtree(chrome_bin_dir)

    # Create chrome-bin directory
    chrome_bin_dir = Path("chrome-bin")
    chrome_bin_dir.mkdir(exist_ok=True)
    print(f"📁 Created/verified chrome-bin directory")

    # Chrome version to use (stable version that works well)
    chrome_version = "119.0.6045.105"

    # Download URLs - using the full Chrome browser package
    chrome_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chrome-win64.zip"
    chromedriver_url = f"https://storage.googleapis.com/chrome-for-testing-public/{chrome_version}/win64/chromedriver-win64.zip"

    temp_dir = Path("temp_chrome_setup")
    temp_dir.mkdir(exist_ok=True)

    try:
        # Download Chrome
        chrome_zip = temp_dir / "chrome.zip"
        if not download_file(chrome_url, chrome_zip):
            print("❌ Failed to download Chrome. Trying alternative source...")
            # Alternative: download from different source
            chrome_url_alt = f"https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Win_x64%2F{chrome_version}%2Fchrome-win.zip?alt=media"
            if not download_file(chrome_url_alt, chrome_zip):
                raise Exception("Failed to download Chrome from all sources")

        # Download ChromeDriver
        driver_zip = temp_dir / "chromedriver.zip"
        if not download_file(chromedriver_url, driver_zip):
            raise Exception("Failed to download ChromeDriver")

        # Extract Chrome
        extract_zip(chrome_zip, temp_dir)
        chrome_extracted = temp_dir / "chrome-win64"

        # Extract ChromeDriver
        extract_zip(driver_zip, temp_dir)
        driver_extracted = temp_dir / "chromedriver-win64"

        # Copy Chrome binaries to chrome-bin directory
        print("📋 Copying Chrome files...")
        if chrome_extracted.exists():
            # Copy entire Chrome directory contents
            for item in chrome_extracted.iterdir():
                if item.is_file():
                    shutil.copy2(item, chrome_bin_dir)
                elif item.is_dir():
                    shutil.copytree(item, chrome_bin_dir /
                                    item.name, dirs_exist_ok=True)

        # Copy ChromeDriver
        print("📋 Copying ChromeDriver...")
        driver_exe_src = driver_extracted / "chromedriver.exe"
        driver_exe_dest = chrome_bin_dir / "chromedriver.exe"

        if driver_exe_src.exists():
            shutil.copy2(driver_exe_src, driver_exe_dest)
        else:
            raise Exception(
                "ChromeDriver executable not found in extracted files")

        # Verify files were copied correctly
        chrome_exe_final = chrome_bin_dir / "chrome.exe"
        driver_exe_final = chrome_bin_dir / "chromedriver.exe"

        if not chrome_exe_final.exists():
            raise Exception("Chrome executable not found after copying")
        if not driver_exe_final.exists():
            raise Exception("ChromeDriver executable not found after copying")

        # Check file sizes
        chrome_size = chrome_exe_final.stat().st_size
        driver_size = driver_exe_final.stat().st_size

        print(f"✅ Chrome binaries installed to {chrome_bin_dir}/")
        print(f"   - chrome.exe: {chrome_exe_final} ({chrome_size:,} bytes)")
        print(
            f"   - chromedriver.exe: {driver_exe_final} ({driver_size:,} bytes)")

        # Count total files
        total_files = len(list(chrome_bin_dir.rglob("*")))
        print(f"   - Total files: {total_files}")

        # Verify reasonable file sizes
        if chrome_size < 1000000:  # Less than 1MB is suspicious
            print("⚠️  WARNING: Chrome executable seems unusually small")
        if driver_size < 1000000:  # Less than 1MB is suspicious
            print("⚠️  WARNING: ChromeDriver executable seems unusually small")

        # Create version info file
        version_file = chrome_bin_dir / "version.txt"
        with open(version_file, 'w') as f:
            f.write(f"Chrome Version: {chrome_version}\n")
            f.write(f"ChromeDriver Version: {chrome_version}\n")
            f.write(
                "Downloaded from: https://googlechromelabs.github.io/chrome-for-testing/\n")
            f.write(f"Chrome size: {chrome_size:,} bytes\n")
            f.write(f"ChromeDriver size: {driver_size:,} bytes\n")
            f.write(f"Total files: {total_files}\n")

        print(f"✅ Version info saved to {version_file}")
        return True

    except Exception as e:
        print(f"❌ Error setting up Chrome binaries: {e}")
        return False

    finally:
        # Clean up temp directory
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        print("🧹 Cleaned up temporary files")


if __name__ == "__main__":
    force_reinstall = "--force" in sys.argv

    print("🔧 Setting up Chrome binaries for Merit Akademik automation...")

    success = setup_chrome_binaries(force_reinstall)

    if success:
        print("\n✅ Setup complete! Chrome binaries are ready.")
        print("📁 The chrome-bin folder contains:")
        print("   - chrome.exe (portable Chrome browser)")
        print("   - chromedriver.exe (WebDriver for automation)")
        print("   - Additional Chrome dependencies")
        print("   - version.txt (version information)")
        print("\n🚀 Next steps:")
        print("   1. Run: python app.py (to test)")
        print("   2. Run: python build.py (to build executable)")
        print("   3. Run: python create_distribution.py (to create distribution package)")
    else:
        print("\n❌ Setup failed! Check the error messages above.")
        sys.exit(1)
