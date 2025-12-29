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

Title(f"{version_tool} Changelog")

try:
    changelog = f"""
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 {INFO} {red}New Features:
 {INFO}  - Discord Token Information
 {INFO}  - Discord Token Login
 {INFO}  - Discord Token Onliner
 {INFO}  - Discord Token Generator
 {INFO}  - Discord Token Disabler
 {INFO}  - Discord Token Bio Changer
 {INFO}  - Discord Token Alias Changer
 {INFO}  - Discord Token Status Changer
 {INFO}  - Discord Token Pfp Changer
 {INFO}  - Discord Token Language Changer
 {INFO}  - Discord Token House Changer
 {INFO}  - Discord Token Theme Changer
 {INFO}  - Discord Token Joiner
 {INFO}  - Discord Token Leaver
 {INFO}  - Discord Server Information
 {INFO}  - Discord Token Nuker
 {INFO}  - Discord Token Delete Friends
 {INFO}  - Discord Token Block Friends
 {INFO}  - Discord Token Unblock Users
 {INFO}  - Discord Token Spammer
 {INFO}  - Discord Token Mass Dm
 {INFO}  - Discord Token Delete Dm
 {INFO}  - Discord Id To Token
 {INFO}  - Discord Snowflake Decoder
 {INFO}  - Discord Bot Invite To Id
 {INFO}  - Discord Webhook Information
 {INFO}  - Discord Webhook Generator
 {INFO}  - Discord Webhook Spammer
 {INFO}  - Discord Webhook Deleter
 {INFO}  - Discord Nitro Generator

 {INFO} {red}Improvements:
 {INFO}  - Nothing for the moment!

 {INFO} {red}Bug Fixes:
 {INFO}   - No bugs!

 {INFO} {red}Removed Features:
 {INFO}  - Nothing has been removed!

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""
    Scroll(Gradient(changelog))

    Continue()
    Reset()

except Exception as e:
    Error(e)