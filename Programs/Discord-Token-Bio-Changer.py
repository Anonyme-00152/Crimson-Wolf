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

Title("Discord Token Bio Changer")
Connection()

try:
    token   = ChoiceToken()
    new_bio = input(f"{INPUT} Bio {red}->{reset} ").strip()

    print(f"{LOADING} Changing Bio..", reset)

    def ChangeBio(token, new_bio):
        url = "https://discord.com/api/v9/users/@me/profile"

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": RandomUserAgents()
        }

        payload = {
            "bio": new_bio
        }

        try:
            response = requests.patch(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f"{SUCCESS} Bio changed!", reset)
                return response.json()
            else:
                print(f"{ERROR} Failed to change Bio!", reset)
                return None
        except:
            print(f"{ERROR} Error while trying to change Bio!", reset)
            return None

    ChangeBio(token, new_bio)
    Continue()
    Reset()

except Exception as e:
    Error(e)