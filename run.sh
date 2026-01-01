#!/bin/bash

echo "===================================="
echo " Minecraft 2D Mining Game - Python"
echo "===================================="
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 not found! Please install Python 3.7+"
    exit 1
fi

python3 --version

echo ""
echo "Checking dependencies..."
if ! python3 -c "import pygame" 2>/dev/null; then
    echo "[!] pygame not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting game..."
python3 main.py
