#!/usr/bin/env python3
"""
sysinfo GUI - Interactive system information viewer with graphical interface
Run: python3 sysinfo_gui.py
"""

import tkinter as tk
from tkinter import ttk
import psutil
import platform
from datetime import datetime
import threading


class SysInfoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Information Viewer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background="#f0f0f0", borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        self.setup_ui()
        self.update_data()
        
    def setup_ui(self):
        """Create the main UI"""
        # Header
        header = tk.Frame(self.root, bg="#1a1a2e", height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(header, text="🔱 System Information Viewer", 
                        font=("Helvetica", 18, "bold"), 
                        bg="#1a1a2e", fg="white")
        title.pack(pady=10)
        
        # Notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.overview_tab = ttk.Frame(self.notebook)
        self.cpu_tab = ttk.Frame(self.notebook)
        self.memory_tab = ttk.Frame(self.notebook)
        self.disk_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)
        self.process_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.overview_tab, text="Overview")
        self.notebook.add(self.cpu_tab, text="CPU")
        self.notebook.add(self.memory_tab, text="Memory")
        self.notebook.add(self.disk_tab, text="Disk")
        self.notebook.add(self.network_tab, text="Network")
        self.notebook.add(self.process_tab, text="Processes")
        
        # Populate tabs
        self.create_overview_tab()
        self.create_cpu_tab()
        self.create_memory_tab()
        self.create_disk_tab()
        self.create_network_tab()
        self.create_process_tab()
        
        # Footer with refresh button
        footer = tk.Frame(self.root, bg="#f0f0f0")
        footer.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = tk.Button(footer, text="🔄 Refresh", command=self.update_data,
                               bg="#0066cc", fg="white", padx=20, pady=5, 
                               font=("Helvetica", 10, "bold"), cursor="hand2")
        refresh_btn.pack(side=tk.LEFT)
        
        auto_refresh = tk.Checkbutton(footer, text="Auto-refresh every 5s",
                                     variable=tk.BooleanVar(value=False),
                                     command=self.toggle_auto_refresh,
                                     font=("Helvetica", 9))
        auto_refresh.pack(side=tk.LEFT, padx=20)
        self.auto_refresh_var = auto_refresh.var
        
        exit_btn = tk.Button(footer, text="Exit", command=self.root.quit,
                            bg="#cc0000", fg="white", padx=20, pady=5,
                            font=("Helvetica", 10, "bold"), cursor="hand2")
        exit_btn.pack(side=tk.RIGHT)
        
    def create_overview_tab(self):
        """Overview tab"""
        canvas = tk.Canvas(self.overview_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.overview_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.overview_text = tk.Text(scrollable_frame, height=30, width=80,
                                    font=("Courier", 10), bg="white",
                                    relief=tk.FLAT, borderwidth=0)
        self.overview_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_cpu_tab(self):
        """CPU tab"""
        canvas = tk.Canvas(self.cpu_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.cpu_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.cpu_text = tk.Text(scrollable_frame, height=30, width=80,
                               font=("Courier", 10), bg="white",
                               relief=tk.FLAT, borderwidth=0)
        self.cpu_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_memory_tab(self):
        """Memory tab"""
        canvas = tk.Canvas(self.memory_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.memory_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.memory_text = tk.Text(scrollable_frame, height=30, width=80,
                                  font=("Courier", 10), bg="white",
                                  relief=tk.FLAT, borderwidth=0)
        self.memory_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_disk_tab(self):
        """Disk tab"""
        canvas = tk.Canvas(self.disk_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.disk_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.disk_text = tk.Text(scrollable_frame, height=30, width=80,
                                font=("Courier", 10), bg="white",
                                relief=tk.FLAT, borderwidth=0)
        self.disk_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_network_tab(self):
        """Network tab"""
        canvas = tk.Canvas(self.network_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.network_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.network_text = tk.Text(scrollable_frame, height=30, width=80,
                                   font=("Courier", 10), bg="white",
                                   relief=tk.FLAT, borderwidth=0)
        self.network_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_process_tab(self):
        """Process tab"""
        canvas = tk.Canvas(self.process_tab, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.process_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.process_text = tk.Text(scrollable_frame, height=30, width=80,
                                   font=("Courier", 10), bg="white",
                                   relief=tk.FLAT, borderwidth=0)
        self.process_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def update_data(self):
        """Update all tabs with current data"""
        thread = threading.Thread(target=self._update_all, daemon=True)
        thread.start()
        
    def _update_all(self):
        """Background thread to update data"""
        self.overview_text.config(state=tk.NORMAL)
        self.overview_text.delete(1.0, tk.END)
        self.overview_text.insert(tk.END, self.get_overview())
        self.overview_text.config(state=tk.DISABLED)
        
        self.cpu_text.config(state=tk.NORMAL)
        self.cpu_text.delete(1.0, tk.END)
        self.cpu_text.insert(tk.END, self.get_cpu_info())
        self.cpu_text.config(state=tk.DISABLED)
        
        self.memory_text.config(state=tk.NORMAL)
        self.memory_text.delete(1.0, tk.END)
        self.memory_text.insert(tk.END, self.get_memory_info())
        self.memory_text.config(state=tk.DISABLED)
        
        self.disk_text.config(state=tk.NORMAL)
        self.disk_text.delete(1.0, tk.END)
        self.disk_text.insert(tk.END, self.get_disk_info())
        self.disk_text.config(state=tk.DISABLED)
        
        self.network_text.config(state=tk.NORMAL)
        self.network_text.delete(1.0, tk.END)
        self.network_text.insert(tk.END, self.get_network_info())
        self.network_text.config(state=tk.DISABLED)
        
        self.process_text.config(state=tk.NORMAL)
        self.process_text.delete(1.0, tk.END)
        self.process_text.insert(tk.END, self.get_process_info())
        self.process_text.config(state=tk.DISABLED)
        
    def get_overview(self):
        """Get system overview"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        info = "=== SYSTEM OVERVIEW ===\n\n"
        info += f"OS: {platform.system()} {platform.release()}\n"
        info += f"Hostname: {platform.node()}\n"
        info += f"Uptime: {str(uptime).split('.')[0]}\n"
        info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        info += f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        info += f"CPU: {platform.processor()}\n"
        info += f"Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical\n\n"
        
        mem = psutil.virtual_memory()
        info += f"Memory: {mem.used / (1024**3):.1f} / {mem.total / (1024**3):.1f} GB ({mem.percent:.1f}%)\n"
        info += f"Memory Available: {mem.available / (1024**3):.1f} GB\n"
        
        return info
        
    def get_cpu_info(self):
        """Get CPU information"""
        cpu_count = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)
        
        info = "=== CPU INFORMATION ===\n\n"
        info += f"Physical Cores: {cpu_count}\n"
        info += f"Logical Cores: {cpu_logical}\n"
        info += f"Frequency: {cpu_freq.current:.1f} MHz\n"
        info += f"Max Frequency: {cpu_freq.max:.1f} MHz\n\n"
        
        info += "Per-Core Usage:\n"
        for i, percent in enumerate(cpu_percent[:16]):  # Show first 16
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            info += f"  Core {i:2d}: [{bar}] {percent:6.1f}%\n"
        
        if len(cpu_percent) > 16:
            info += f"\n  ... and {len(cpu_percent) - 16} more cores\n"
        
        avg = psutil.cpu_percent(interval=0.5)
        info += f"\nAverage CPU Usage: {avg:.1f}%\n"
        
        return info
        
    def get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        def draw_bar(used, total):
            percent = (used / total * 100) if total > 0 else 0
            bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
            return f"[{bar}] {percent:.1f}%"
        
        info = "=== MEMORY INFORMATION ===\n\n"
        info += f"Physical Memory:\n"
        info += f"  Used: {mem.used / (1024**3):.2f} GB / {mem.total / (1024**3):.2f} GB\n"
        info += f"  {draw_bar(mem.used, mem.total)}\n"
        info += f"  Available: {mem.available / (1024**3):.2f} GB\n"
        info += f"  Free: {mem.free / (1024**3):.2f} GB\n\n"
        
        info += f"Swap:\n"
        info += f"  Used: {swap.used / (1024**3):.2f} GB / {swap.total / (1024**3):.2f} GB\n"
        info += f"  {draw_bar(swap.used, swap.total)}\n"
        
        return info
        
    def get_disk_info(self):
        """Get disk usage information"""
        info = "=== DISK USAGE ===\n\n"
        
        for partition in psutil.disk_partitions():
            if partition.fstype:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    percent = usage.percent
                    bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
                    info += f"{partition.device} ({partition.fstype})\n"
                    info += f"  Mount: {partition.mountpoint}\n"
                    info += f"  {usage.used / (1024**3):.2f} GB / {usage.total / (1024**3):.2f} GB\n"
                    info += f"  [{bar}] {percent:.1f}%\n\n"
                except:
                    pass
        
        return info
        
    def get_network_info(self):
        """Get network information"""
        info = "=== NETWORK INFORMATION ===\n\n"
        
        net_if = psutil.net_if_addrs()
        for interface, addrs in net_if.items():
            info += f"{interface}:\n"
            for addr in addrs:
                info += f"  {addr.family.name}: {addr.address}\n"
            info += "\n"
        
        # Network I/O stats
        net_io = psutil.net_io_counters()
        info += f"Network Statistics:\n"
        info += f"  Bytes Sent: {net_io.bytes_sent / (1024**3):.2f} GB\n"
        info += f"  Bytes Received: {net_io.bytes_recv / (1024**3):.2f} GB\n"
        info += f"  Packets Sent: {net_io.packets_sent:,}\n"
        info += f"  Packets Received: {net_io.packets_recv:,}\n"
        
        return info
        
    def get_process_info(self):
        """Get top processes"""
        info = "=== TOP PROCESSES ===\n\n"
        
        info += "Top 10 by Memory Usage:\n"
        try:
            procs = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), 
                          key=lambda p: p.info['memory_percent'], reverse=True)[:10]
            for p in procs:
                try:
                    info += f"  PID {p.info['pid']:>6} | {p.info['name'][:40]:<40} | {p.info['memory_percent']:>6.1f}%\n"
                except:
                    pass
        except:
            pass
        
        info += "\nTop 10 by CPU Usage:\n"
        try:
            procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                          key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:10]
            for p in procs:
                try:
                    cpu = p.info['cpu_percent'] or 0
                    info += f"  PID {p.info['pid']:>6} | {p.info['name'][:40]:<40} | {cpu:>6.1f}%\n"
                except:
                    pass
        except:
            pass
        
        return info
        
    def toggle_auto_refresh(self):
        """Toggle auto-refresh"""
        if self.auto_refresh_var.get():
            self.auto_refresh()
        
    def auto_refresh(self):
        """Auto-refresh every 5 seconds"""
        if self.auto_refresh_var.get():
            self.update_data()
            self.root.after(5000, self.auto_refresh)


def main():
    root = tk.Tk()
    app = SysInfoGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
