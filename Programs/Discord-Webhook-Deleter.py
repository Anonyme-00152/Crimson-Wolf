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

Title("Discord Webhook Deleter")
Connection()

try:
    webhook = ChoiceWebhook()

    print(f"{INFO} Deleting Webhook..", reset)

    try:
        response = requests.delete(webhook)
        if response.status_code == 204:
            print(f"{SUCCESS} Webhook deleted!", reset)
        else:
            print(f"{ERROR} Failed to delete Webhook!", reset)
    except:
        print(f"{ERROR} Error while trying to delete the Webhook!", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)