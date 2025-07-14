"""
Flask web application for Merit Akademik automation system.
This application provides a web interface for processing matric numbers
through the eKolej Merit Akademik system.
"""
from config import (
    SECRET_KEY, DEBUG, UPLOAD_FOLDER, SCREENSHOTS_FOLDER,
    SESI_OPTIONS, SEMESTER_OPTIONS, ACHIEVEMENT_OPTIONS,
    APP_TITLE, APP_VERSION
)
from utils import (
    process_uploaded_file, get_file_columns, get_matric_list,
    validate_form_data, clean_screenshots_folder, format_success_message
)
from flask import Flask, render_template_string, request, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from automation import MeritAkademikAutomation
import os
import time
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = SECRET_KEY
app.config['DEBUG'] = DEBUG

# Clean up old screenshots on startup
clean_screenshots_folder()

# Global progress tracking
progress_data = {
    'current': 0,
    'total': 0,
    'message': '',
    'completed': False,
    'error': None
}


def reset_progress():
    """Reset progress tracking data."""
    global progress_data
    progress_data = {
        'current': 0,
        'total': 0,
        'message': '',
        'completed': False,
        'error': None
    }


def update_progress(current, total, message=""):
    """Update progress tracking data."""
    global progress_data
    progress_data['current'] = current
    progress_data['total'] = total
    progress_data['message'] = message
    if current >= total:
        progress_data['completed'] = True


"""
Merit Akademik Automation System

"""


# HTML Template with modern styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ app_title }}</title>
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f8f9fa;
            color: #212529;
            line-height: 1.5;
            font-size: 14px;
            overflow-x: hidden;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 24px;
            min-height: 100vh;
        }
        
        .header { 
            background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
            color: white;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,123,255,0.3);
        }
        
        .header h1 { 
            font-size: 24px; 
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 4px;
        }
        
        .header p { 
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
        }
        
        .main-content { 
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 16px;
            align-items: start;
        }
        
        .panel { 
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            height: fit-content;
        }
        
        .section { 
            margin-bottom: 24px;
        }
        
        .section:last-child { 
            margin-bottom: 0;
        }
        
        .section-title { 
            font-size: 16px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #e9ecef;
        }
        

        
        .form-group { 
            margin-bottom: 16px;
        }
        
        .form-group label { 
            display: block;
            margin-bottom: 6px;
            font-weight: 500;
            color: #495057;
            font-size: 13px;
        }
        
        .form-control { 
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 14px;
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            background: #ffffff;
        }
        
        .form-control:focus { 
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
        }
        
        .form-control::placeholder {
            color: #6c757d;
        }
        
        .btn { 
            display: inline-block;
            padding: 10px 20px;
            background: #007bff;
            color: #ffffff;
            border: none;
            border-radius: 4px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: background-color 0.15s ease-in-out;
            text-decoration: none;
            width: 100%;
            text-align: center;
        }
        
        .btn:hover { 
            background: #0056b3;
        }
        
        .btn:active { 
            background: #004085;
        }
        
        .btn:disabled { 
            background: #6c757d;
            cursor: not-allowed;
        }
        
        .file-upload { 
            position: relative;
            overflow: hidden;
            display: block;
            width: 100%;
        }
        
        .file-upload input[type=file] {
            position: absolute;
            left: -9999px;
        }
        
        .file-upload-label {
            display: block;
            padding: 32px 16px;
            background: #f8f9fa;
            border: 2px dashed #ced4da;
            border-radius: 4px;
            text-align: center;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            color: #6c757d;
            font-size: 14px;
        }
        
        .file-upload-label:hover {
            background: #e9ecef;
            border-color: #007bff;
            color: #495057;
        }
        
        .file-upload-label.has-file {
            background: #e7f3ff;
            border-color: #007bff;
            color: #0056b3;
        }
        
        .status-panel { 
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 16px;
            min-height: 200px;
            max-height: 400px;
            overflow-y: auto;
        }
        
        .message { 
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 4px;
            font-size: 13px;
            border-left: 4px solid #28a745;
            background: #d4edda;
            color: #155724;
        }
        
        .message.error { 
            border-left-color: #dc3545;
            background: #f8d7da;
            color: #721c24;
        }
        
        .progress-section {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .progress-title {
            font-weight: bold;
            color: #333;
        }
        
        .progress-text {
            color: #666;
            font-size: 14px;
        }
        
        .progress-bar-container {
            background: #e9ecef;
            border-radius: 4px;
            height: 20px;
            margin: 10px 0;
            overflow: hidden;
        }
        
        .progress-bar {
            background: linear-gradient(90deg, #28a745, #20c997);
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s ease;
            width: 0%;
        }
        
        .progress-message {
            color: #666;
            font-style: italic;
            margin: 10px 0;
        }
        
        .progress-spinner {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px 0;
        }
        
        .results-section {
            background: white;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .results-summary {
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .results-details {
            color: #666;
            font-size: 14px;
        }
        
        .message.warning { 
            border-left-color: #ffc107;
            background: #fff3cd;
            color: #856404;
        }
        
        .message.info { 
            border-left-color: #17a2b8;
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .failed-list { 
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            padding: 16px;
            margin-top: 16px;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .failed-list-title {
            font-weight: 600;
            color: #dc3545;
            margin-bottom: 8px;
            font-size: 13px;
        }
        
        .failed-list ul { 
            list-style: none;
            padding: 0;
        }
        
        .failed-list li { 
            padding: 4px 0;
            border-bottom: 1px solid #f8f9fa;
            font-size: 13px;
            color: #495057;
        }
        
        .failed-list li:last-child { 
            border-bottom: none;
        }
        
        .loading { 
            display: none;
            text-align: center;
            padding: 32px;
        }
        
        .loading.show { 
            display: block;
        }
        
        .spinner { 
            border: 3px solid #f8f9fa;
            border-top: 3px solid #007bff;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            animation: spin 1s linear infinite;
            margin: 0 auto 12px;
        }
        
        @keyframes spin { 
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .instructions { 
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 12px 16px;
            margin-top: 16px;
            border-radius: 4px;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .instructions-title {
            font-weight: 600;
            margin-bottom: 6px;
            color: #ffffff;
        }
        
        .instructions ul { 
            margin-left: 16px;
            margin-top: 6px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .instructions li { 
            margin-bottom: 2px;
            margin-right: 12px;
            position: relative;
        }
        
        .instructions li:after {
            content: "•";
            margin-left: 8px;
            opacity: 0.5;
        }
        
        .instructions li:last-child:after {
            display: none;
        }
        

        
        @media (max-width: 1024px) {
            .main-content { 
                grid-template-columns: 1fr;
                gap: 16px;
            }
            
            .container { 
                padding: 16px;
            }
        }
        
        @media (max-width: 768px) {
            .container { 
                padding: 12px;
            }
            
            .header {
                padding: 16px;
            }
            
            .panel {
                padding: 16px;
            }
            
            .instructions ul {
                display: block;
            }
            
            .instructions li {
                margin-right: 0;
                margin-bottom: 4px;
            }
            
            .instructions li:after {
                display: none;
            }
        }
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ app_title }}</h1>
            <p>Automated processing of student merit records</p>
            <div class="instructions">
                <div class="instructions-title">Quick Guide</div>
                <ul>
                    <li>Enter your eKolej credentials</li>
                    <li>Upload Excel or CSV file containing student data</li>
                    <li>Configure settings and run automation</li>
                </ul>
            </div>
        </div>

                <div class="main-content">
            <!-- Left Panel: Login & File Upload -->
            <div class="panel">
                <form method="post" enctype="multipart/form-data" id="mainForm">
                    <div class="section">
                        <div class="section-title">Login Credentials</div>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input type="text" id="username" name="username" class="form-control" placeholder="Enter username" value="{{ username or '' }}" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input type="password" id="password" name="password" class="form-control" placeholder="Enter password" value="{{ password or '' }}" required>
                        </div>
                    </div>
                    
                    <div class="section">
                        <div class="section-title">Student Data</div>
                        <div class="form-group">
                            <label for="file">Upload File</label>
                            <div class="file-upload">
                                <input type="file" id="file" name="file" accept=".xlsx,.csv" {% if not filename %}required{% endif %}>
                                <label for="file" class="file-upload-label {% if filename %}has-file{% endif %}" id="fileLabel">
                                    {% if filename %}{{ filename }}{% else %}Click to select file (.xlsx, .csv){% endif %}
                                </label>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
            
            <!-- Middle Panel: Configuration -->
            {% if columns %}
            <div class="panel">
                <div class="section-title">Configuration</div>
                <form method="post" action="{{ url_for('run_automation') }}" id="configForm">
                    <div class="form-group">
                        <label for="matric_column">Matric Column</label>
                        <select name="matric_column" id="matric_column" class="form-control" required>
                            <option value="">Select column</option>
                            {% for col in columns %}
                            <option value="{{ col }}">{{ col }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="sesi">Academic Session</label>
                        <select name="sesi" id="sesi" class="form-control" required>
                            <option value="">Select session</option>
                            {% for value, label in sesi_options %}
                            <option value="{{ value }}">{{ label }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="semester">Semester</label>
                        <select name="semester" id="semester" class="form-control" required>
                            <option value="">Select semester</option>
                            {% for value, label in semester_options %}
                            <option value="{{ value }}">{{ label }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="achievement">Achievement Level</label>
                        <select name="achievement" id="achievement" class="form-control" required>
                            <option value="">Select achievement</option>
                            {% for value, label in achievement_options %}
                            <option value="{{ value }}">{{ label }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    
                    <input type="hidden" name="username" value="{{ username }}">
                    <input type="hidden" name="password" value="{{ password }}">
                    <input type="hidden" name="filename" value="{{ filename }}">
                    <input type="hidden" name="run_automation" value="true">
                    
                    <button type="submit" class="btn" id="runBtn">Run Automation</button>
                </form>
            </div>
            {% else %}
            <div class="panel">
                <div class="section-title">Configuration</div>
                <div class="message info">Upload a file to configure automation settings.</div>
            </div>
            {% endif %}
            
            <!-- Right Panel: Results -->
            <div class="panel">
                <div class="section-title">Process Status</div>
                <div class="status-panel" id="statusPanel">
                    {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                        <div class="message {% if 'Error' in message %}error{% elif 'Warning' in message %}warning{% elif 'Processing' in message %}info{% endif %}">
                            {{ message }}
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="message info">Ready to process. Upload a file to begin.</div>
                    {% endif %}
                    {% endwith %}
                    
                    <!-- Progress Section -->
                    <div class="progress-section" id="progressSection" style="display: none;">
                        <div class="progress-header">
                            <div class="progress-title">Processing Progress</div>
                            <div class="progress-text" id="progressText">0 / 0 matric numbers processed</div>
                        </div>
                        <div class="progress-bar-container">
                            <div class="progress-bar" id="progressBar"></div>
                        </div>
                        <div class="progress-message" id="progressMessage">Initializing...</div>
                        <div class="progress-spinner" id="progressSpinner">
                            <div class="spinner"></div>
                        </div>
                    </div>
                    
                    <!-- Results Section -->
                    <div class="results-section" id="resultsSection" style="display: none;">
                        <div class="results-summary" id="resultsSummary"></div>
                        <div class="results-details" id="resultsDetails"></div>
                    </div>
                    
                    {% if failed_matrics %}
                    <div class="failed-list">
                        <div class="failed-list-title">Failed Matric Numbers</div>
                        <ul>
                            {% for matric in failed_matrics %}
                            <li>{{ matric }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    {% endif %}
                </div>
                
                <div class="loading" id="loadingDiv">
                    <div class="spinner"></div>
                    <p>Processing automation... Please wait.</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Auto-submit form when file is selected
        document.getElementById('file').addEventListener('change', function(e) {
            const file = e.target.files[0];
            const label = document.getElementById('fileLabel');
            
            if (file) {
                label.textContent = file.name;
                label.classList.add('has-file');
                
                // Auto-submit form to get columns
                setTimeout(() => {
                    document.getElementById('mainForm').submit();
                }, 500);
            }
        });
        
        // Handle configuration form submission
        document.getElementById('configForm')?.addEventListener('submit', function(e) {
            document.getElementById('loadingDiv').classList.add('show');
            document.getElementById('runBtn').disabled = true;
            document.getElementById('runBtn').textContent = 'Processing...';
            
            // Start progress tracking
            startProgressTracking();
        });
        
        // Progress tracking functionality
        let progressInterval;
        
        function startProgressTracking() {
            const progressSection = document.getElementById('progressSection');
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');
            const progressMessage = document.getElementById('progressMessage');
            const progressSpinner = document.getElementById('progressSpinner');
            const resultsSection = document.getElementById('resultsSection');
            const resultsSummary = document.getElementById('resultsSummary');
            const resultsDetails = document.getElementById('resultsDetails');
            
            // Show progress section
            progressSection.style.display = 'block';
            resultsSection.style.display = 'none';
            
            // Start polling for progress
            progressInterval = setInterval(function() {
                fetch('/progress')
                    .then(response => response.json())
                    .then(data => {
                        // Update progress bar
                        const percentage = data.total > 0 ? (data.current / data.total) * 100 : 0;
                        progressBar.style.width = percentage + '%';
                        
                        // Update progress text
                        progressText.textContent = `${data.current} / ${data.total} matric numbers processed`;
                        
                        // Update progress message
                        progressMessage.textContent = data.message || 'Processing...';
                        
                        // Handle completion or error
                        if (data.error) {
                            clearInterval(progressInterval);
                            progressSpinner.style.display = 'none';
                            
                            // Show error
                            resultsSection.style.display = 'block';
                            resultsSummary.innerHTML = '<span style="color: #dc3545;">❌ Error</span>';
                            resultsDetails.innerHTML = `<div style="color: #dc3545;">Error: ${data.error}</div>`;
                            
                            // Re-enable button
                            document.getElementById('runBtn').disabled = false;
                            document.getElementById('runBtn').textContent = 'Process Matric Numbers';
                            document.getElementById('loadingDiv').classList.remove('show');
                            
                        } else if (data.completed) {
                            clearInterval(progressInterval);
                            progressSpinner.style.display = 'none';
                            
                            // Show results
                            resultsSection.style.display = 'block';
                            
                            if (data.results) {
                                const success = data.results.success_count || 0;
                                const errors = data.results.error_count || 0;
                                
                                resultsSummary.innerHTML = '<span style="color: #28a745;">✅ Processing Complete</span>';
                                
                                let details = `<div>📊 Results: ${success} successful, ${errors} errors</div>`;
                                if (data.failed_file) {
                                    details += `<div>📄 Failed matrics saved to: ${data.failed_file}</div>`;
                                }
                                resultsDetails.innerHTML = details;
                            } else {
                                resultsSummary.innerHTML = '<span style="color: #28a745;">✅ Processing Complete</span>';
                                resultsDetails.innerHTML = '<div>Process completed successfully.</div>';
                            }
                            
                            // Re-enable button
                            document.getElementById('runBtn').disabled = false;
                            document.getElementById('runBtn').textContent = 'Process Matric Numbers';
                            document.getElementById('loadingDiv').classList.remove('show');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching progress:', error);
                    });
            }, 1000); // Poll every second
        }
        
        // Check if we should show progress on page load
        {% if show_progress %}
        window.addEventListener('load', function() {
            startProgressTracking();
        });
        {% endif %}
    </script>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Handle file upload and credential input."""
    if request.method == 'POST':
        # Check if this is a run automation request
        if request.form.get('run_automation'):
            return run_automation()

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        file = request.files.get('file')

        if not username or not password:
            flash('Username and password are required.')
            return render_template_string(HTML_TEMPLATE,
                                          app_title=APP_TITLE,
                                          sesi_options=SESI_OPTIONS,
                                          semester_options=SEMESTER_OPTIONS,
                                          achievement_options=ACHIEVEMENT_OPTIONS)

        try:
            filename, filepath = process_uploaded_file(file)
            columns = get_file_columns(filepath)
            flash(f'File uploaded: {filename}')

            return render_template_string(HTML_TEMPLATE,
                                          app_title=APP_TITLE,
                                          columns=columns,
                                          filename=filename,
                                          username=username,
                                          password=password,
                                          sesi_options=SESI_OPTIONS,
                                          semester_options=SEMESTER_OPTIONS,
                                          achievement_options=ACHIEVEMENT_OPTIONS)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return render_template_string(HTML_TEMPLATE,
                                          app_title=APP_TITLE,
                                          sesi_options=SESI_OPTIONS,
                                          semester_options=SEMESTER_OPTIONS,
                                          achievement_options=ACHIEVEMENT_OPTIONS)

    return render_template_string(HTML_TEMPLATE,
                                  app_title=APP_TITLE,
                                  sesi_options=SESI_OPTIONS,
                                  semester_options=SEMESTER_OPTIONS,
                                  achievement_options=ACHIEVEMENT_OPTIONS)


@app.route('/progress')
def get_progress():
    """Get current progress status."""
    return jsonify(progress_data)


@app.route('/run_automation', methods=['POST'])
def run_automation():
    """Run the automation process."""
    try:
        # Extract request data BEFORE starting the thread
        validated_data = validate_form_data(request.form)

        # Get matric numbers from file
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'], validated_data['filename'])
        matric_list = get_matric_list(
            filepath, validated_data['matric_column'])

        if not matric_list:
            flash('No valid matric numbers found in the selected column.')
            return render_template_string(HTML_TEMPLATE,
                                          sesi_options=SESI_OPTIONS,
                                          semester_options=SEMESTER_OPTIONS,
                                          achievement_options=ACHIEVEMENT_OPTIONS)

    except Exception as e:
        flash(f'Error: {str(e)}')
        return render_template_string(HTML_TEMPLATE,
                                      sesi_options=SESI_OPTIONS,
                                      semester_options=SEMESTER_OPTIONS,
                                      achievement_options=ACHIEVEMENT_OPTIONS)

    def run_automation_thread(validated_data, matric_list):
        """Run automation in a separate thread."""
        try:
            reset_progress()

            update_progress(0, len(
                matric_list), f'Starting to process {len(matric_list)} matric numbers...')

            # Initialize automation
            automation = MeritAkademikAutomation()
            automation.set_progress_callback(update_progress)

            try:
                # Login
                update_progress(0, len(matric_list), 'Logging in...')
                if not automation.login(validated_data['username'], validated_data['password']):
                    progress_data['error'] = 'Login failed. Please check your credentials.'
                    return

                # Navigate to Merit Akademik page
                update_progress(0, len(matric_list),
                                'Navigating to Merit Akademik page...')
                automation.navigate_to_merit_akademik()

                # Process all matric numbers
                results = automation.process_matric_list(
                    matric_list,
                    validated_data['sesi'],
                    validated_data['semester'],
                    validated_data['achievement']
                )

                # Save failed matrics to file
                failed_file = None
                if results['failed_matrics']:
                    failed_file = automation.save_failed_matrics(
                        results['failed_matrics'],
                        validated_data['sesi'],
                        validated_data['semester'],
                        validated_data['achievement']
                    )

                # Update final progress
                update_progress(
                    len(matric_list),
                    len(matric_list),
                    f'Completed: {results["success_count"]} successful, {results["error_count"]} errors'
                )

                # Store results in progress data
                progress_data['results'] = results
                progress_data['failed_file'] = failed_file

            finally:
                automation.quit()

        except Exception as e:
            progress_data['error'] = str(e)
            progress_data['completed'] = True

    # Start automation in background thread with the extracted data
    thread = threading.Thread(
        target=run_automation_thread, args=(validated_data, matric_list))
    thread.daemon = True
    thread.start()

    # Return to same page with processing message
    flash(f'Started processing {len(matric_list)} matric numbers...')
    return render_template_string(HTML_TEMPLATE,
                                  sesi_options=SESI_OPTIONS,
                                  semester_options=SEMESTER_OPTIONS,
                                  achievement_options=ACHIEVEMENT_OPTIONS,
                                  show_progress=True)


@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    """Serve screenshot files for debugging."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
