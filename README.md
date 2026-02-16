# sysinfo - Interactive System Monitor

A lightweight, interactive Python app to view system information on any Linux machine. Available in both **TUI (Terminal UI)** and **GUI (Graphical UI)** versions.

## Features

### Both Versions
- **Overview**: System basics (OS, uptime, hostname, CPU cores, memory)
- **CPU**: Per-core usage with visual bars, frequency, core count
- **Memory**: RAM and swap usage with visual bars
- **Disk**: Partition usage for all mounted filesystems
- **Network**: Interface info and I/O statistics
- **Processes**: Top processes by memory and CPU usage

### TUI (Terminal Version)
- Interactive navigation with number keys
- Smooth terminal UI with colors
- Works over SSH
- No graphics dependencies

### GUI (Graphical Version)
- Tabbed interface (easier navigation)
- Auto-refresh feature
- Point-and-click interface
- Visual design with modern styling

## Requirements

- Python 3.6+
- `psutil` (installed automatically)
- Linux OS
- For GUI: tkinter (usually included with Python)
- Terminal with color support (TUI only)

## Installation

### Option 1: Quick Install (Recommended)
```bash
git clone https://github.com/poseidonclaw200/sysinfo.git
cd sysinfo
chmod +x install_sysinfo.sh
./install_sysinfo.sh
```

Then run from anywhere:
```bash
sysinfo           # TUI version
sysinfo-gui       # GUI version
```

### Option 2: Manual Install
```bash
pip3 install psutil

# TUI
chmod +x sysinfo.py
python3 sysinfo.py

# GUI
chmod +x sysinfo_gui.py
python3 sysinfo_gui.py
```

### Option 3: No Install (Just Run)
```bash
pip3 install psutil
python3 sysinfo.py          # TUI
# or
python3 sysinfo_gui.py      # GUI
```

## Usage

### TUI Version
```
Press keys to navigate:
  1 - Overview
  2 - CPU info
  3 - Memory info
  4 - Disk usage
  5 - Network info
  6 - Top processes
  q - Quit
```

### GUI Version
- Click tabs to switch views
- Click "Refresh" to update data
- Check "Auto-refresh" for continuous updates (5s interval)
- Click "Exit" to quit

## File Structure

```
sysinfo.py           - TUI app (standalone, ~350 lines)
sysinfo_gui.py       - GUI app (standalone, ~600 lines)
install_sysinfo.sh   - Installer script
README.md            - This file
```

## How It Works

- Uses `psutil` for cross-platform system info
- **TUI**: Renders with `curses` (built-in Python)
- **GUI**: Uses `tkinter` (built-in Python)
- Updates data on demand (no lag)
- Works on any Linux distro (Ubuntu, Debian, CentOS, Fedora, etc.)

## Troubleshooting

**"psutil not found"**
```bash
pip3 install psutil
```

**TUI: "Colors not showing"**
```bash
export TERM=xterm-256color
```

**GUI: "No module named tkinter"**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# macOS
brew install python-tk@3.11
```

**"Command not found" after install**
Make sure `/usr/local/bin` is in your PATH:
```bash
echo $PATH | grep /usr/local/bin
```

## Performance

- **Lightweight**: ~15MB total (psutil)
- **Fast startup**: <1 second
- **Low CPU usage**: Only reads when refreshed
- **Minimal memory footprint**: <50MB

## Platforms

Tested on:
- Ubuntu 20.04, 22.04, 24.04
- Debian 11, 12, 13
- CentOS 7, 8
- Fedora 38, 39
- Raspberry Pi OS

## License

Free to use and modify. Enjoy! 🔱
