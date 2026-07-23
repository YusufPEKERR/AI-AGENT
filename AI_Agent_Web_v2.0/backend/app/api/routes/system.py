from fastapi import APIRouter
import psutil
import time
import os
import sys

router = APIRouter(prefix="/api/system", tags=["system"])

START_TIME = time.time()

@router.get("/metrics")
def get_metrics():
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    # Sort top 5 processes by memory
    processes = sorted(processes, key=lambda p: p.get('memory_percent') or 0, reverse=True)[:5]
    
    uptime = int(time.time() - START_TIME)
    
    return {
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_used_mb": round(memory.used / (1024 * 1024), 1),
        "memory_total_mb": round(memory.total / (1024 * 1024), 1),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024 * 1024 * 1024), 1),
        "disk_total_gb": round(disk.total / (1024 * 1024 * 1024), 1),
        "uptime_seconds": uptime,
        "top_processes": processes,
        "python_version": sys.version.split()[0],
        "os_platform": sys.platform
    }

@router.get("/doctor")
def system_doctor():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    
    issues = []
    if cpu > 85:
        issues.append({"level": "WARNING", "msg": f"High CPU utilization detected ({cpu}%)"})
    if mem > 90:
        issues.append({"level": "CRITICAL", "msg": f"High Memory usage ({mem}%)"})
    if disk > 90:
        issues.append({"level": "WARNING", "msg": f"Low Disk space remaining ({disk}% filled)"})
        
    return {
        "status": "Healthy" if len(issues) == 0 else "Degraded",
        "score": max(100 - len(issues) * 15, 60),
        "diagnostics": issues if issues else [{"level": "INFO", "msg": "All core system modules operating at 100% efficiency."}]
    }

@router.get("/select-directory")
def select_directory():
    import subprocess
    cmd = [
        sys.executable,
        "-c",
        "import tkinter as tk; from tkinter import filedialog; root = tk.Tk(); root.withdraw(); root.attributes('-topmost', True); print(filedialog.askdirectory(title='Proje Klasorunu Secin'))"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        path = result.stdout.strip()
        return {"path": path}
    except Exception as e:
        return {"error": str(e)}
