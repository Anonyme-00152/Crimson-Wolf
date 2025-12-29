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
except Exception as e:
    MissingModule(e)

Title("Discord Token Delete Dm")
Connection()

try:
    token = ChoiceToken()

    print(f"{LOADING} Deleting Dm..", reset)

    def DeleteDm(token, channels):
        for channel in channels:
            try:
                response = requests.delete(f'https://discord.com/api/v9/channels/'+channel['id'], headers={'Authorization': token})
                if response.status_code == 204 or response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Deleted {white}| Channel Id:{red} {channel['id']}", reset)
                else:
                    print(f"{ERROR} Status {red} Failed  {white}| Channel Id:{red} {channel['id']}", reset)
            except:
                print(f"{ERROR} Status {red} Error   {white}| Channel Id:{red} {channel['id']}", reset)

    processes = []
    channel_id = requests.get("https://discord.com/api/v9/users/@me/channels", headers={'Authorization': token}).json()
    if not channel_id:
        print(f"{ERROR} No Dm found!", reset)
        Continue()
        Reset()
    
    for channel in [channel_id[:i+3] for i in range(0, len(channel_id), 3)]:
        t = threading.Thread(target=DeleteDm, args=(token, channel))
        t.start()
        processes.append(t)
    for process in processes:
        process.join()

    Continue()
    Reset()

except Exception as e:
    Error(e)