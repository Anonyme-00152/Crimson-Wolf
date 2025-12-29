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
    import threading
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Token Mass Dm")
Connection()

try:
    token = ChoiceToken()

    message = input(f"{INPUT} Message {red}->{reset} ")
    if not message:
        ErrorInput()

    repetitions = int(input(f"{INPUT} Repetitions {red}->{reset} ").strip())
    if not repetitions or repetitions < 0:
        ErrorNumber()

    print(f"{INFO} Sending Dm..", reset)

    def MassDm(token, channels, message):
        for channel in channels:
            for user in [x["username"] for x in channel["recipients"]]:
                try:
                    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}
                    payload = {"content": message}

                    response = requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers=headers, json=payload)
                    if response.status_code == 200:
                        print(f"{SUCCESS} Status:{red} Sent   {white}| Username:{red} {user}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed {white}| Username:{red} {user}", reset)
                except:
                    print(f"{ERROR} Status:{red} Error  {white}| Username:{red} {user}", reset)
                time.sleep(0.1)

    channel_ids = requests.get("https://discord.com/api/v9/users/@me/channels", headers={'Authorization': token}).json()
    threads   = []

    rep = 0
    for i in range(repetitions):
        rep += 1
        if not channel_ids:
            print(f"{ERROR} No Dm found!", reset)
            Continue()
            Reset()
        for channel in [channel_ids[i:i + 3] for i in range(0, len(channel_ids), 3)]:
            t = threading.Thread(target=MassDm, args=(token, channel, message))
            t.start()
            threads.append(t)
            time.sleep(0.1)
            
    for thread in threads:
        thread.join()
    
    Continue()
    Reset()

except Exception as e:
    Error(e)