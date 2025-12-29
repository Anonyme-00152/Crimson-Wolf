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


from Programs.Plugins.Config import *
from Programs.Plugins.Utils import Title

import os
import sys

Title("Setup")

def OpenLinks():
    try:
        import webbrowser
        webbrowser.open(github_url)
        webbrowser.open(gunslol_url)
    except:
        pass

if sys.platform.startswith("win"):
    os.system("cls")
    print(f"Installing required modules for {name_tool}:")
    os.system("python -m pip install --upgrade pip")
    os.system("pip install -r requirements.txt")
    OpenLinks()
    os.system("python Buildware.py")
elif sys.platform.startswith("linux"):
    os.system("clear")
    print(f"Installing required modules for {name_tool}:")
    os.system("python3 -m pip install --upgrade pip")
    os.system("pip3 install -r requirements.txt")
    OpenLinks()
    os.system("python3 Buildware.py")