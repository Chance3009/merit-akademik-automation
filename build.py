#!/usr/bin/env python3
"""
Build script for Merit Akademik Automation
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path


def install_requirements():
    """Install Python dependencies."""
    print("[INFO] Installing requirements...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install requirements")
        return False


def build_executable():
    """Build the executable using PyInstaller."""
    print("[INFO] Building executable...")
    try:
        # Clean up old build and dist directories
        for dir_name in ['build', 'dist']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)

        # Build using spec file
        subprocess.check_call(
            [sys.executable, "-m", "PyInstaller", "build_executable.spec"])

        exe_path = Path(
            "dist/MeritAkademikAutomation/MeritAkademikAutomation.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\n[SUCCESS] Executable created: {exe_path}")
            print(f"[INFO] Size: {size_mb:.1f} MB")
            print("\n[INFO] To run the application:")
            print("1. Navigate to: dist\\MeritAkademikAutomation")
            print("2. Double-click MeritAkademikAutomation.exe")
            print("3. Open browser to http://localhost:5000")
            return True
        else:
            print("[ERROR] Executable not found after build")
            return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Build failed: {e}")
        return False


def main():
    """Main build process."""
    print("Merit Akademik Automation Builder")
    print("=" * 50)

    # Install requirements
    if not install_requirements():
        return False

    # Build executable
    if not build_executable():
        return False

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
