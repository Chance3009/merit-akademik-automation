# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('data/uploads', 'data/uploads'),
        ('data/screenshots', 'data/screenshots'),
        ('chrome-bin', 'chrome-bin'),  # Bundle Chrome with the executable
    ],
    hiddenimports=[
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.chrome.service',
        'openpyxl',
        'werkzeug.utils',
        'flask',
        'csv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Scientific computing (removed with pandas)
        'pandas',
        'numpy',
        'matplotlib',
        'scipy',
        'sympy',
        'IPython',
        'jupyter',
        'notebook',
        
        # GUI libraries (not needed for web app)
        'tkinter',
        'turtle',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'wx',
        
        # Development/testing tools
        'test',
        'unittest',
        'pytest',
        'pydoc',
        'doctest',
        'pdb',
        'profile',
        'cProfile',
        
        # Database libraries (not used)
        'sqlite3',
        'mysql',
        'psycopg2',
        'pymongo',
        
        # Network libraries (not needed)
        'ftplib',
        'poplib',
        'imaplib',
        'smtplib',
        'telnetlib',
        
        # Media libraries
        'PIL.ImageQt',
        'imageio',
        'cv2',
        'skimage',
        
        # Misc large modules
        'asyncio',
        'multiprocessing',
        'concurrent.futures',
        'distutils',
        'setuptools',
        'pip',
    ],
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
    strip=False,  # Disable strip for Windows compatibility
    upx=True,   # Keep UPX compression
    upx_exclude=[
        'chrome.exe',
        'chromedriver.exe',
        'vcruntime140.dll',  # Don't compress these critical files
    ],
    runtime_tmpdir=None,
    console=True,  # Enable console for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
) 