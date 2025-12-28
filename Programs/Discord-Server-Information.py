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
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Discord Server Information")
Connection()

try:
    invite = input(f"{INPUT} Server Invitation {red}->{reset} ")
    try:
        invite_code = invite.split("/")[-1]
    except:
        invite_code = invite

    print(f"{LOADING} Retrieving Information..", reset)

    response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
    if response.status_code == 200:
        data         = response.json()
        server_info  = data.get("guild", {})
        inviter_info = data.get("inviter", {})

        type_value         = data.get("type", "None")
        code_value         = data.get("code", "None")
        expires_at         = data.get("expires_at", "None")
        max_uses           = data.get("max_uses", "None")
        uses               = data.get("uses", "None")
        server_id          = server_info.get("id", "None")
        server_name        = server_info.get("name", "None")
        channel_id         = data.get("channel", {}).get("id", "None")
        channel_name       = data.get("channel", {}).get("name", "None")
        channel_type       = data.get("channel", {}).get("type", "None")
        server_description = server_info.get("description", "None")
        server_icon        = server_info.get("icon", "None")
        server_features    = server_info.get("features", [])
        server_nsfw_level  = server_info.get("nsfw_level", "None")
        server_nsfw        = server_info.get("nsfw", "None")
        server_flags       = server_info.get("flags", "None")
        server_verif_level = server_info.get("verification_level", "None")
        server_premium_subscription_count = server_info.get("premium_subscription_count", "None")

        inviter_id           = inviter_info.get("id", "None")
        inviter_username     = inviter_info.get("username", "None")
        inviter_display_name = inviter_info.get("global_name", "None")
        inviter_avatar       = inviter_info.get("avatar", "None")
        inviter_public_flags = inviter_info.get("public_flags", "None")
        inviter_flags        = inviter_info.get("flags", "None")
        inviter_banner       = inviter_info.get("banner", "None")
        inviter_accent_color = inviter_info.get("accent_color", "None")
        inviter_banner_color = inviter_info.get("banner_color", "None")

        try:
            if type_value == 0:
                type_value = "Standard Server"
            elif type_value == 1:
                type_value = "Group Dm"
            elif type_value == 2:
                type_value = "Community Server"
            elif type_value == 3:
                type_value = "Scheduled Event"
            else:
                type_value = type_value
        except:
            type_value = "None"

        try:
            if expires_at is None and (max_uses == 0 or max_uses is None):
                invite_type = "Permanent"
            else:
                invite_type = "Temporary"
        except:
            invite_type = "Unknown"

        try:
            dt         = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            expires_at = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            expires_at = "Unlimited"

        try:
            if max_uses == 0:
                max_uses = "Unlimited"
            elif max_uses == "None":
                max_uses = "None"
        except:
            max_uses = "None"

        try:
            if uses is None:
                uses = "No permission"
        except:
            uses = "None"

        try:
            if server_icon.startswith("a_"):
                server_icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.gif"
            else:
                server_icon_url = f"https://cdn.discordapp.com/icons/{server_id}/{server_icon}.png"
        except:
            server_icon_url = "None"

        try:
            if channel_type == 0:
                channel_type = "Text Channel"
            elif channel_type == 2:
                channel_type = "Voice Channel"
            elif channel_type == 3:
                channel_type = "Category"
            elif channel_type == 4:
                channel_type = "Announcement Channel"
            elif channel_type == 5:
                channel_type = "Store Channel"
            elif channel_type == 10:
                channel_type = "News Thread"
            elif channel_type == 11:
                channel_type = "Public Thread"
            elif channel_type == 12:
                channel_type = "Private Thread"
            elif channel_type == 13:
                channel_type = "Stage Channel"
            elif channel_type == 15:
                channel_type = "Forum Channel"
            else:
                channel_type = "None"
        except:
            channel_type = "None"

    else:
        ErrorUrl()

    Scroll(f"""
 {INFO} Server Invitation                 :{red} {invite}
 {INFO} Server Type                       :{red} {type_value}
 {INFO} Server Code                       :{red} {code_value}
 {INFO} Invitation Expiration             :{red} {expires_at}
 {INFO} Invitation Max Uses               :{red} {max_uses}
 {INFO} Invitation Uses                   :{red} {uses}
 {INFO} Server Id                         :{red} {server_id}
 {INFO} Server Name                       :{red} {server_name}
 {INFO} Channel Id                        :{red} {channel_id}
 {INFO} Channel Name                      :{red} {channel_name}
 {INFO} Channel Type                      :{red} {channel_type}
 {INFO} Server Description                :{red} {server_description}
 {INFO} Server Icon Url                   :{red} {server_icon_url}
 {INFO} Server Features                   :{red} {', '.join(server_features)}
 {INFO} Server NSFW Level                 :{red} {server_nsfw_level}
 {INFO} Server NSFW                       :{red} {server_nsfw}
 {INFO} Server Flags                      :{red} {server_flags}
 {INFO} Server Verification Level         :{red} {server_verif_level}
 {INFO} Server Premium Subscription Count :{red} {server_premium_subscription_count}
 
 {INFO} Inviter Id           :{red} {inviter_id}
 {INFO} Inviter Username     :{red} {inviter_username}
 {INFO} Inviter Display Name :{red} {inviter_display_name}
 {INFO} Inviter Avatar       :{red} {inviter_avatar}
 {INFO} Inviter Public Flags :{red} {inviter_public_flags}
 {INFO} Inviter Flags        :{red} {inviter_flags}
 {INFO} Inviter Banner       :{red} {inviter_banner}
 {INFO} Inviter Accent Color :{red} {inviter_accent_color}
 {INFO} Inviter Banner Color :{red} {inviter_banner_color}
""")
    Continue()
    Reset()
    
except Exception as e:
    Error(e)