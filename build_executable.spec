# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],  # Changed from app/app.py to run.py
    pathex=['.'],  # Add current directory to Python path
    binaries=[],
    datas=[
        ('data/uploads', 'data/uploads'),
        ('data/screenshots', 'data/screenshots'),
    ],
    hiddenimports=[
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.chrome.service',
        'pandas',
        'openpyxl',
        'werkzeug.utils',
        'flask',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MeritAkademikAutomation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True to see any errors during startup
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if you have one
)

# Create a single executable file
# Note: Screenshots and uploads folders will be created relative to the exe location 