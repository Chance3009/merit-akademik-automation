"""
Utility functions for Merit Akademik Automation System
"""

import os
import pandas as pd
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str): Name of the file

    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def read_excel_file(filepath):
    """
    Read Excel or CSV file and return DataFrame.

    Args:
        filepath (str): Path to the file

    Returns:
        pandas.DataFrame: DataFrame containing the data

    Raises:
        Exception: If file cannot be read
    """
    try:
        if filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            raise Exception("Unsupported file format")

        return df
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")


def process_uploaded_file(file):
    """
    Process uploaded file and save it to the uploads folder.

    Args:
        file: Flask file object from request.files

    Returns:
        tuple: (filename, filepath) if successful

    Raises:
        Exception: If file processing fails
    """
    if not file or not allowed_file(file.filename):
        raise Exception(
            "Invalid file type. Please upload .xlsx or .csv files only.")

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(filepath)
        return filename, filepath
    except Exception as e:
        raise Exception(f"Error saving file: {str(e)}")


def get_file_columns(filepath):
    """
    Get column names from Excel or CSV file.

    Args:
        filepath (str): Path to the file

    Returns:
        list: List of column names
    """
    df = read_excel_file(filepath)
    return df.columns.tolist()


def get_matric_list(filepath, matric_column):
    """
    Get list of matric numbers from the specified column.

    Args:
        filepath (str): Path to the file
        matric_column (str): Name of the column containing matric numbers

    Returns:
        list: List of matric numbers as strings
    """
    df = read_excel_file(filepath)
    if matric_column not in df.columns:
        raise Exception(f"Column '{matric_column}' not found in file")

    matric_list = df[matric_column].astype(str).tolist()
    # Remove any empty or NaN values
    matric_list = [
        matric for matric in matric_list if matric and matric != 'nan']

    return matric_list


def validate_form_data(form_data):
    """
    Validate form data from the web interface.

    Args:
        form_data (dict): Form data from Flask request

    Returns:
        dict: Validated form data

    Raises:
        Exception: If validation fails
    """
    required_fields = ['filename', 'username', 'password',
                       'matric_column', 'sesi', 'semester', 'achievement']

    validated_data = {}
    for field in required_fields:
        value = form_data.get(field, '').strip()
        if not value:
            raise Exception(f"Field '{field}' is required")
        validated_data[field] = value

    return validated_data


def clean_screenshots_folder():
    """
    Clean up old screenshots to prevent folder from getting too large.
    Keeps only the most recent 10 screenshots.
    """
    try:
        from config import SCREENSHOTS_FOLDER

        if not os.path.exists(SCREENSHOTS_FOLDER):
            return

        # Get all screenshot files
        screenshot_files = []
        for filename in os.listdir(SCREENSHOTS_FOLDER):
            if filename.endswith('.png'):
                filepath = os.path.join(SCREENSHOTS_FOLDER, filename)
                screenshot_files.append((filepath, os.path.getmtime(filepath)))

        # Sort by modification time (newest first)
        screenshot_files.sort(key=lambda x: x[1], reverse=True)

        # Keep only the most recent 10 files
        for filepath, _ in screenshot_files[10:]:
            try:
                os.remove(filepath)
            except Exception:
                pass  # Ignore errors when deleting files

    except Exception:
        pass  # Ignore errors in cleanup


def format_success_message(success_count, error_count, failed_file=None):
    """
    Format success message for the web interface.

    Args:
        success_count (int): Number of successfully processed entries
        error_count (int): Number of failed entries
        failed_file (str): Path to failed entries file

    Returns:
        list: List of formatted messages
    """
    messages = []

    messages.append(
        f"Automation complete! Successful: {success_count}, Errors: {error_count}")

    if error_count > 0:
        messages.append(
            f"Please review the {error_count} failed entries listed below.")

        if failed_file:
            messages.append(
                f"Failed entries saved to: {os.path.basename(failed_file)}")

    return messages
