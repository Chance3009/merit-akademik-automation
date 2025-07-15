"""
Entry point script for Merit Akademik Automation
"""
from app import app
from config import DEBUG

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
