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

Title("Discord Token Joiner")
Connection()

try:
    token = ChoiceToken()
    invite_code = input(f"{INPUT} Server Invitation {red}->{reset} ").split("/")[-1]

    print(f"{LOADING} Joining the Server..", reset)

    try:
        response = requests.post(f"https://discord.com/api/v9/invites/{invite_code}", headers={'Authorization': token})

        if response.status_code == 200:
            print(f"{SUCCESS} Token joined the Server!", reset)
        else:
            print(f"{ERROR} Failed to join the Server!", reset)
    except:
        print(f"{ERROR} Error while trying to join the Server!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)