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

def collect_system_info():
    """Collect system information"""
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
