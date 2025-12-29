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
    import os
    import subprocess
except Exception as e:
    MissingModule(e)

Title("Tokens File")

try:
    file_path = os.path.join(tool_path, "Programs", "Extras", "DiscordTokens.txt")

    print(f"{INFO} Each token must be on a separate line", reset)
    print(f'{LOADING} Opening {red}"{white}DiscordTokens.txt{red}"{white}..', reset)

    try:
        if platform_pc == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(['xdg-open', file_path])
        print(f"{SUCCESS} File opened!", reset)
    except:
        print(f"{ERROR} Error while trying to open file!", reset)
        print(f"{INFO} Path:{red} {file_path}{reset}", reset)

    Continue()
    Reset()

except Exception as e:
    Error(e)