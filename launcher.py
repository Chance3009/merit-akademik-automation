#!/usr/bin/env python3
"""
Launcher script for Merit Akademik Automation System
This script launches the application and opens the browser automatically.
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path


def check_port_available(port=5000):
    """Check if the specified port is available."""
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return True


def find_application():
    """Find the application executable."""
    current_dir = Path(__file__).parent
    possible_paths = [
        current_dir / 'app_new.py',
        current_dir / 'MeritAkademikAutomation.exe',
        current_dir / 'dist' / 'MeritAkademikAutomation' / 'MeritAkademikAutomation.exe'
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def launch_application():
    """Launch the application."""
    app_path = find_application()

    if not app_path:
        print("❌ Application not found!")
        print("Please ensure the application is built correctly.")
        return False

    print(f"🚀 Starting application from: {app_path}")

    if app_path.suffix == '.py':
        # Running Python script directly
        process = subprocess.Popen([sys.executable, str(app_path)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
    else:
        # Running executable
        process = subprocess.Popen([str(app_path)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

    # Wait for the application to start
    print("⏳ Waiting for application to start...")
    for i in range(30):  # Wait up to 30 seconds
        if not check_port_available(5000):
            print("✅ Application started successfully!")
            return process
        time.sleep(1)
        print(f"   Waiting... ({i+1}/30)")

    print("❌ Application failed to start within 30 seconds")
    try:
        process.terminate()
    except:
        pass
    return None


def open_browser():
    """Open the browser with the application URL."""
    url = "http://localhost:5000"
    print(f"🌐 Opening browser at: {url}")

    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"Please manually open: {url}")
        return False


def main():
    """Main launcher function."""
    print("🏗️  Merit Akademik Automation System Launcher")
    print("=" * 50)

    # Check if port is already in use
    if not check_port_available(5000):
        print("⚠️  Port 5000 is already in use.")
        print("The application might already be running.")
        print("Please check your browser at: http://localhost:5000")

        answer = input(
            "Do you want to open the browser anyway? (y/n): ").lower()
        if answer == 'y':
            open_browser()
        return

    # Launch application
    process = launch_application()
    if not process:
        print("\n❌ Failed to start application")
        input("Press Enter to exit...")
        return

    # Open browser
    time.sleep(2)  # Give the app a moment to fully start
    open_browser()

    print("\n✅ Application is running!")
    print("📋 Instructions:")
    print("1. Use the web interface in your browser")
    print("2. When finished, close this window to stop the application")
    print("3. Or press Ctrl+C to stop the application")

    try:
        # Keep the application running
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping application...")
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            process.kill()
        print("✅ Application stopped")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
    finally:
        print("👋 Goodbye!")
