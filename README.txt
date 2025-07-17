======================================
Merit Akademik Automation Tool (v1.06)
======================================

This tool allows you to automatically input student merit data into the UPM eKolej system using an Excel or CSV file containing matric numbers.

-----------------------
🧾 HOW TO USE THIS TOOL
-----------------------

1. Run **MeritAkademikAutomation.exe**
   - This will launch a local automation server in the background.

2. Open your browser and go to:
   👉 http://127.0.0.1:5000

3. Log in with your **eKolej credentials**

4. Upload your **Excel (.xlsx)** or **CSV** file with a column of matric numbers.

5. Choose the correct **Session**, **Semester**, and **Achievement** options  
   ⚠ Please verify these values on the eKolej page before starting. If the options in this tool do not match the current system values, it may result in failure.

6. Select the correct column that contains the matric numbers from the dropdown.

7. Click **Run Automation** to start the automatic submission process.

8. After processing:
   - A summary of success and failed matric numbers will be shown.
   - Failed cases will be saved to a `.csv` file for review.

-----------------------
❗ TROUBLESHOOTING
-----------------------

📸 If something goes wrong, check the `data/screenshots/` folder. Screenshots are automatically captured at the moment of failure. Examples:

- `login_error.png` → login field not found or incorrect credentials
- `navigation_error.png` → unable to find or click the Merit menu
- `submenu_not_found.png` → could not locate the "Merit Akademik" submenu
- `matric_error_<matric>.png` → failure during data input for specific student

🧾 Also check:
✔ You selected the correct **merit configuration** values  
✔ Your account has access to the Merit Akademik module  
✔ Your Excel/CSV file is formatted correctly:

    ✅ The file must include a header row (first row)
    ✅ The column containing matric numbers must have a proper title
    ✅ You will select the correct column during upload

    ✅ Example Excel format:

        | Matric  |
        |---------|
        | 215035  |
        | 217088  |
        | 227890  |

    ❌ Do NOT:
        - Leave the first row blank
        - Include multiple header rows
        - Upload a file without any headers

-----------------------
📅 Last Built:
-----------------------
15 July 2025

-----------------------
✅ Created by:
-----------------------
Chan Ci En
