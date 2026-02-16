#!/usr/bin/env python3
"""
sysinfo - Interactive Linux system information viewer
Run: python3 sysinfo.py
"""

import curses
import psutil
import platform
import subprocess
import os
from datetime import datetime, timedelta


class SysInfoViewer:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.current_view = 'main'
        self.setup_colors()
        
    def setup_colors(self):
        """Initialize color pairs"""
        curses.curs_set(0)  # Hide cursor
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Headers
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Active
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Warning
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Normal
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Yellow
        
    def draw_header(self):
        """Draw top header"""
        self.stdscr.addstr(0, 0, "╔" + "═" * (curses.COLS - 2) + "╗", curses.color_pair(1))
        title = "  System Information Viewer  "
        self.stdscr.addstr(0, (curses.COLS - len(title)) // 2, title, curses.color_pair(1) | curses.A_BOLD)
        
    def draw_footer(self):
        """Draw navigation footer"""
        footer = "🔱 (1)Overview  (2)CPU  (3)Memory  (4)Disk  (5)Network  (6)Process  (q)Quit"
        self.stdscr.addstr(curses.LINES - 1, 0, footer[:curses.COLS], curses.color_pair(5))
        
    def draw_section(self, y, title, content):
        """Draw a section with title and content"""
        self.stdscr.addstr(y, 2, f"▸ {title}", curses.color_pair(1) | curses.A_BOLD)
        for i, line in enumerate(content.split('\n')):
            if y + i + 1 < curses.LINES - 1:
                line_display = line[:curses.COLS - 4]
                self.stdscr.addstr(y + i + 1, 4, line_display, curses.color_pair(4))
        return y + len(content.split('\n')) + 2
        
    def get_cpu_info(self):
        """Get CPU information"""
        cpu_count = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
        
        info = f"Physical Cores: {cpu_count}\n"
        info += f"Logical Cores: {cpu_logical}\n"
        info += f"Frequency: {cpu_freq.current:.1f} MHz\n\n"
        info += "Per-Core Usage:\n"
        for i, percent in enumerate(cpu_percent[:8]):  # Show first 8 cores
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            info += f"  Core {i}: [{bar}] {percent:5.1f}%\n"
        if len(cpu_percent) > 8:
            info += f"  ... and {len(cpu_percent) - 8} more cores\n"
        
        avg = psutil.cpu_percent(interval=0.5)
        info += f"\nAverage: {avg:.1f}%"
        return info
        
    def get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        def draw_bar(used, total):
            percent = (used / total * 100) if total > 0 else 0
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            return f"[{bar}] {percent:.1f}%"
        
        info = f"Physical Memory:\n"
        info += f"  Used: {mem.used / (1024**3):.1f} GB / {mem.total / (1024**3):.1f} GB\n"
        info += f"  {draw_bar(mem.used, mem.total)}\n"
        info += f"  Available: {mem.available / (1024**3):.1f} GB\n\n"
        
        info += f"Swap:\n"
        info += f"  Used: {swap.used / (1024**3):.1f} GB / {swap.total / (1024**3):.1f} GB\n"
        info += f"  {draw_bar(swap.used, swap.total)}"
        
        return info
        
    def get_disk_info(self):
        """Get disk usage information"""
        info = ""
        for partition in psutil.disk_partitions():
            if partition.fstype:  # Skip pseudo filesystems
                usage = psutil.disk_usage(partition.mountpoint)
                percent = usage.percent
                bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
                info += f"{partition.device} ({partition.fstype})\n"
                info += f"  {partition.mountpoint}\n"
                info += f"  {usage.used / (1024**3):.1f} GB / {usage.total / (1024**3):.1f} GB\n"
                info += f"  [{bar}] {percent:.1f}%\n\n"
        
        return info.strip() if info else "No disk partitions found"
        
    def get_network_info(self):
        """Get network information"""
        info = ""
        net_if = psutil.net_if_addrs()
        
        for interface, addrs in net_if.items():
            info += f"{interface}:\n"
            for addr in addrs:
                info += f"  {addr.family.name}: {addr.address}\n"
            info += "\n"
        
        # Network I/O stats
        net_io = psutil.net_io_counters()
        info += f"Network Stats:\n"
        info += f"  Bytes Sent: {net_io.bytes_sent / (1024**3):.2f} GB\n"
        info += f"  Bytes Recv: {net_io.bytes_recv / (1024**3):.2f} GB\n"
        info += f"  Packets Sent: {net_io.packets_sent}\n"
        info += f"  Packets Recv: {net_io.packets_recv}"
        
        return info
        
    def get_process_info(self):
        """Get top processes by memory and CPU"""
        info = "Top 5 by Memory Usage:\n"
        procs = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), 
                      key=lambda p: p.info['memory_percent'], reverse=True)[:5]
        
        for p in procs:
            try:
                info += f"  {p.info['name'][:30]:<30} {p.info['memory_percent']:>6.1f}%\n"
            except:
                pass
        
        info += "\nTop 5 by CPU Usage:\n"
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                      key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:5]
        
        for p in procs:
            try:
                cpu = p.info['cpu_percent'] or 0
                info += f"  {p.info['name'][:30]:<30} {cpu:>6.1f}%\n"
            except:
                pass
        
        return info
        
    def get_overview(self):
        """Get system overview"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        info = f"OS: {platform.system()} {platform.release()}\n"
        info += f"Hostname: {platform.node()}\n"
        info += f"Uptime: {str(uptime).split('.')[0]}\n"
        info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        info += f"CPU: {platform.processor()}\n"
        info += f"Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical\n\n"
        
        mem = psutil.virtual_memory()
        info += f"Memory: {mem.used / (1024**3):.1f} / {mem.total / (1024**3):.1f} GB ({mem.percent:.1f}%)\n"
        
        return info
        
    def view_overview(self):
        """Display overview screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "System Overview", self.get_overview())
        y = self.draw_section(y, "Quick Stats", self.get_cpu_info()[:200])
        self.draw_footer()
        
    def view_cpu(self):
        """Display CPU screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "CPU Information", self.get_cpu_info())
        self.draw_footer()
        
    def view_memory(self):
        """Display memory screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "Memory Information", self.get_memory_info())
        self.draw_footer()
        
    def view_disk(self):
        """Display disk screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "Disk Usage", self.get_disk_info())
        self.draw_footer()
        
    def view_network(self):
        """Display network screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "Network Information", self.get_network_info())
        self.draw_footer()
        
    def view_process(self):
        """Display process screen"""
        self.stdscr.clear()
        self.draw_header()
        y = 2
        y = self.draw_section(y, "Process Information", self.get_process_info())
        self.draw_footer()
        
    def run(self):
        """Main run loop"""
        while True:
            try:
                self.view_overview()
                self.stdscr.refresh()
                
                key = self.stdscr.getch()
                
                if key == ord('q'):
                    break
                elif key == ord('1'):
                    self.view_overview()
                elif key == ord('2'):
                    self.view_cpu()
                elif key == ord('3'):
                    self.view_memory()
                elif key == ord('4'):
                    self.view_disk()
                elif key == ord('5'):
                    self.view_network()
                elif key == ord('6'):
                    self.view_process()
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.stdscr.addstr(10, 10, f"Error: {str(e)[:50]}")
                self.stdscr.refresh()
                self.stdscr.getch()


def main():
    try:
        curses.wrapper(lambda stdscr: SysInfoViewer(stdscr).run())
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have psutil installed: pip install psutil")


if __name__ == '__main__':
    main()
