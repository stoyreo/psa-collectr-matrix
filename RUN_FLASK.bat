@echo off
title Flask Server - PSA x Collectr Tracer
cd /d "%~dp0"

echo Installing required packages...
python -m pip install flask flask-cors anthropic --quiet

echo Starting Flask backend...
python webapp.py
pause
