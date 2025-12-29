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

# Improved Webhook Information Script by Colin

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import json
    from datetime import datetime
except Exception as e:
    MissingModule(e)

Title("Discord Webhook Information Pro")
Connection()

def format_timestamp(timestamp):
    """Format Discord timestamp to readable date"""
    try:
        if timestamp:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except:
        pass
    return "Unknown"

def get_webhook_details(webhook_url):
    """Fetch and parse webhook information with better error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"{INFO} Fetching webhook information...", reset)
        
        response = requests.get(webhook_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "Webhook not found (404)"
        elif response.status_code == 403:
            return None, "Access denied (403)"
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After', 5)
            return None, f"Rate limited. Try again in {retry_after} seconds"
        else:
            return None, f"HTTP Error {response.status_code}: {response.reason}"
            
    except requests.exceptions.Timeout:
        return None, "Request timed out"
    except requests.exceptions.ConnectionError:
        return None, "Connection error"
    except json.JSONDecodeError:
        return None, "Invalid JSON response"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def parse_webhook_data(data, webhook_url):
    """Parse and organize webhook data with comprehensive information"""
    info = {}
    
    # Basic information with fallbacks
    info['url'] = webhook_url
    info['id'] = data.get('id', 'N/A')
    info['name'] = data.get('name', 'N/A')
    info['token'] = webhook_url.split('/')[-1] if '/' in webhook_url else 'N/A'
    
    # Avatar information
    avatar_hash = data.get('avatar')
    if avatar_hash and info['id'] != 'N/A':
        info['avatar_hash'] = avatar_hash
        info['avatar_url'] = f"https://cdn.discordapp.com/avatars/{info['id']}/{avatar_hash}.png?size=4096"
        info['avatar_url_webp'] = f"https://cdn.discordapp.com/avatars/{info['id']}/{avatar_hash}.webp?size=4096"
    else:
        info['avatar_hash'] = 'None'
        info['avatar_url'] = 'Default Avatar'
        info['avatar_url_webp'] = 'Default Avatar'
    
    # Server and channel information
    info['guild_id'] = data.get('guild_id', 'N/A')
    info['channel_id'] = data.get('channel_id', 'N/A')
    info['application_id'] = data.get('application_id', 'N/A')
    
    # Webhook type with detailed description
    webhook_type = data.get('type', 0)
    type_map = {
        1: ("Incoming Webhook", "Can post messages to a specific channel"),
        2: ("Channel Follower Webhook", "Can follow and crosspost messages"),
        3: ("Application Webhook", "Created by an application/bot")
    }
    
    if webhook_type in type_map:
        info['type'] = type_map[webhook_type][0]
        info['type_description'] = type_map[webhook_type][1]
    else:
        info['type'] = f"Unknown ({webhook_type})"
        info['type_description'] = "Unknown webhook type"
    
    # Creator information
    if 'user' in data:
        user = data['user']
        info['creator_username'] = user.get('username', 'N/A')
        info['creator_discriminator'] = user.get('discriminator', 'N/A')
        info['creator_id'] = user.get('id', 'N/A')
        info['creator_avatar'] = user.get('avatar', 'None')
        info['creator_bot'] = "Yes" if user.get('bot', False) else "No"
    else:
        info['creator_username'] = 'N/A'
        info['creator_discriminator'] = 'N/A'
        info['creator_id'] = 'N/A'
        info['creator_avatar'] = 'None'
        info['creator_bot'] = 'N/A'
    
    # Additional metadata
    info['created_at'] = format_timestamp(data.get('created_at'))
    
    # Webhook permissions (if available)
    if 'permissions' in data:
        info['permissions'] = hex(data['permissions'])
    else:
        info['permissions'] = 'N/A'
    
    # Source information
    if 'source_guild' in data:
        info['source_guild_name'] = data['source_guild'].get('name', 'N/A')
        info['source_guild_icon'] = data['source_guild'].get('icon', 'N/A')
    else:
        info['source_guild_name'] = 'N/A'
        info['source_guild_icon'] = 'N/A'
    
    return info

def display_webhook_info(info, error=None):
    """Display webhook information in a formatted way"""
    if error:
        Scroll(f"""
 {ERROR} Failed to fetch webhook information!
 {PREFIX} Error: {red}{error}{reset}
""")
        return
    
    # Create ASCII art header
    header = f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               WEBHOOK INFORMATION REPORT               ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
"""
    
    # Basic information section
    basic_info = f"""
 {PREFIX1}🔗 BASIC INFORMATION{SUFFIX1}
 {SUCCESS} URL        :{red} {info['url']}
 {SUCCESS} ID         :{red} {info['id']}
 {SUCCESS} Name       :{red} {info['name']}
 {SUCCESS} Token      :{red} {info['token']}
 {SUCCESS} Created    :{red} {info['created_at']}
"""
    
    # Type and permissions section
    type_info = f"""
 {PREFIX1}📊 TYPE & PERMISSIONS{SUFFIX1}
 {SUCCESS} Type       :{red} {info['type']}
 {SUCCESS} Description:{red} {info['type_description']}
 {SUCCESS} App ID     :{red} {info['application_id']}
 {SUCCESS} Permissions:{red} {info['permissions']}
"""
    
    # Location information
    location_info = f"""
 {PREFIX1}📍 LOCATION{SUFFIX1}
 {SUCCESS} Guild ID   :{red} {info['guild_id']}
 {SUCCESS} Channel ID :{red} {info['channel_id']}
 {SUCCESS} Source Guild:{red} {info['source_guild_name']}
"""
    
    # Creator information
    creator_info = f"""
 {PREFIX1}👤 CREATOR{SUFFIX1}
 {SUCCESS} Username   :{red} {info['creator_username']}#{info['creator_discriminator']}
 {SUCCESS} User ID    :{red} {info['creator_id']}
 {SUCCESS} Is Bot     :{red} {info['creator_bot']}
 {SUCCESS} Avatar Hash:{red} {info['creator_avatar']}
"""
    
    # Avatar information
    avatar_info = f"""
 {PREFIX1}🖼️ AVATAR{SUFFIX1}
 {SUCCESS} Avatar Hash:{red} {info['avatar_hash']}
 {SUCCESS} PNG URL    :{red} {info['avatar_url']}
 {SUCCESS} WebP URL   :{red} {info['avatar_url_webp']}
"""
    
    # Combine all sections
    full_display = header + basic_info + type_info + location_info + creator_info + avatar_info
    
    Scroll(full_display)

try:
    # Get webhook URL with validation
    while True:
        webhook = ChoiceWebhook()
        
        if not webhook.startswith('https://discord.com/api/webhooks/'):
            print(f"{PREFIX} {PREFIX} URL doesn't look like a Discord webhook. Continue anyway? (y/n): ", end='')
            choice = input().strip().lower()
            if choice != 'y':
                continue
        
        # Fetch and parse data
        data, error = get_webhook_details(webhook)
        
        if error:
            print(f"{PREFIX} {ERROR} {error}", reset)
            print(f"{PREFIX} {INFO} Try again? (y/n): ", end='')
            if input().strip().lower() == 'y':
                continue
            else:
                break
        
        # Parse and display information
        info = parse_webhook_data(data, webhook)
        display_webhook_info(info)
        
        # Additional actions
        print(f"\n{PREFIX} {INFO} Additional actions:", reset)
        print(f"  {PREFIX1}1{SUFFIX1} Test webhook (send test message)")
        print(f"  {PREFIX1}2{SUFFIX1} Copy webhook URL")
        print(f"  {PREFIX1}3{SUFFIX1} Check another webhook")
        print(f"  {PREFIX1}4{SUFFIX1} Return to menu")
        
        action = input(f"\n{PREFIX} Select action (1-4): ").strip()
        
        if action == '1':
            # Test webhook functionality
            test_payload = {
                "content": f"Webhook test from {name_tool} - {datetime.now().strftime('%H:%M:%S')}",
                "username": "Webhook Tester"
            }
            
            try:
                test_response = requests.post(webhook, json=test_payload, timeout=5)
                if test_response.status_code == 204:
                    print(f"{PREFIX} {SUCCESS} Test message sent successfully!", reset)
                else:
                    print(f"{PREFIX} {PREFIX} Test failed: {test_response.status_code}", reset)
                time.sleep(1)
            except Exception as e:
                print(f"{PREFIX} {ERROR} Test failed: {str(e)}", reset)
                time.sleep(1)
                
        elif action == '3':
            continue  # Check another webhook
        elif action == '4':
            break  # Return to menu
        else:
            break  # Default to return
    
    Continue()
    Reset()

except KeyboardInterrupt:
    print(f"\n{PREFIX} {INFO} Operation cancelled by user", reset)
    Continue()
    Reset()
except Exception as e:
    Error(e)