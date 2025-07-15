"""
Utility functions for Merit Akademik Automation System
"""

import os
import csv
import openpyxl
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER


class LightweightFileReader:
    """Lightweight file reader to replace pandas dependency."""

    @staticmethod
    def read_excel_file(filepath):
        """
        Read Excel file and return data as list of dictionaries.

        Args:
            filepath (str): Path to Excel file

        Returns:
            tuple: (column_names, rows_data)
        """
        try:
            workbook = openpyxl.load_workbook(filepath, read_only=True)
            sheet = workbook.active

            # Get all rows as list
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                return [], []

            # First row as column names
            columns = [
                str(col) if col is not None else f"Column_{i}" for i, col in enumerate(rows[0])]

            # Rest as data rows
            data_rows = []
            for row in rows[1:]:
                # Convert row to list and handle None values
                row_data = [
                    str(cell) if cell is not None else '' for cell in row]
                data_rows.append(row_data)

            workbook.close()
            return columns, data_rows

        except Exception as e:
            raise Exception(f"Error reading Excel file: {str(e)}")

    @staticmethod
    def read_csv_file(filepath):
        """
        Read CSV file and return data as list of dictionaries.

        Args:
            filepath (str): Path to CSV file

        Returns:
            tuple: (column_names, rows_data)
        """
        try:
            with open(filepath, 'r', encoding='utf-8', newline='') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter

                reader = csv.reader(file, delimiter=delimiter)
                rows = list(reader)

                if not rows:
                    return [], []

                # First row as column names
                columns = [str(col).strip() for col in rows[0]]

                # Rest as data rows
                data_rows = []
                for row in rows[1:]:
                    # Ensure each row has same number of columns as header
                    row_data = []
                    for i in range(len(columns)):
                        if i < len(row):
                            row_data.append(str(row[i]).strip())
                        else:
                            row_data.append('')
                    data_rows.append(row_data)

                return columns, data_rows

        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")

    @staticmethod
    def write_csv_file(filepath, columns, rows_data):
        """
        Write data to CSV file.

        Args:
            filepath (str): Path to output CSV file
            columns (list): Column names
            rows_data (list): List of row data
        """
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows_data)
        except Exception as e:
            raise Exception(f"Error writing CSV file: {str(e)}")


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str): Name of the file

    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    if filepath.endswith('.xlsx'):
        columns, _ = LightweightFileReader.read_excel_file(filepath)
    elif filepath.endswith('.csv'):
        columns, _ = LightweightFileReader.read_csv_file(filepath)
    else:
        raise Exception("Unsupported file format")

    return columns


def get_matric_list(filepath, matric_column):
    """
    Get list of matric numbers from the specified column.

    Args:
        filepath (str): Path to the file
        matric_column (str): Name of the column containing matric numbers

    Returns:
        list: List of matric numbers as strings
    """
    if filepath.endswith('.xlsx'):
        columns, rows_data = LightweightFileReader.read_excel_file(filepath)
    elif filepath.endswith('.csv'):
        columns, rows_data = LightweightFileReader.read_csv_file(filepath)
    else:
        raise Exception("Unsupported file format")

    if matric_column not in columns:
        raise Exception(f"Column '{matric_column}' not found in file")

    # Find the index of the matric column
    column_index = columns.index(matric_column)

    # Extract matric numbers from that column
    matric_list = []
    for row in rows_data:
        if column_index < len(row):
            cell_value = str(row[column_index]).strip()
            if cell_value and cell_value != 'nan' and cell_value != '':
                matric_list.append(cell_value)

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
