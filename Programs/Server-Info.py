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

# Advanced Discord Server Lookup Pro by Colin

from Plugins.Utils import *
from Plugins.Config import *

try:
    import requests
    import json
    from datetime import datetime
    import asyncio
    import aiohttp
    import time
    from concurrent.futures import ThreadPoolExecutor
    from PIL import Image
    import io
except Exception as e:
    MissingModule(e)

Title("Discord Server Lookup Pro")
Connection()

class DiscordInviteAPI:
    """Advanced Discord API wrapper for server information lookup"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': RandomUserAgents(),
            'Accept': 'application/json'
        }
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    def get_invite_info(self, invite_code):
        """Get detailed invite information"""
        try:
            # Clean the invite code
            invite_code = self._clean_invite_code(invite_code)
            
            if not invite_code:
                return None, "Invalid invite code format"
            
            # Make API request
            response = requests.get(
                f"https://discord.com/api/v10/invites/{invite_code}",
                headers=self.headers,
                params={'with_counts': 'true', 'with_expiration': 'true'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_invite_data(data, invite_code), None
            elif response.status_code == 404:
                return None, "Invite not found or expired"
            elif response.status_code == 403:
                return None, "Access denied - invite may be private"
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
    
    async def get_invite_info_async(self, invite_code):
        """Async version of get_invite_info"""
        try:
            invite_code = self._clean_invite_code(invite_code)
            
            if not invite_code:
                return None, "Invalid invite code format"
            
            async with self.session.get(
                f"https://discord.com/api/v10/invites/{invite_code}",
                params={'with_counts': 'true', 'with_expiration': 'true'}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    return self._parse_invite_data(data, invite_code), None
                elif response.status == 404:
                    return None, "Invite not found or expired"
                elif response.status == 403:
                    return None, "Access denied - invite may be private"
                elif response.status == 429:
                    retry_after = response.headers.get('Retry-After', 5)
                    return None, f"Rate limited. Try again in {retry_after} seconds"
                else:
                    return None, f"HTTP Error {response.status}: {response.reason}"
                    
        except asyncio.TimeoutError:
            return None, "Request timed out"
        except aiohttp.ClientError:
            return None, "Connection error"
        except json.JSONDecodeError:
            return None, "Invalid JSON response"
        except Exception as e:
            return None, f"Unexpected error: {str(e)}"
    
    def _clean_invite_code(self, invite_input):
        """Extract clean invite code from various input formats"""
        if not invite_input:
            return None
            
        # Remove whitespace
        invite_input = invite_input.strip()
        
        # Extract code from different formats
        patterns = [
            'https://discord.gg/',
            'https://discord.com/invite/',
            'discord.gg/',
            'discord.com/invite/'
        ]
        
        for pattern in patterns:
            if pattern in invite_input:
                return invite_input.split(pattern)[-1].split('?')[0]
        
        # If no pattern found, assume it's already a code
        return invite_input.split('?')[0]
    
    def _parse_invite_data(self, data, invite_code):
        """Parse and organize invite data"""
        info = {
            'invite': {},
            'server': {},
            'channel': {},
            'inviter': {},
            'metadata': {}
        }
        
        # Invite information
        info['invite']['code'] = data.get('code', invite_code)
        info['invite']['url'] = f"https://discord.gg/{info['invite']['code']}"
        info['invite']['expires_at'] = self._format_timestamp(data.get('expires_at'))
        info['invite']['created_at'] = self._format_timestamp(data.get('created_at'))
        info['invite']['uses'] = data.get('uses', 0)
        info['invite']['max_uses'] = data.get('max_uses', 0)
        info['invite']['max_age'] = data.get('max_age', 0)
        info['invite']['temporary'] = data.get('temporary', False)
        info['invite']['approximate_presence_count'] = data.get('approximate_presence_count', 0)
        info['invite']['approximate_member_count'] = data.get('approximate_member_count', 0)
        
        # Server information
        if 'guild' in data:
            guild = data['guild']
            info['server']['id'] = guild.get('id', 'N/A')
            info['server']['name'] = guild.get('name', 'N/A')
            info['server']['description'] = guild.get('description', 'No description')
            info['server']['vanity_url'] = guild.get('vanity_url_code', 'No vanity URL')
            info['server']['verification_level'] = self._get_verification_level(guild.get('verification_level', 0))
            info['server']['nsfw_level'] = self._get_nsfw_level(guild.get('nsfw_level', 0))
            info['server']['premium_tier'] = guild.get('premium_tier', 0)
            info['server']['premium_subscription_count'] = guild.get('premium_subscription_count', 0)
            info['server']['max_presences'] = guild.get('max_presences', 25000)
            info['server']['max_members'] = guild.get('max_members', 500000)
            info['server']['max_video_channel_users'] = guild.get('max_video_channel_users', 25)
            
            # Features
            info['server']['features'] = guild.get('features', [])
            info['server']['premium_features'] = self._parse_premium_features(guild.get('premium_tier', 0))
            
            # Media URLs
            info['server']['icon'] = self._get_media_url(guild.get('icon'), info['server']['id'], 'icons')
            info['server']['banner'] = self._get_media_url(guild.get('banner'), info['server']['id'], 'banners')
            info['server']['splash'] = self._get_media_url(guild.get('splash'), info['server']['id'], 'splashes')
            info['server']['discovery_splash'] = self._get_media_url(guild.get('discovery_splash'), info['server']['id'], 'discovery-splashes')
            
        # Channel information
        if 'channel' in data:
            channel = data['channel']
            info['channel']['id'] = channel.get('id', 'N/A')
            info['channel']['name'] = channel.get('name', 'N/A')
            info['channel']['type'] = self._get_channel_type(channel.get('type', 0))
            info['channel']['topic'] = channel.get('topic', 'No topic')
            info['channel']['nsfw'] = channel.get('nsfw', False)
            info['channel']['position'] = channel.get('position', 0)
            
        # Inviter information
        if 'inviter' in data:
            inviter = data['inviter']
            info['inviter']['id'] = inviter.get('id', 'N/A')
            info['inviter']['username'] = inviter.get('username', 'N/A')
            info['inviter']['discriminator'] = inviter.get('discriminator', '0000')
            info['inviter']['avatar'] = self._get_media_url(inviter.get('avatar'), info['inviter']['id'], 'avatars')
            info['inviter']['banner'] = self._get_media_url(inviter.get('banner'), info['inviter']['id'], 'banners')
            info['inviter']['accent_color'] = f"#{hex(inviter.get('accent_color', 0))[2:].zfill(6)}" if inviter.get('accent_color') else 'Default'
            info['inviter']['public_flags'] = inviter.get('public_flags', 0)
            info['inviter']['bot'] = inviter.get('bot', False)
            
        # Metadata
        info['metadata']['fetched_at'] = datetime.utcnow().isoformat()
        info['metadata']['api_version'] = 'v10'
        info['metadata']['with_counts'] = True
        
        return info
    
    def _format_timestamp(self, timestamp):
        """Format Discord timestamp to readable date"""
        if not timestamp:
            return "Never"
        
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            return timestamp
    
    def _get_verification_level(self, level):
        """Convert verification level to text"""
        levels = {
            0: "None",
            1: "Low",
            2: "Medium",
            3: "High",
            4: "Very High"
        }
        return levels.get(level, f"Unknown ({level})")
    
    def _get_nsfw_level(self, level):
        """Convert NSFW level to text"""
        levels = {
            0: "Default",
            1: "Explicit",
            2: "Safe",
            3: "Age Restricted"
        }
        return levels.get(level, f"Unknown ({level})")
    
    def _get_channel_type(self, channel_type):
        """Convert channel type to text"""
        types = {
            0: "Text Channel",
            1: "DM",
            2: "Voice Channel",
            3: "Group DM",
            4: "Category",
            5: "Announcement",
            10: "Announcement Thread",
            11: "Public Thread",
            12: "Private Thread",
            13: "Stage Voice",
            14: "Directory",
            15: "Forum"
        }
        return types.get(channel_type, f"Unknown ({channel_type})")
    
    def _parse_premium_features(self, tier):
        """Parse premium features based on tier"""
        features = []
        
        if tier >= 1:
            features.extend([
                "Animated Server Icon",
                "Custom Server Banner",
                "Increased Audio Quality",
                "Server Banner",
                "Vanity URL"
            ])
        
        if tier >= 2:
            features.extend([
                "Server Splash",
                "Increased Upload Limit (100MB)",
                "1080p 60fps Go Live Streaming"
            ])
        
        if tier >= 3:
            features.extend([
                "Animated Server Banner",
                "Custom Server Invite Background",
                "Increased Upload Limit (500MB)",
                "384kbps Audio Quality"
            ])
        
        return features if features else ["No premium features"]
    
    def _get_media_url(self, hash_id, entity_id, media_type):
        """Generate Discord media URL"""
        if not hash_id:
            return "None"
        
        extension = "gif" if hash_id.startswith("a_") else "png"
        return f"https://cdn.discordapp.com/{media_type}/{entity_id}/{hash_id}.{extension}?size=4096"

class ServerLookupManager:
    """Manager for server lookup operations"""
    
    def __init__(self):
        self.api = DiscordInviteAPI()
        self.history = []
        self.max_history = 10
    
    def lookup_server(self, invite_input):
        """Perform server lookup"""
        print(f"{LOADING} Looking up server information...", reset)
        
        info, error = self.api.get_invite_info(invite_input)
        
        if error:
            return None, error
        
        # Add to history
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'invite_code': info['invite']['code'],
            'server_name': info['server']['name'],
            'url': info['invite']['url']
        })
        
        # Keep history size limited
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
        
        return info, None
    
    async def bulk_lookup(self, invite_codes):
        """Perform bulk lookup of multiple invites"""
        results = []
        
        async with self.api as api:
            tasks = [api.get_invite_info_async(code) for code in invite_codes]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    def get_history(self):
        """Get lookup history"""
        return self.history

def display_server_info(info, error=None):
    """Display server information in formatted way"""
    if error:
        Scroll(f"""
 {ERROR} Failed to fetch server information!
 {PREFIX} Error: {red}{error}{reset}
""")
        return
    
    # Create ASCII art header
    header = f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               SERVER INFORMATION REPORT                ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
"""
    
    # Invite Information
    invite_info = f"""
 {PREFIX1}🔗 INVITE INFORMATION{SUFFIX1}
 {SUCCESS} URL        :{red} {info['invite']['url']}
 {SUCCESS} Code       :{red} {info['invite']['code']}
 {SUCCESS} Created    :{red} {info['invite']['created_at']}
 {SUCCESS} Expires    :{red} {info['invite']['expires_at']}
 {SUCCESS} Uses       :{red} {info['invite']['uses']}/{info['invite']['max_uses']}
 {SUCCESS} Max Age    :{red} {info['invite']['max_age']} seconds
 {SUCCESS} Temporary  :{red} {'Yes' if info['invite']['temporary'] else 'No'}
 {SUCCESS} Members    :{red} {info['invite']['approximate_member_count']:,}
 {SUCCESS} Online     :{red} {info['invite']['approximate_presence_count']:,}
"""
    
    # Server Information
    server_info = f"""
 {PREFIX1}🏰 SERVER INFORMATION{SUFFIX1}
 {SUCCESS} Name       :{red} {info['server']['name']}
 {SUCCESS} ID         :{red} {info['server']['id']}
 {SUCCESS} Description:{red} {info['server']['description'][:100]}{'...' if len(info['server']['description']) > 100 else ''}
 {SUCCESS} Vanity URL :{red} {info['server']['vanity_url']}
 {SUCCESS} Verification:{red} {info['server']['verification_level']}
 {SUCCESS} NSFW Level :{red} {info['server']['nsfw_level']}
 {SUCCESS} Premium Tier:{red} {info['server']['premium_tier']}
 {SUCCESS} Nitro Boosts:{red} {info['server']['premium_subscription_count']:,}
 {SUCCESS} Max Members:{red} {info['server']['max_members']:,}
"""
    
    # Media URLs
    media_info = f"""
 {PREFIX1}🖼️ MEDIA{SUFFIX1}
 {SUCCESS} Icon       :{red} {info['server']['icon']}
 {SUCCESS} Banner     :{red} {info['server']['banner']}
 {SUCCESS} Splash     :{red} {info['server']['splash']}
 {SUCCESS} Discovery  :{red} {info['server']['discovery_splash']}
"""
    
    # Features
    features_text = ""
    if info['server']['features']:
        features_text = f"""
 {PREFIX1}⚙️ SERVER FEATURES{SUFFIX1}
"""
        for feature in info['server']['features']:
            features_text += f" {SUCCESS} •{red} {feature.replace('_', ' ').title()}{white}\n"
    
    # Premium Features
    premium_features_text = ""
    if info['server']['premium_features']:
        premium_features_text = f"""
 {PREFIX1}💎 PREMIUM FEATURES{SUFFIX1}
"""
        for feature in info['server']['premium_features']:
            premium_features_text += f" {SUCCESS} •{red} {feature}{white}\n"
    
    # Channel Information
    channel_info = f"""
 {PREFIX1}📝 CHANNEL INFORMATION{SUFFIX1}
 {SUCCESS} Name       :{red} {info['channel']['name']}
 {SUCCESS} ID         :{red} {info['channel']['id']}
 {SUCCESS} Type       :{red} {info['channel']['type']}
 {SUCCESS} Topic      :{red} {info['channel']['topic'][:80]}{'...' if len(info['channel']['topic']) > 80 else ''}
 {SUCCESS} Position   :{red} {info['channel']['position']}
 {SUCCESS} NSFW       :{red} {'Yes' if info['channel']['nsfw'] else 'No'}
"""
    
    # Inviter Information
    inviter_info = ""
    if info['inviter'].get('id') != 'N/A':
        inviter_info = f"""
 {PREFIX1}👤 INVITER INFORMATION{SUFFIX1}
 {SUCCESS} Username   :{red} {info['inviter']['username']}#{info['inviter']['discriminator']}
 {SUCCESS} ID         :{red} {info['inviter']['id']}
 {SUCCESS} Avatar     :{red} {info['inviter']['avatar']}
 {SUCCESS} Banner     :{red} {info['inviter']['banner']}
 {SUCCESS} Accent Color:{red} {info['inviter']['accent_color']}
 {SUCCESS} Is Bot     :{red} {'Yes' if info['inviter']['bot'] else 'No'}
 {SUCCESS} Public Flags:{red} {info['inviter']['public_flags']}
"""
    
    # Combine all sections
    full_display = header + invite_info + server_info
    
    if info['server']['icon'] != 'None' or info['server']['banner'] != 'None':
        full_display += media_info
    
    if info['server']['features']:
        full_display += features_text
    
    if info['server']['premium_features']:
        full_display += premium_features_text
    
    full_display += channel_info
    
    if inviter_info:
        full_display += inviter_info
    
    Scroll(full_display)

def bulk_lookup_mode():
    """Bulk lookup multiple invites"""
    manager = ServerLookupManager()
    
    print(f"{PREFIX} Enter invite codes/URLs (one per line, type 'DONE' when finished):", reset)
    
    invite_codes = []
    while True:
        code = input(f"{INPUT} Code/URL {red}->{reset} ").strip()
        
        if code.upper() == 'DONE':
            break
        
        if code:
            invite_codes.append(code)
    
    if not invite_codes:
        print(f"{ERROR} No invites provided", reset)
        Continue()
        return
    
    print(f"\n{LOADING} Looking up {len(invite_codes)} invites...", reset)
    
    async def run_bulk_lookup():
        return await manager.bulk_lookup(invite_codes)
    
    results = asyncio.run(run_bulk_lookup())
    
    success_count = 0
    failed_count = 0
    
    for i, result in enumerate(results):
        if isinstance(result, tuple):
            info, error = result
            if info:
                success_count += 1
                print(f"\n{PREFIX} {SUCCESS} {invite_codes[i]}: Found - {info['server']['name']}", reset)
            else:
                failed_count += 1
                print(f"\n{PREFIX} {ERROR} {invite_codes[i]}: {error}", reset)
        else:
            failed_count += 1
            print(f"\n{PREFIX} {ERROR} {invite_codes[i]}: Error processing", reset)
    
    print(f"\n{PREFIX} Summary: {red}{success_count}{white} successful, {red}{failed_count}{white} failed", reset)

def history_mode():
    """View lookup history"""
    manager = ServerLookupManager()
    history = manager.get_history()
    
    if not history:
        print(f"{INFO} No lookup history available", reset)
        Continue()
        return
    
    Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║                 LOOKUP HISTORY                         ║
{red}╚══════════════════════════════════════════════════════════╝{reset}
""")
    
    for i, entry in enumerate(reversed(history), 1):
        timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M")
        print(f" {PREFIX1}{i:02d}{SUFFIX1} {timestamp} | {red}{entry['server_name']}{white}")
        print(f"      {SUCCESS}Code:{red} {entry['invite_code']}{white}")
        print(f"      {SUCCESS}URL: {red}{entry['url']}{white}")
        print()

def main_lookup_mode():
    """Main server lookup mode"""
    manager = ServerLookupManager()
    
    while True:
        print(f"\n{PREFIX} Enter Discord invite code or URL:", reset)
        print(f" {INFO} Examples: {red}discord.gg/code{white}, {red}https://discord.gg/code{white}, {red}code{white}")
        
        invite_input = input(f"{INPUT} Invite {red}->{reset} ").strip()
        
        if not invite_input:
            print(f"{ERROR} Please enter an invite code or URL", reset)
            Continue()
            continue
        
        info, error = manager.lookup_server(invite_input)
        
        display_server_info(info, error)
        
        if info:
            # Additional actions
            print(f"\n{PREFIX} {INFO} Additional actions:", reset)
            print(f"  {PREFIX1}1{SUFFIX1} Copy invite URL")
            print(f"  {PREFIX1}2{SUFFIX1} Save to file")
            print(f"  {PREFIX1}3{SUFFIX1} Check another server")
            print(f"  {PREFIX1}4{SUFFIX1} Return to menu")
            
            action = input(f"\n{PREFIX} Select action (1-4): ").strip()
            
            if action == '2':
                try:
                    filename = f"server_info_{info['invite']['code']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(info, f, indent=2, ensure_ascii=False, default=str)
                    print(f"{SUCCESS} Information saved to {red}{filename}{white}", reset)
                    time.sleep(1)
                except Exception as e:
                    print(f"{ERROR} Failed to save file: {str(e)}", reset)
                    time.sleep(1)
            elif action == '4':
                break
        else:
            print(f"\n{PREFIX} {INFO} Try again? (y/n): ", end='')
            if input().strip().lower() != 'y':
                break

try:
    while True:
        Clear()
        Scroll(f"""
{red}╔══════════════════════════════════════════════════════════╗
{red}║               DISCORD SERVER LOOKUP PRO               ║
{red}║                   v2.0 Advanced                        ║
{red}╚══════════════════════════════════════════════════════════╝{reset}

 {PREFIX1}1{SUFFIX1} Server Lookup
 {PREFIX1}2{SUFFIX1} Bulk Lookup
 {PREFIX1}3{SUFFIX1} View History
 {PREFIX1}4{SUFFIX1} Return to Main Menu

 {INFO} Features:
   {SUCCESS}✓{white} Detailed server information
   {SUCCESS}✓{white} Bulk invite checking
   {SUCCESS}✓{white} Lookup history
   {SUCCESS}✓{white} Media URL generation
   {SUCCESS}✓{white} Premium features detection
   {SUCCESS}✓{white} Error handling & rate limit protection

""")
        
        choice = input(f"{INPUT} Select mode {red}->{reset} ").strip()
        
        if choice == '1':
            main_lookup_mode()
        elif choice == '2':
            bulk_lookup_mode()
            Continue()
        elif choice == '3':
            history_mode()
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