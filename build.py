#!/usr/bin/env python3
"""
Build script for Merit Akademik Automation System
Creates a PyInstaller executable with all dependencies
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd):
    """Run a command and return True if successful."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    directories = ['uploads', 'screenshots', 'dist', 'build']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"[+] Created directory: {directory}")


def install_requirements():
    """Install Python requirements."""
    cmd = f"{sys.executable} -m pip install -r requirements.txt"
    print(f"[+] {cmd}")
    return run_command(cmd)


def build_executable():
    """Build the executable using PyInstaller."""
    cmd = "pyinstaller build_executable.spec"
    print(f"[+] {cmd}")
    return run_command(cmd)


def cleanup():
    """Clean up build artifacts."""
    # Keep dist folder but clean build folder
    if Path('build').exists():
        shutil.rmtree('build')
        print("[+] Cleaned up build artifacts")


def main():
    """Main build process."""
    print("Building Merit Akademik Automation System")
    print("=" * 50)

    # Create directories
    create_directories()

    # Install requirements
    if not install_requirements():
        print("[-] Failed to install requirements")
        return False

    # Build executable
    if not build_executable():
        print("[-] Failed to build executable")
        return False

    # Cleanup
    cleanup()

    # Check if executable was created
    exe_path = Path("dist/MeritAkademikAutomation.exe")
    if exe_path.exists():
        exe_size = exe_path.stat().st_size
        print(f"[+] Executable created successfully: {exe_path}")
        print(f"[+] Size: {exe_size:,} bytes ({exe_size/1024/1024:.1f} MB)")

        # List contents of dist directory
        print("\n[+] Distribution contents:")
        for item in Path("dist").iterdir():
            if item.is_file():
                size = item.stat().st_size
                print(f"    {item.name}: {size:,} bytes")
            elif item.is_dir():
                file_count = len(list(item.rglob("*")))
                print(f"    {item.name}/: {file_count} files")

        return True
    else:
        print("[-] Executable not found after build")
        return False


if __name__ == "__main__":
    success = main()

    if success:
        print("\n" + "=" * 50)
        print("BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print(f"Executable location: dist/MeritAkademikAutomation.exe")
        print("\nTo test the executable:")
        print("1. Go to dist/ folder")
        print("2. Double-click MeritAkademikAutomation.exe")
        print("3. Open browser to http://localhost:5000")
        print("\nTo create distribution package:")
        print("python create_distribution.py")
    else:
        print("\n" + "=" * 50)
        print("BUILD FAILED!")
        print("=" * 50)
        print("Check the error messages above for details.")
        sys.exit(1)
