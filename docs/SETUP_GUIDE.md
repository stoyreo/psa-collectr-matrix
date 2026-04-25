# Pokémon TCG Portfolio Intelligence System - Setup Guide

## Quick Start

This guide walks you through installing and running the Pokémon TCG Portfolio Intelligence System on your Windows machine.

---

## 1. Prerequisites

Before starting, ensure you have:

- **Windows 7 or later** (tested on Windows 10/11)
- **Python 3.8 or higher** installed
  - Download from [python.org](https://www.python.org)
  - During installation, **check "Add Python to PATH"**
  - Verify by opening Command Prompt and typing: `python --version`
- **pip** (Python package manager, included with Python 3.8+)
  - Verify: `pip --version`

---

## 2. Installation

### Step 1: Create Project Directory

Choose a location on your computer where you want to install the system. For example:

```
C:\Users\YourName\Documents\Pokemon-Portfolio
```

Create this directory and copy all project files into it. Your structure should look like:

```
Pokemon-Portfolio/
├── scripts/
│   ├── main.py
│   ├── config.py
│   ├── refresh.py
│   ├── ingest.py
│   ├── matching.py
│   ├── ebay_connector.py
│   ├── collectr_connector.py
│   ├── psa_connector.py
│   ├── signals.py
│   ├── cache_manager.py
│   └── excel_writer.py
├── REFRESH.bat
├── requirements.txt
├── My Collection CSV - 19.csv
├── README.md
└── docs/
```

### Step 2: Install Python Dependencies

Open Command Prompt and navigate to your project directory:

```cmd
cd C:\Users\YourName\Documents\Pokemon-Portfolio
```

Run the following command to install all required packages:

```cmd
pip install -r requirements.txt
```

This installs:
- `openpyxl` - Excel workbook generation
- `requests` - HTTP requests (future live eBay connector)
- `python-dateutil` - Date handling

**Expected output:**
```
Successfully installed openpyxl-3.x.x requests-2.x.x python-dateutil-2.x.x
```

If you see errors, verify:
- Python and pip are in your PATH
- You have internet connectivity
- No firewall is blocking pip (uncommon)

---

## 3. Prepare Your Collection Data

### Getting Your PSA Collection CSV

1. Log into your PSA account at [psacard.com](https://www.psacard.com)
2. Navigate to **My Collection**
3. Click **Export Collection** and select **CSV format**
4. Download the file (e.g., `My Collection CSV - 19.csv`)

### Place the CSV in the Project Root

Move the downloaded CSV file to your project root directory:

```
Pokemon-Portfolio/
├── scripts/
├── My Collection CSV - 19.csv  ← Place your CSV here
├── REFRESH.bat
└── requirements.txt
```

**Note:** The system looks for any CSV file with "My Collection" in the filename. If your filename is different, either rename it to match or edit `scripts/config.py` and change the `CSV_INPUT_PATH` variable.

---

## 4. Running the System

### Option A: One-Click Refresh (Recommended)

Simply double-click `REFRESH.bat` in your project directory.

**What happens:**
1. Python starts the refresh process
2. Console window shows progress (ingest → comps → signals → export)
3. Excel file automatically opens when complete
4. Console window closes automatically

**Expected duration:** 10-30 seconds

### Option B: Manual Command Line

If you prefer to see all output, open Command Prompt in the project directory and run:

```cmd
python scripts/main.py
```

This shows all logs in real-time. Press `Ctrl+C` to stop at any time.

---

## 5. Understanding the Output

After running a refresh, two files are created:

### `output/Pokemon_Portfolio_Intelligence.xlsx`

Your main portfolio workbook with 10 sheets:

| Sheet | Purpose |
|-------|---------|
| **DASHBOARD** | Executive summary with KPI cards, signal distribution, and key metrics |
| **PORTFOLIO** | Complete card-by-card breakdown with costs, market values, signals, and confidence |
| **EBAY_COMPS** | All pricing comps collected from eBay sold listings (demo data) |
| **COLLECTR_MAP** | Collectr pricing (currently stub; reserved for future integration) |
| **PSA_MAP** | Raw PSA certificate data mapped to your portfolio |
| **INSIGHTS** | Curated analysis: top gainers, weak positions, and high-risk cards |
| **EXCEPTIONS** | Any data quality issues or cards that couldn't be matched |
| **TARGETS** | Cards you can configure for price-triggered alerts |
| **ALERT_LOG** | Record of triggered alerts and system notifications |
| **CONFIG** | System configuration parameters and settings |

### `output/portfolio_refresh.log`

A detailed log file of the entire refresh process. Useful for:
- Debugging issues
- Tracking which cards matched to which comps
- Reviewing confidence scores and filtering decisions

Open it with any text editor.

---

## 6. Customization

### Changing Signal Thresholds

Edit `scripts/config.py` to adjust when cards receive BUY/SELL/HOLD signals:

```python
SIGNAL_CONFIG = {
    "buy_upside_multiplier": 1.15,      # 15% upside triggers BUY
    "sell_downside_multiplier": 0.85,   # 15% downside triggers SELL
    "buy_confidence_threshold": 85,      # Only if 85%+ confident
    "liquidity_thresholds": {
        "high": 8,                       # 8+ comps = HIGH liquidity
        "medium": 4,
        "low": 0,
    },
}
```

After editing, re-run REFRESH.bat to apply changes.

### Demo Mode vs. Live Data

Currently, the system runs in **DEMO MODE**, generating realistic sample comps based on PSA Estimates (±15% variance).

To use live eBay data in the future:
1. Obtain an eBay API key
2. Set `DATA_SOURCES["demo_mode"] = False` in `scripts/config.py`
3. Configure your eBay API credentials

### Changing CSV Location

If your CSV isn't named "My Collection CSV - 19.csv", edit `scripts/config.py`:

```python
CSV_INPUT_PATH = DATA_DIR / "Your CSV Filename.csv"
```

### Adjusting Currency and Locale

To work in Thai Baht (THB) or other currencies:

```python
CURRENCY = {
    "primary": "USD",
    "display_options": ["USD", "THB"],
    "default_display": "USD",
    "exchange_rates": {
        "USD_to_THB": 35.0,  # Update with current rate
    }
}
```

The system stores values in USD internally but can display in alternate currencies.

---

## 7. Troubleshooting

### Problem: "Python command not found"

**Solution:**
- Ensure Python is installed and added to PATH
- Restart Command Prompt after installing Python
- Try full path: `C:\Python3.11\python.exe scripts/main.py`

### Problem: "ModuleNotFoundError: No module named 'openpyxl'"

**Solution:**
- Run `pip install -r requirements.txt` again
- Verify `requirements.txt` is in your project root
- Check that pip installed successfully: `pip list`

### Problem: "CSV file not found"

**Solution:**
- Ensure your PSA CSV is in the project root directory
- Check the filename matches what's in `scripts/config.py`
- Don't leave the file in Downloads; move it to the project folder

### Problem: "No comps found for some cards"

**This is normal in DEMO mode.** Cards may have few or no sample comps generated if:
- The PSA Estimate is very high or unusual
- The card grade/set combination is rare

In live mode with real eBay data, this is much rarer.

### Problem: Excel doesn't open automatically

**Solution:**
- The file was created successfully; open it manually from:
  - File Explorer → `output/Pokemon_Portfolio_Intelligence.xlsx`
  - Or from within Excel via File → Open Recent

### Problem: "ImportError" when running main.py

**Solution:**
- Verify all Python files are in the `scripts/` directory
- Check file permissions (files should be readable)
- Run `pip install -r requirements.txt` to ensure all dependencies are installed

### Problem: Permission Denied

If you get "Permission Denied" errors:
- Right-click `REFRESH.bat` → **Run as Administrator**
- Or right-click the project folder → **Properties** → **Security** → ensure your user has Read/Write permissions

---

## 8. Next Steps

After your first successful refresh:

1. **Review the DASHBOARD sheet** to understand your portfolio's overall health
2. **Check the INSIGHTS sheet** for specific recommendations
3. **Explore the CONFIG sheet** to understand all system parameters
4. **Adjust signal thresholds** in `config.py` if signals don't align with your strategy
5. **Set up TARGETS** for cards you want to monitor with price alerts (future feature)

---

## 9. Getting Help

If you encounter issues:

1. **Check the log file:** `output/portfolio_refresh.log` contains detailed error messages
2. **Review this guide's Troubleshooting section**
3. **Verify your CSV format** matches PSA's standard export structure
4. **Ensure Python and pip are up to date:** `pip install --upgrade pip`

---

## 10. System Requirements & Compatibility

| Component | Requirement |
|-----------|------------|
| Operating System | Windows 7, 8, 10, 11 |
| Python Version | 3.8, 3.9, 3.10, 3.11, 3.12 |
| RAM | 512 MB minimum (1 GB recommended) |
| Disk Space | 100 MB for installation |
| CSV Encoding | UTF-8 (PSA exports in this format) |
| Excel Format | .xlsx (Office 2010 and later) |

The system has been tested on:
- Windows 10 Pro (build 19043)
- Windows 11 Home (build 22631)
- Python 3.9, 3.10, 3.11

---

## 11. Uninstalling

To remove the system:

1. Delete the project directory
2. (Optional) To remove Python packages without uninstalling Python:
   ```cmd
   pip uninstall openpyxl requests python-dateutil
   ```

Your PSA data remains safe in PSA's system; nothing is permanently deleted.

---

**Last Updated:** April 2026  
**System Version:** 1.0  
**Support:** Contact system administrator for questions
