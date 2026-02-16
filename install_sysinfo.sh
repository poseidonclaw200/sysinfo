#!/bin/bash
# Installer for sysinfo - Install both TUI and GUI versions

set -e

echo "╔════════════════════════════════════════╗"
echo "║   Installing sysinfo (TUI & GUI)      ║"
echo "╚════════════════════════════════════════╝"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 not found. Please install Python 3 first."
    exit 1
fi

# Install psutil
echo ""
echo "📦 Installing dependencies..."
pip3 install psutil -q

# Check if running with sudo
if [ "$EUID" -ne 0 ]; then
   echo ""
   echo "⚠️  Note: Installing to /usr/local/bin requires sudo"
   echo ""
   SUDO="sudo"
else
   SUDO=""
fi

# Install TUI version
echo "📝 Installing TUI version..."
$SUDO cp sysinfo.py /usr/local/bin/sysinfo
$SUDO chmod +x /usr/local/bin/sysinfo

# Install GUI version
echo "🖥️  Installing GUI version..."
$SUDO cp sysinfo_gui.py /usr/local/bin/sysinfo-gui
$SUDO chmod +x /usr/local/bin/sysinfo-gui

echo ""
echo "✅ Installation complete!"
echo ""
echo "📝 TUI version:  sysinfo"
echo "🖥️  GUI version:  sysinfo-gui"
echo ""
echo "Run with:"
echo "  sysinfo           # Terminal UI"
echo "  sysinfo-gui       # Graphical UI"
