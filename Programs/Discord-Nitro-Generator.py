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
    import string
    import random
    import threading
    import json
except Exception as e:
    MissingModule(e)

Title("Discord Nitro Generator")
Connection()

try:
    webhook = ChoiceWebhook()

    try:
        threads_number = int(input(f"{INPUT} Threads Number {red}->{reset} ").strip())
    except:
        ErrorNumber()

    print(f"{LOADING} Generate Nitro Codes..", reset)

    def SendWebhook(embed_content):
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }
        headers = {'Content-Type': 'application/json'}

        requests.post(webhook, data=json.dumps(payload), headers=headers)

    def NitroCheck():
        try:
            code =  ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
            url  = f'https://discord.gift/{code}'

            response = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true', timeout=1)
            if response.status_code == 200:
                embed_content = {
                    "title": "Nitro found!",
                    "description": f"**Nitro Code:**\n```{url}```",
                    "color": color_embed,
                    "footer": {
                        "text": username_webhook,
                        "icon_url": avatar_webhook
                    }
                }
                SendWebhook(embed_content)
                print(f"{SUCCESS} Status:{red} Valid   {white}| Nitro:{red} {url}", reset)
            else:
                print(f"{ERROR} Status:{red} Invalid {white}| Nitro:{red} {url}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Nitro:{red} {url}", reset)

    def Request():
        threads = []
        try:
            for _ in range(threads_number):
                t = threading.Thread(target=NitroCheck)
                t.start()
                threads.append(t)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while True:
        Request()

except Exception as e:
    Error(e)