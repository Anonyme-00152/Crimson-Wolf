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

Title("Tool Information")

try:
    Scroll(f"""
 {INFO} Tool Name :{red} {name_tool}
 {INFO} Version   :{red} {version_tool}
 {INFO} Type      :{red} {type_tool}
 {INFO} Author    :{red} {author_tool}
 {INFO} GitHub    :{red} {github_url}
 {INFO} Guns.lol  :{red} {gunslol_url}
 {INFO} License   :{red} {license}
    """)
    Continue()
    Reset()

except Exception as e:
    Error(e)