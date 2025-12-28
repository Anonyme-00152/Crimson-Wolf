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

Title("Discord Token Custom Status Changer")
Connection()

try:
    token = ChoiceToken()

    new_status = input(f"{INPUT} Custom Status {red}->{reset} ")
    custom     = {"custom_status": {"text": new_status}}
    headers    = {'Authorization': token, 'Content-Type': 'application/json'}

    print(f"{LOADING} Changing Status..", reset)

    try:
        response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=custom)
        if response.status_code == 200:
            print(f"{SUCCESS} Status changed!", reset)
        else:
            print(f"{ERROR} Failed to change Status!", reset)
    except:
        print(f"{ERROR} Error while trying to change Status!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)