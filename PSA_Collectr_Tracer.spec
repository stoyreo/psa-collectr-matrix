# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for PSA x Collectr Tracer
Produces:  dist\PSA_Collectr_Tracer\PSA_Collectr_Tracer.exe
"""

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# ── Data files to bundle ─────────────────────────────────────────────────────
datas = [
    # HTML template
    ("templates",                   "templates"),
    # Python script modules (imported at runtime)
    ("scripts",                     "scripts"),
    # Portfolio CSV
    ("My Collection CSV - 19.csv",  "."),
]

# Bundle playwright Python package data (NOT the browsers — downloaded at runtime)
datas += collect_data_files("playwright")

# ── Hidden imports ───────────────────────────────────────────────────────────
hiddenimports = (
    collect_submodules("flask") +
    collect_submodules("werkzeug") +
    collect_submodules("jinja2") +
    collect_submodules("click") +
    collect_submodules("itsdangerous") +
    collect_submodules("markupsafe") +
    collect_submodules("playwright") +
    [
        # Our scripts
        "scripts.config",
        "scripts.ingest",
        "scripts.matching",
        "scripts.refresh_live",
        "scripts.collectr_live_prices",
        "scripts.collectr_live_fetcher",
        "scripts.signals",
        "scripts.cache_manager",
        "scripts.excel_writer",
        "scripts.quantitative_matrix",
        # stdlib
        "openpyxl",
        "asyncio",
        "threading",
        "json",
        "csv",
        "pathlib",
        "datetime",
        "re",
        "logging",
    ]
)

# ── Analysis ─────────────────────────────────────────────────────────────────
a = Analysis(
    ["launcher.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "pandas", "PIL", "cv2"],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PSA_Collectr_Tracer",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,        # Keep console so user sees status messages
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PSA_Collectr_Tracer",
)
