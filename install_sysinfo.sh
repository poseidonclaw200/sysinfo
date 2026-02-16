#!/bin/bash
# Simple installer for sysinfo app

echo "Installing sysinfo..."

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 not found. Please install Python 3 first."
    exit 1
fi

# Install psutil
pip3 install psutil -q

# Install sysinfo to /usr/local/bin
sudo cp sysinfo.py /usr/local/bin/sysinfo
sudo chmod +x /usr/local/bin/sysinfo

echo "✓ Installation complete!"
echo "Run with: sysinfo"
