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
    import webbrowser
except Exception as e:
    MissingModule(e)

Title("Discord Bot Id To Invite")
Connection()

try:
    try:
        id_bot = input(f"{INPUT} Bot Id {red}->{reset} ")
    except:
        ErrorId()

    try:
        response = requests.get(f"https://discord.com/oauth2/authorize?client_id={id_bot}&scope=bot&permissions=8")
        print(f"{SUCCESS} Invite Link:{red} {response.url}", reset)
    except:
        ErrorId()

    browser = input(f"{INPUT} Open Browser? {YESORNO} {red}->{reset} ").lower()
    if browser in ['y', 'yes']:
        try:
            webbrowser.open_new_tab(response.url)
            print(f"{SUCCESS} Browser opened!", reset)
        except:
            print(f"{ERROR} Error while trying to open Browser!", reset)
        Continue()
        Reset()
    else:
        Continue()
        Reset()

except Exception as e:
    Error(e)