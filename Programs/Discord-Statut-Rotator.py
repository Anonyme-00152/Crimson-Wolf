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

# Advanced Discord Status Changer Pro by Colin

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import json
    import threading
    import time
    from datetime import datetime
    import random
    import asyncio
    from concurrent.futures import ThreadPoolExecutor, as_completed
except Exception as e:
    MissingModule(e)

Title("Discord Status Changer Pro")
Connection()

class DiscordStatusAPI:
    """Advanced Discord API wrapper for status manipulation"""
    
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': RandomUserAgents()
        }
        self.user_data = None
        
    def validate_token(self):
        """Validate token and fetch user data"""
        try:
            response = requests.get(
                "https://discord.com/api/v9/users/@me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.user_data = response.json()
                return True, "Token valid"
            else:
                return False, f"Invalid token (Status: {response.status_code})"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
            
    def get_user_info(self):
        """Get detailed user information"""
        if not self.user_data:
            success, message = self.validate_token()
            if not success:
                return None, message
        
        try:
            # Fetch additional user data
            response = requests.get(
                "https://discord.com/api/v9/users/@me/profile",
                headers=self.headers,
                timeout=10
            )
            
            profile_data = response.json() if response.status_code == 200 else {}
            
            user_info = {
                'id': self.user_data.get('id'),
                'username': self.user_data.get('username'),
                'discriminator': self.user_data.get('discriminator'),
                'avatar': self.user_data.get('avatar'),
                'email': self.user_data.get('email'),
                'phone': self.user_data.get('phone'),
                'premium_type': self.user_data.get('premium_type'),
                'bio': profile_data.get('bio', 'No bio'),
                'accent_color': self.user_data.get('accent_color'),
                'banner': self.user_data.get('banner'),
                'banner_color': self.user_data.get('banner_color'),
                'verified': self.user_data.get('verified', False),
                'mfa_enabled': self.user_data.get('mfa_enabled', False)
            }
            
            return user_info, "Success"
            
        except Exception as e:
            return None, f"Error fetching user info: {str(e)}"
            
    def set_status(self, status_text, emoji_name=None, emoji_id=None, expires_at=None):
        """Set custom status with advanced options"""
        payload = {
            'custom_status': {
                'text': status_text
            }
        }
        
        # Add emoji if provided
        if emoji_name:
            payload['custom_status']['emoji_name'] = emoji_name
            if emoji_id:
                payload['custom_status']['emoji_id'] = emoji_id
        
        # Add expiration if provided
        if expires_at:
            payload['custom_status']['expires_at'] = expires_at
        
        try:
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Status updated successfully"
            else:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('message', f'HTTP {response.status_code}')
                return False, f"Failed to update status: {error_msg}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
            
    def clear_status(self):
        """Clear custom status"""
        payload = {
            'custom_status': None
        }
        
        try:
            response = requests.patch(
                "https://discord.com/api/v9/users/@me/settings",
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return True, "Status cleared successfully"
            else:
                return False, f"Failed to clear status (HTTP {response.status_code})"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"
            
    def get_current_status(self):
        """Get current user status"""
        try:
            response = requests.get(
                "https://discord.com/api/v9/users/@me/settings",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                settings = response.json()
                custom_status = settings.get('custom_status')
                
                if custom_status:
                    status_info = {
                        'text': custom_status.get('text', ''),
                        'emoji': custom_status.get('emoji_name', ''),
                        'emoji_id': custom_status.get('emoji_id', ''),
                        'expires_at': custom_status.get('expires_at')
                    }
                    return True, status_info
                else:
                    return True, {'text': '', 'emoji': '', 'emoji_id': '', 'expires_at': None}
            else:
                return False, f"Failed to fetch status (HTTP {response.status_code})"
                
        except requests.exceptions.RequestException as e:
            return False, f"Connection error: {str(e)}"

class StatusManager:
    """Manage multiple status configurations"""
    
    def __init__(self):
        self.status_profiles = {}
        self.load_presets()
        
    def load_presets(self):
        """Load predefined status presets"""
        self.status_profiles = {
            'gaming': {
                'name': '🎮 Gaming',
                'statuses': [
                    'Playing Valorant',
                    'On Fortnite',
                    'Streaming CS2',
                    'AFK in Minecraft'
                ],
                'emojis': ['🎮', '⚔️', '🔫', '🏹']
            },
            'working': {
                'name': '💼 Working',
                'statuses': [
                    'Coding Python',
                    'Working on project',
                    'In a meeting',
                    'Fixing bugs'
                ],
                'emojis': ['💻', '📊', '📈', '🔧']
            },
            'music': {
                'name': '🎵 Listening',
                'statuses': [
                    'Listening to Spotify',
                    '🎶 Vibing to music',
                    'Discovering new tracks',
                    'On SoundCloud'
                ],
                'emojis': ['🎵', '🎶', '🎧', '📻']
            },
            'streaming': {
                'name': '📺 Streaming',
                'statuses': [
                    'Live on Twitch!',
                    'Streaming gameplay',
                    'Just chatting',
                    '🔴 LIVE NOW'
                ],
                'emojis': ['📺', '🔴', '🎥', '💬']
            },
            'custom': {
                'name': '⚙️ Custom',
                'statuses': [],
                'emojis': []
            }
        }
        
    def add_custom_status(self, text, emoji=''):
        """Add custom status to profile"""
        if 'custom' not in self.status_profiles:
            self.status_profiles['custom'] = {'name': 'Custom', 'statuses': [], 'emojis': []}
        
        self.status_profiles['custom']['statuses'].append(text)
        self.status_profiles['custom']['emojis'].append(emoji)
        
    def get_random_status(self, profile_key):
        """Get random status from a profile"""
        if profile_key not in self.status_profiles:
            return None, None
            
        profile = self.status_profiles[profile_key]
        
        if not profile['statuses']:
            return "No status available", ""
            
        index = random.randint(0, len(profile['statuses']) - 1)
        return profile['statuses'][index], profile['emojis'][index] if index < len(profile['emojis']) else ''

class MultiTokenStatusChanger:
    """Handle multiple tokens simultaneously"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.clients = [DiscordStatusAPI(token) for token in tokens]
        self.running = False
        
    def validate_all_tokens(self):
        """Validate all tokens"""
        results = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_token = {executor.submit(client.validate_token): i 
                              for i, client in enumerate(self.clients)}
            
            for future in as_completed(future_to_token):
                token_idx = future_to_token[future]
                try:
                    success, message = future.result()
                    results.append((token_idx, success, message))
                except Exception as e:
                    results.append((token_idx, False, str(e)))
                    
        return results
        
    def set_status_all(self, status_text, emoji_name=None):
        """Set status for all tokens"""
        if not self.running:
            print(f"{ERROR} Status changer not running", reset)
            return
            
        results = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_client = {executor.submit(client.set_status, status_text, emoji_name): i 
                              for i, client in enumerate(self.clients)}
            
            for future in as_completed(future_to_client):
                client_idx = future_to_client[future]
                try:
                    success, message = future.result()
                    results.append((client_idx, success, message))
                except Exception as e:
                    results.append((client_idx, False, str(e)))
                    
        return results
        
    def start_rotation(self, status_manager, profile_key, interval=5):
        """Start rotating statuses for all tokens"""
        self.running = True
        
        def rotation_loop():
            while self.running:
                status_text, emoji = status_manager.get_random_status(profile_key)
                if status_text:
                    results = self.set_status_all(status_text, emoji)
                    
                    # Display results
                    success_count = sum(1 for _, success, _ in results if success)
                    print(f"\r{PREFIX} Status: {red}{status_text[:30]}...{white} | "
                          f"Tokens: {red}{success_count}/{len(self.tokens)}{white} updated", 
                          end='', flush=True)
                
                time.sleep(interval)
        
        thread = threading.Thread(target=rotation_loop, daemon=True)
        thread.start()
        
    def stop_rotation(self):
        """Stop the status rotation"""
        self.running = False

def display_user_info(user_info):
    """Display user information in formatted way"""
    if not user_info:
        return
        
    header = f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║                  USER INFORMATION                       ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
"""
    
    info_display = f"""
 {PREFIX1}👤 ACCOUNT INFO{SUFFIX1}
 {SUCCESS} Username  :{red} {user_info.get('username', 'N/A')}#{user_info.get('discriminator', 'N/A')}
 {SUCCESS} User ID   :{red} {user_info.get('id', 'N/A')}
 {SUCCESS} Email     :{red} {user_info.get('email', 'N/A')}
 {SUCCESS} Bio       :{red} {user_info.get('bio', 'No bio')}
 
 {PREFIX1}🎨 PROFILE{SUFFIX1}
 {SUCCESS} Premium   :{red} {'Nitro' if user_info.get('premium_type') else 'No'}
 {SUCCESS} Verified  :{red} {'Yes' if user_info.get('verified') else 'No'}
 {SUCCESS} 2FA       :{red} {'Enabled' if user_info.get('mfa_enabled') else 'Disabled'}
 {SUCCESS} Accent    :{red} #{hex(user_info.get('accent_color', 0))[2:] if user_info.get('accent_color') else 'Default'}
"""
    
    Scroll(header + info_display)

def display_status_info(status_info):
    """Display current status information"""
    if not status_info or not status_info.get('text'):
        print(f"\n{PREFIX} {INFO} No custom status set", reset)
        return
        
    header = f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║                  CURRENT STATUS                         ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
"""
    
    status_text = status_info.get('text', '')
    emoji = status_info.get('emoji', '')
    expires_at = status_info.get('expires_at')
    
    status_display = f"""
 {PREFIX1}📝 STATUS{SUFFIX1}
 {SUCCESS} Text      :{red} {emoji} {status_text}
 {SUCCESS} Emoji ID  :{red} {status_info.get('emoji_id', 'None')}
"""
    
    if expires_at:
        try:
            expires_time = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
            time_left = expires_time - datetime.utcnow()
            
            if time_left.total_seconds() > 0:
                hours = int(time_left.total_seconds() // 3600)
                minutes = int((time_left.total_seconds() % 3600) // 60)
                status_display += f" {SUCCESS} Expires in:{red} {hours}h {minutes}m\n"
            else:
                status_display += f" {SUCCESS} Expired    :{red} Yes\n"
        except:
            status_display += f" {SUCCESS} Expires at:{red} {expires_at}\n"
    
    Scroll(header + status_display)

def create_status_presets():
    """Create and manage status presets"""
    manager = StatusManager()
    
    while True:
        Clear()
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║                  STATUS PRESETS                         ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Gaming Profile ({len(manager.status_profiles['gaming']['statuses'])} statuses)
 {PREFIX1}2{SUFFIX1} Working Profile ({len(manager.status_profiles['working']['statuses'])} statuses)
 {PREFIX1}3{SUFFIX1} Music Profile ({len(manager.status_profiles['music']['statuses'])} statuses)
 {PREFIX1}4{SUFFIX1} Streaming Profile ({len(manager.status_profiles['streaming']['statuses'])} statuses)
 {PREFIX1}5{SUFFIX1} Custom Profile ({len(manager.status_profiles['custom']['statuses'])} statuses)
 {PREFIX1}6{SUFFIX1} Add Custom Status
 {PREFIX1}7{SUFFIX1} Back to Main Menu

""")
        
        choice = input(f"{INPUT} Select profile {red}->{reset} ").strip()
        
        if choice == '1':
            return 'gaming', manager
        elif choice == '2':
            return 'working', manager
        elif choice == '3':
            return 'music', manager
        elif choice == '4':
            return 'streaming', manager
        elif choice == '5':
            return 'custom', manager
        elif choice == '6':
            print(f"\n{PREFIX} Enter custom status text:", reset)
            status_text = input(f"{INPUT} Text {red}->{reset} ")
            
            print(f"{PREFIX} Enter emoji (optional, press Enter to skip):", reset)
            emoji = input(f"{INPUT} Emoji {red}->{reset} ").strip()
            
            manager.add_custom_status(status_text, emoji)
            print(f"{SUCCESS} Custom status added!", reset)
            time.sleep(1)
        elif choice == '7':
            return None, None

def single_token_mode():
    """Single token status changer mode"""
    token = ChoiceToken()
    api = DiscordStatusAPI(token)
    
    # Validate token
    print(f"{LOADING} Validating token...", reset)
    success, message = api.validate_token()
    
    if not success:
        print(f"{ERROR} {message}", reset)
        Continue()
        return
    
    print(f"{SUCCESS} Token validated successfully!", reset)
    
    # Get user info
    user_info, info_msg = api.get_user_info()
    if user_info:
        display_user_info(user_info)
    
    # Get current status
    status_success, status_info = api.get_current_status()
    if status_success:
        display_status_info(status_info)
    
    while True:
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               SINGLE TOKEN MODE                         ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Set Custom Status
 {PREFIX1}2{SUFFIX1} Clear Status
 {PREFIX1}3{SUFFIX1} Use Status Presets
 {PREFIX1}4{SUFFIX1} Auto-Rotate Status
 {PREFIX1}5{SUFFIX1} Back to Main Menu

""")
        
        choice = input(f"{INPUT} Select option {red}->{reset} ").strip()
        
        if choice == '1':
            print(f"\n{PREFIX} Enter status text:", reset)
            status_text = input(f"{INPUT} Text {red}->{reset} ")
            
            print(f"{PREFIX} Enter emoji (optional, press Enter to skip):", reset)
            emoji = input(f"{INPUT} Emoji {red}->{reset} ").strip() or None
            
            print(f"{PREFIX} Enter expiration in minutes (optional, 0 for none):", reset)
            try:
                expire_min = int(input(f"{INPUT} Minutes {red}->{reset} ").strip() or "0")
                expires_at = None
                if expire_min > 0:
                    from datetime import datetime, timedelta
                    expires_at = (datetime.utcnow() + timedelta(minutes=expire_min)).isoformat() + 'Z'
            except:
                expires_at = None
            
            print(f"{LOADING} Setting status...", reset)
            success, message = api.set_status(status_text, emoji, None, expires_at)
            
            if success:
                print(f"{SUCCESS} {message}", reset)
            else:
                print(f"{ERROR} {message}", reset)
            
            Continue()
            
        elif choice == '2':
            print(f"{LOADING} Clearing status...", reset)
            success, message = api.clear_status()
            
            if success:
                print(f"{SUCCESS} {message}", reset)
            else:
                print(f"{ERROR} {message}", reset)
            
            Continue()
            
        elif choice == '3':
            profile_key, manager = create_status_presets()
            
            if profile_key and manager:
                status_text, emoji = manager.get_random_status(profile_key)
                
                if status_text:
                    print(f"{LOADING} Setting status: {red}{emoji} {status_text}{white}...", reset)
                    success, message = api.set_status(status_text, emoji)
                    
                    if success:
                        print(f"{SUCCESS} {message}", reset)
                    else:
                        print(f"{ERROR} {message}", reset)
                
                Continue()
            
        elif choice == '4':
            profile_key, manager = create_status_presets()
            
            if profile_key and manager:
                try:
                    print(f"\n{PREFIX} Enter rotation interval (seconds):", reset)
                    interval = int(input(f"{INPUT} Interval {red}->{reset} ").strip())
                    
                    if interval < 2:
                        print(f"{ERROR} Interval must be at least 2 seconds", reset)
                        Continue()
                        continue
                    
                    print(f"\n{INFO} Starting auto-rotation...", reset)
                    print(f"{INFO} Press Ctrl+C to stop", reset)
                    
                    rotation_count = 0
                    try:
                        while True:
                            status_text, emoji = manager.get_random_status(profile_key)
                            if status_text:
                                api.set_status(status_text, emoji)
                                rotation_count += 1
                                print(f"\r{PREFIX} Rotation #{rotation_count}: {red}{emoji} {status_text[:30]}...{white}", 
                                      end='', flush=True)
                            
                            time.sleep(interval)
                    except KeyboardInterrupt:
                        print(f"\n\n{PREFIX} Auto-rotation stopped", reset)
                        api.clear_status()
                        print(f"{SUCCESS} Status cleared", reset)
                        
                except ValueError:
                    print(f"{ERROR} Invalid interval", reset)
                
                Continue()
            
        elif choice == '5':
            break

def multi_token_mode():
    """Multiple tokens status changer mode"""
    print(f"{INFO} Select tokens for multi-token mode", reset)
    tokens = ChoiceMultiToken()
    
    if len(tokens) < 2:
        print(f"{ERROR} Select at least 2 tokens for multi-token mode", reset)
        Continue()
        return
    
    manager = MultiTokenStatusChanger(tokens)
    
    # Validate all tokens
    print(f"{LOADING} Validating {len(tokens)} tokens...", reset)
    results = manager.validate_all_tokens()
    
    valid_count = sum(1 for _, success, _ in results if success)
    print(f"{SUCCESS} {valid_count}/{len(tokens)} tokens valid", reset)
    
    if valid_count == 0:
        print(f"{ERROR} No valid tokens found", reset)
        Continue()
        return
    
    while True:
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               MULTI-TOKEN MODE                          ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Set Same Status for All Tokens
 {PREFIX1}2{SUFFIX1} Auto-Rotate Status (All Tokens)
 {PREFIX1}3{SUFFIX1} Clear All Statuses
 {PREFIX1}4{SUFFIX1} Back to Main Menu

 {INFO} Valid tokens: {red}{valid_count}/{len(tokens)}{white}
""")
        
        choice = input(f"{INPUT} Select option {red}->{reset} ").strip()
        
        if choice == '1':
            print(f"\n{PREFIX} Enter status text for all tokens:", reset)
            status_text = input(f"{INPUT} Text {red}->{reset} ")
            
            print(f"{PREFIX} Enter emoji (optional, press Enter to skip):", reset)
            emoji = input(f"{INPUT} Emoji {red}->{reset} ").strip() or None
            
            print(f"{LOADING} Setting status for {valid_count} tokens...", reset)
            
            manager.running = True
            results = manager.set_status_all(status_text, emoji)
            manager.running = False
            
            success_count = sum(1 for _, success, _ in results if success)
            print(f"{SUCCESS} {success_count}/{valid_count} tokens updated successfully", reset)
            
            Continue()
            
        elif choice == '2':
            profile_key, status_manager = create_status_presets()
            
            if profile_key and status_manager:
                try:
                    print(f"\n{PREFIX} Enter rotation interval (seconds):", reset)
                    interval = int(input(f"{INPUT} Interval {red}->{reset} ").strip())
                    
                    if interval < 5:
                        print(f"{ERROR} Interval must be at least 5 seconds for multi-token", reset)
                        Continue()
                        continue
                    
                    print(f"\n{INFO} Starting auto-rotation for {valid_count} tokens...", reset)
                    print(f"{INFO} Press Enter to stop", reset)
                    
                    manager.start_rotation(status_manager, profile_key, interval)
                    
                    # Wait for user to stop
                    input()
                    
                    manager.stop_rotation()
                    print(f"\n{PREFIX} Auto-rotation stopped", reset)
                    
                    # Clear all statuses
                    print(f"{LOADING} Clearing all statuses...", reset)
                    manager.running = True
                    manager.set_status_all("")
                    manager.running = False
                    print(f"{SUCCESS} All statuses cleared", reset)
                    
                except ValueError:
                    print(f"{ERROR} Invalid interval", reset)
                
                Continue()
            
        elif choice == '3':
            print(f"{LOADING} Clearing statuses for all tokens...", reset)
            
            manager.running = True
            results = manager.set_status_all("")
            manager.running = False
            
            success_count = sum(1 for _, success, _ in results if success)
            print(f"{SUCCESS} {success_count}/{valid_count} statuses cleared", reset)
            
            Continue()
            
        elif choice == '4':
            break

try:
    while True:
        Clear()
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               DISCORD STATUS CHANGER PRO               ║
{red}║                   v2.0 Advanced                        ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Single Token Mode
 {PREFIX1}2{SUFFIX1} Multi-Token Mode
 {PREFIX1}3{SUFFIX1} Status Presets Manager
 {PREFIX1}4{SUFFIX1} Return to Main Menu

 {INFO} Features:
   {SUCCESS}✓{white} Advanced status rotation
   {SUCCESS}✓{white} Multi-token support
   {SUCCESS}✓{white} Custom emojis
   {SUCCESS}✓{white} Status expiration
   {SUCCESS}✓{white} Preset profiles
   {SUCCESS}✓{white} Real-time updates

""")
        
        choice = input(f"{INPUT} Select mode {red}->{reset} ").strip()
        
        if choice == '1':
            single_token_mode()
        elif choice == '2':
            multi_token_mode()
        elif choice == '3':
            profile_key, manager = create_status_presets()
            if manager and profile_key:
                print(f"\n{PREFIX} Selected profile: {red}{manager.status_profiles[profile_key]['name']}{white}", reset)
                status_count = len(manager.status_profiles[profile_key]['statuses'])
                print(f"{PREFIX} Contains {red}{status_count}{white} statuses", reset)
                Continue()
        elif choice == '4':
            break
        else:
            ErrorChoice()
    
    Continue()
    Reset()

except KeyboardInterrupt:
    print(f"\n{PREFIX} {INFO} Operation cancelled by user", reset)
    Continue()
    Reset()
except Exception as e:
    Error(e)