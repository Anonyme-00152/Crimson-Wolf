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
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord Token Theme Changer")
Connection()

try:
    token = ChoiceToken()

    Scroll(f"""
 {PREFIX}01{SUFFIX} Light Theme
 {PREFIX}02{SUFFIX} Ash Theme
 {PREFIX}03{SUFFIX} Dark Theme
 {PREFIX}04{SUFFIX} Onyx Theme
""")
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip().lstrip("0")

    themes = {
        "1": "light",
        "2": "dark", 
        "3": "darker",
        "4": "midnight"
    }
    if choice in themes:
        theme = themes[choice]

        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        data    = {"theme": theme}

        print(f"{INFO} Changing Theme..", reset)

        try:
            response = requests.patch('https://discord.com/api/v9/users/@me/settings', json=data, headers=headers)
            if response.status_code == 200:
                print(f"{SUCCESS} Theme changed!", reset)
            else:
                print(f"{ERROR} Failed to change Theme!", reset)
        except:
            print(f"{ERROR} Error while trying to change Theme!", reset)
    else:
        ErrorNumber()

    Continue()
    Reset()

except Exception as e:
    Error(e)