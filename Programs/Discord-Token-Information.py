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
    from datetime import datetime, timezone
except Exception as e:
    MissingModule(e)

Title("Discord Token Information")
Connection()

try:
    token = ChoiceToken()
    
    print(f"{LOADING} Retrieving Information..", reset)

    api      = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token}).json()
    response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})

    if response.status_code == 200:
        status = "Valid"
    else:
        status = "Invalid"

    username          = api.get('username')
    display_name      = api.get('global_name')
    user_id           = api.get('id')
    country           = api.get('locale')
    email             = api.get('email')
    email_verified    = api.get('verified')
    phone             = api.get('phone')
    
    try:
        linked_users_raw = api.get('linked_users')
        if linked_users_raw and len(linked_users_raw) > 0:
            linked_users = ', '.join([str(user) for user in linked_users_raw])
        else:
            linked_users = "None"
    except:
        linked_users = "None"
    
    avatar_decoration = api.get('avatar_decoration')
    avatar            = api.get('avatar')   
    accent_color      = api.get('accent_color')
    banner            = api.get('banner')  
    banner_color      = api.get('banner_color')
    flags             = api.get('flags')
    public_flags      = api.get('public_flags')
    nsfw_allowed      = api.get('nsfw_allowed')
    mfa_enabled       = api.get('mfa_enabled')
    
    try:
        mfa_type_raw = api.get('authenticator_types')
        if mfa_type_raw and len(mfa_type_raw) > 0:
            mfa_types = []
            for mfa in mfa_type_raw:
                if mfa == 1:
                    mfa_types.append('SMS')
                elif mfa == 2:
                    mfa_types.append('App')
                elif mfa == 3:
                    mfa_types.append('WebAuthn')
                else:
                    mfa_types.append(f'Other ({mfa})')
            mfa_type = ', '.join(mfa_types)
        else:
            mfa_type = "None"
    except:
        mfa_type = "None"
    
    bio = api.get('bio')

    try:
        created_at_raw = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000, timezone.utc)
        created_at = created_at_raw.strftime('%Y-%m-%d %H:%M:%S')
    except:
        created_at = "None"

    try:
        premium_type = api.get('premium_type')
        if premium_type == 0:
            nitro_type = "No Nitro"
        elif premium_type == 1:
            nitro_type = "Nitro Classic"
        elif premium_type == 2:
            nitro_type = "Nitro Boost"
        else:
            nitro_type = "No Nitro"
    except:
        nitro_type = "No Nitro"

    try:
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
    except:
        avatar_url = "No Avatar"

    try:
        billing = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': token}).json()
        if billing:
            payment_methods = []

            for method in billing:
                if method['type'] == 1:
                    payment_methods.append('Credit Card')
                elif method['type'] == 2:
                    payment_methods.append('PayPal')
                else:
                    payment_methods.append('Other')
            payment_methods = ', '.join(payment_methods)
        else:
            payment_methods = 'No Payment Methods'
    except:
        payment_methods = 'No Payment Methods'

    try:
        gift_codes = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': token}).json()
        if gift_codes:
            codes = []
            for gift in gift_codes:
                gift_name = gift.get['promotion']['outbound_title']
                gift_code = gift.get['code']
                msg_gift = f"Gift: {gift_name}\nCode: {gift_code}"
                if len(gift) > 0:
                    gift = '\n\n'.join(gift) + len()
            else:
                gift = 'No Gift Codes'
        else:
            gift = 'No Gift Codes'
    except:
        gift = 'No Gift Codes'

    try:
        response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': token})
        if response.status_code == 200:
            guilds = response.json()
            try:
                guild_count = len(guilds)
            except:
                guild_count = 'None'
            try:
                owner_guilds       = [guild for guild in guilds if guild.get('owner')]
                owner_guilds_count = len(owner_guilds)
                if owner_guilds:
                    owner_guilds_list = []
                    for guild in owner_guilds:
                        owner_guilds_list.append(f"{guild.get('name')} {red}({white}{guild.get('id')}{red})")
                    owner_guilds_names = '\n' + ', '.join(owner_guilds_list)
                else:
                    owner_guilds_names = ''
            except:
                owner_guilds_count = 'None'
                owner_guilds_names = ''
    except:
        guild_count        = 'None'
        owner_guilds_count = 'None'
        owner_guilds_names = ''
        owner_guilds_names = 'None'

    try:
        response = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': token}).json()
        if response:
            friends_list = []
            for friend in response:
                try:
                    if friend.get('type') != 1:
                        continue
                    
                    user_data = friend.get('user', {})
                    username = user_data.get('username', 'Unknown')
                    user_id_friend = user_data.get('id', 'Unknown')
                    friends_names = f"{username} {red}({white}{user_id_friend}{red})"
                    
                    if len('\n'.join(friends_list)) + len(friends_names) >= 1024:
                        continue
                    
                    friends_list.append(friends_names)
                except:
                    continue

            if len(friends_list) > 0:
                friends_count = len(friends_list)
                friends = f"{friends_count}\n" + ', '.join(friends_list)
            else:
                friends = 'None'
        else:
            friends = 'None'
    except:
        friends = 'None'

    Scroll(f"""
 {INFO} Status            :{red} {status}
 {INFO} Token             :{red} {token}
 {INFO} Username          :{red} {username}
 {INFO} Display Name      :{red} {display_name}
 {INFO} User Id           :{red} {user_id}
 {INFO} Created At        :{red} {created_at}
 {INFO} Country           :{red} {country}
 {INFO} Email             :{red} {email}
 {INFO} Email Verified    :{red} {email_verified}
 {INFO} Phone             :{red} {phone}
 {INFO} Nitro             :{red} {nitro_type}
 {INFO} Linked Users      :{red} {linked_users}
 {INFO} Avatar Decoration :{red} {avatar_decoration}
 {INFO} Avatar            :{red} {avatar}
 {INFO} Avatar Url        :{red} {avatar_url}
 {INFO} Accent Color      :{red} {accent_color}
 {INFO} Banner            :{red} {banner}
 {INFO} Banner Color      :{red} {banner_color}
 {INFO} Flags             :{red} {flags}
 {INFO} Public Flags      :{red} {public_flags}
 {INFO} NSFW Allowed      :{red} {nsfw_allowed}
 {INFO} MFA Enabled       :{red} {mfa_enabled}
 {INFO} MFA Type          :{red} {mfa_type}
 {INFO} Billing           :{red} {payment_methods}
 {INFO} Gift Codes        :{red} {gift}
 {INFO} Guilds            :{red} {guild_count}
 {INFO} Owner Guilds      :{red} {owner_guilds_count}{owner_guilds_names}
 {INFO} Bio               :{red} {bio}
 {INFO} Friends           :{red} {friends}{reset}
""")
    Continue()
    Reset()

except Exception as e:
    Error(e)
    
    
# # Copyright (c) 2025 v4lkyr0/v4lkyr_
# # See LICENSE file for details

# from Plugins.Utils import *
# from Plugins.Config import *

# try:
#     import requests
#     import json
#     import time
#     import threading
#     import concurrent.futures
#     from datetime import datetime, timezone
#     import hashlib
#     import base64
# except Exception as e:
#     MissingModule(e)

# Title("Discord Token Intelligence Suite")
# Connection()

# class DiscordTokenAnalyzer:
#     def __init__(self, token):
#         self.token = token
#         self.session = requests.Session()
#         self.session.headers.update({
#             'Authorization': token,
#             'Content-Type': 'application/json',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
#         })
#         self.results = {}
#         self.errors = {}
    
#     def check_token_validity(self):
#         """Check if token is valid and get basic info"""
#         endpoints = [
#             'https://discord.com/api/v10/users/@me',
#             'https://discord.com/api/v9/users/@me',
#             'https://discord.com/api/v8/users/@me'
#         ]
        
#         for endpoint in endpoints:
#             try:
#                 response = self.session.get(endpoint, timeout=10)
                
#                 if response.status_code == 200:
#                     self.results['basic_info'] = response.json()
#                     self.results['token_status'] = 'VALID'
#                     self.results['api_version'] = endpoint.split('/')[-2]
#                     return True
#                 elif response.status_code == 401:
#                     self.results['token_status'] = 'INVALID/UNAUTHORIZED'
#                     return False
#                 elif response.status_code == 403:
#                     self.results['token_status'] = 'FORBIDDEN (LOCKED/FLAGGED)'
#                     return False
#                 elif response.status_code == 429:
#                     # Rate limited, try next endpoint
#                     continue
#             except Exception as e:
#                 self.errors[f'basic_check_{endpoint}'] = str(e)
#                 continue
        
#         self.results['token_status'] = 'UNKNOWN/ERROR'
#         return False
    
#     def analyze_token_structure(self):
#         """Analyze token format and type - ADDED THIS MISSING METHOD"""
#         token = self.token
        
#         # Bot vs User token detection
#         if token.startswith('Bot '):
#             token_type = 'Bot Token'
#             raw_token = token[4:]
#         elif token.startswith('Bearer '):
#             token_type = 'OAuth2 Bearer Token'
#             raw_token = token[7:]
#         else:
#             token_type = 'User Token'
#             raw_token = token
        
#         # Token length analysis
#         token_length = len(raw_token)
        
#         # Common token patterns
#         if token_length == 59:
#             token_format = 'Standard (59 chars)'
#         elif token_length == 70:
#             token_format = 'Extended (70 chars)'
#         else:
#             token_format = f'Unusual ({token_length} chars)'
        
#         # Try to decode parts
#         try:
#             parts = raw_token.split('.')
#             if len(parts) >= 2:
#                 try:
#                     # Try to decode first part
#                     part1_decoded = base64.b64decode(parts[0] + '==').decode('utf-8', errors='ignore')
#                 except:
#                     part1_decoded = 'Not decodable'
                
#                 # Second part
#                 try:
#                     part2_decoded = base64.b64decode(parts[1] + '==').decode('utf-8', errors='ignore')
#                 except:
#                     part2_decoded = 'Not decodable'
                
#                 token_parts = {
#                     'part1': part1_decoded[:50],
#                     'part2': part2_decoded[:50],
#                     'part_count': len(parts)
#                 }
#             else:
#                 token_parts = {'error': 'Not enough parts'}
#         except:
#             token_parts = {'error': 'Decoding failed'}
        
#         # Hash for comparison
#         token_hash = hashlib.sha256(raw_token.encode()).hexdigest()[:16]
        
#         self.results['token_analysis'] = {
#             'type': token_type,
#             'format': token_format,
#             'length': token_length,
#             'raw_length': len(self.token),
#             'parts': token_parts,
#             'hash': token_hash,
#             'first_10': raw_token[:10] + '...',
#             'last_10': '...' + raw_token[-10:] if len(raw_token) > 20 else raw_token
#         }
        
#         return True
    
#     def fetch_parallel_data(self):
#         """Fetch multiple data points in parallel"""
#         endpoints = {
#             'guilds': 'https://discord.com/api/v9/users/@me/guilds?with_counts=true',
#             'connections': 'https://discord.com/api/v9/users/@me/connections',
#             'relationships': 'https://discord.com/api/v9/users/@me/relationships',
#             'billing': 'https://discord.com/api/v9/users/@me/billing/payment-sources',
#             'subscriptions': 'https://discord.com/api/v9/users/@me/billing/subscriptions',
#             'entitlements': 'https://discord.com/api/v9/users/@me/entitlements',
#             'promotions': 'https://discord.com/api/v9/users/@me/outbound-promotions/codes',
#             'applications': 'https://discord.com/api/v9/users/@me/applications',
#             'activities': 'https://discord.com/api/v9/users/@me/activities/statistics/applications',
#             'notes': 'https://discord.com/api/v9/users/@me/notes'
#         }
        
#         def fetch_endpoint(name, url):
#             try:
#                 response = self.session.get(url, timeout=15)
#                 if response.status_code == 200:
#                     return name, response.json(), None
#                 elif response.status_code == 403:
#                     return name, None, 'Forbidden (no permission)'
#                 elif response.status_code == 404:
#                     return name, None, 'Not found'
#                 elif response.status_code == 429:
#                     return name, None, 'Rate limited'
#                 else:
#                     return name, None, f'HTTP {response.status_code}'
#             except Exception as e:
#                 return name, None, str(e)
        
#         # Run all requests in parallel
#         with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#             futures = {executor.submit(fetch_endpoint, name, url): name for name, url in endpoints.items()}
            
#             for future in concurrent.futures.as_completed(futures):
#                 name, data, error = future.result()
#                 if error:
#                     self.errors[name] = error
#                 else:
#                     self.results[name] = data
        
#         return True
    
#     def analyze_user_data(self):
#         """Perform deep analysis on user data"""
#         if 'basic_info' not in self.results:
#             return False
        
#         user = self.results['basic_info']
        
#         # Snowflake analysis
#         user_id = user.get('id')
#         if user_id:
#             try:
#                 snowflake = int(user_id)
#                 timestamp = ((snowflake >> 22) + 1420070400000) / 1000
#                 created_at = datetime.fromtimestamp(timestamp, timezone.utc)
                
#                 self.results['snowflake_analysis'] = {
#                     'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S UTC'),
#                     'timestamp': timestamp,
#                     'worker_id': (snowflake & 0x3E0000) >> 17,
#                     'process_id': (snowflake & 0x1F000) >> 12,
#                     'increment': snowflake & 0xFFF,
#                     'age_days': round((time.time() - timestamp) / 86400, 1)
#                 }
#             except:
#                 self.results['snowflake_analysis'] = {'error': 'Failed to decode'}
        
#         # Premium analysis
#         premium_type = user.get('premium_type', 0)
#         premium_map = {
#             0: 'None',
#             1: 'Nitro Classic',
#             2: 'Nitro',
#             3: 'Nitro Basic'
#         }
        
#         # Badge analysis from public flags - FIXED TYPE CONVERSION
#         flags = user.get('public_flags', 0)
#         # Ensure flags is integer
#         try:
#             flags_int = int(flags) if not isinstance(flags, int) else flags
#         except (ValueError, TypeError):
#             flags_int = 0
        
#         badges = []
        
#         flag_definitions = {
#             1 << 0: 'STAFF',
#             1 << 1: 'PARTNER',
#             1 << 2: 'HYPESQUAD',
#             1 << 3: 'BUG_HUNTER_LEVEL_1',
#             1 << 6: 'HYPESQUAD_BRAVERY',
#             1 << 7: 'HYPESQUAD_BRILLIANCE',
#             1 << 8: 'HYPESQUAD_BALANCE',
#             1 << 9: 'EARLY_SUPPORTER',
#             1 << 10: 'TEAM_USER',
#             1 << 14: 'BUG_HUNTER_LEVEL_2',
#             1 << 16: 'VERIFIED_BOT',
#             1 << 17: 'VERIFIED_DEVELOPER',
#             1 << 18: 'CERTIFIED_MODERATOR',
#             1 << 22: 'ACTIVE_DEVELOPER',
#             1 << 23: 'BOT_HTTP_INTERACTIONS'
#         }
        
#         for flag_value, badge_name in flag_definitions.items():
#             if flags_int & flag_value:
#                 badges.append(badge_name)
        
#         # Avatar analysis
#         avatar_hash = user.get('avatar')
#         avatar_info = {
#             'hash': avatar_hash,
#             'has_custom': avatar_hash is not None,
#             'is_animated': avatar_hash.startswith('a_') if avatar_hash else False,
#             'cdn_urls': {}
#         }
        
#         if avatar_hash and user_id:
#             base_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}"
#             avatar_info['cdn_urls'] = {
#                 'png_4096': f"{base_url}.png?size=4096",
#                 'webp_4096': f"{base_url}.webp?size=4096",
#                 'gif_4096': f"{base_url}.gif?size=4096" if avatar_hash.startswith('a_') else None
#             }
        
#         # Banner analysis
#         banner_hash = user.get('banner')
#         banner_color = user.get('banner_color')
#         accent_color = user.get('accent_color')
        
#         banner_info = {
#             'hash': banner_hash,
#             'color': banner_color,
#             'accent': accent_color,
#             'has_banner': banner_hash is not None,
#             'has_color': banner_color is not None,
#             'cdn_urls': {}
#         }
        
#         if banner_hash and user_id:
#             base_url = f"https://cdn.discordapp.com/banners/{user_id}/{banner_hash}"
#             banner_info['cdn_urls'] = {
#                 'png_4096': f"{base_url}.png?size=4096",
#                 'webp_4096': f"{base_url}.webp?size=4096",
#                 'gif_4096': f"{base_url}.gif?size=4096" if banner_hash.startswith('a_') else None
#             }
        
#         # MFA analysis
#         mfa_enabled = user.get('mfa_enabled', False)
#         authenticator_types = user.get('authenticator_types', [])
        
#         mfa_types = []
#         for auth_type in authenticator_types:
#             if auth_type == 1:
#                 mfa_types.append('SMS')
#             elif auth_type == 2:
#                 mfa_types.append('TOTP App')
#             elif auth_type == 3:
#                 mfa_types.append('WebAuthn')
#             else:
#                 mfa_types.append(f'Unknown ({auth_type})')
        
#         # Security assessment
#         security_score = 0
#         if mfa_enabled:
#             security_score += 40
#         if user.get('verified', False):
#             security_score += 20
#         if phone := user.get('phone'):
#             security_score += 20
#         if len(mfa_types) > 1:
#             security_score += 20
        
#         security_assessment = 'HIGH' if security_score >= 60 else 'MEDIUM' if security_score >= 30 else 'LOW'
        
#         # Store analysis
#         self.results['user_analysis'] = {
#             'premium': {
#                 'type': premium_map.get(premium_type, 'Unknown'),
#                 'raw_value': premium_type
#             },
#             'badges': badges,
#             'badge_count': len(badges),
#             'avatar': avatar_info,
#             'banner': banner_info,
#             'mfa': {
#                 'enabled': mfa_enabled,
#                 'types': mfa_types,
#                 'type_count': len(mfa_types)
#             },
#             'security': {
#                 'score': security_score,
#                 'assessment': security_assessment,
#                 'factors': []
#             },
#             'account_age': self.results.get('snowflake_analysis', {}).get('age_days', 'Unknown')
#         }
        
#         # Add security factors
#         if mfa_enabled:
#             self.results['user_analysis']['security']['factors'].append('MFA Enabled')
#         if user.get('verified'):
#             self.results['user_analysis']['security']['factors'].append('Email Verified')
#         if user.get('phone'):
#             self.results['user_analysis']['security']['factors'].append('Phone Linked')
#         if len(mfa_types) > 1:
#             self.results['user_analysis']['security']['factors'].append('Multiple MFA Methods')
        
#         return True
    
#     def analyze_guilds(self):
#         """Analyze guild data - FIXED VERSION (KEEP ONLY THIS ONE)"""
#         if 'guilds' not in self.results:
#             return False
        
#         guilds = self.results['guilds']
        
#         if not guilds or not isinstance(guilds, list):
#             self.results['guild_analysis'] = {'error': 'No guild data'}
#             return False
        
#         # Basic stats
#         total_guilds = len(guilds)
#         owner_guilds = []
#         admin_guilds = []
        
#         # Fix: Convert permissions to int before bitwise operation
#         for guild in guilds:
#             # Check if owner
#             if guild.get('owner', False):
#                 owner_guilds.append(guild)
            
#             # Check if admin - convert permission to int first
#             permissions = guild.get('permissions')
#             if permissions:
#                 try:
#                     # Ensure permissions is an integer
#                     perm_int = int(permissions) if not isinstance(permissions, int) else permissions
#                     if perm_int & 0x8:  # ADMINISTRATOR permission
#                         admin_guilds.append(guild)
#                 except (ValueError, TypeError):
#                     # If conversion fails, skip this guild
#                     continue
        
#         # Size analysis
#         large_guilds = []
#         medium_guilds = []
#         small_guilds = []
        
#         for guild in guilds:
#             member_count = guild.get('approximate_member_count', 0)
#             # Ensure member_count is int
#             try:
#                 member_int = int(member_count) if not isinstance(member_count, int) else member_count
                
#                 if member_int > 10000:
#                     large_guilds.append(guild)
#                 elif 1000 < member_int <= 10000:
#                     medium_guilds.append(guild)
#                 elif member_int <= 1000:
#                     small_guilds.append(guild)
#             except (ValueError, TypeError):
#                 # Skip if conversion fails
#                 continue
        
#         # Boost analysis
#         boosted_guilds = []
#         total_boosts = 0
        
#         for guild in guilds:
#             boost_count = guild.get('premium_subscription_count', 0)
#             try:
#                 boost_int = int(boost_count) if not isinstance(boost_count, int) else boost_count
#                 if boost_int > 0:
#                     boosted_guilds.append(guild)
#                     total_boosts += boost_int
#             except (ValueError, TypeError):
#                 continue
        
#         # Partner/verified analysis
#         partnered_guilds = []
#         verified_guilds = []
        
#         for guild in guilds:
#             features = guild.get('features', [])
#             if features and isinstance(features, list):
#                 if 'PARTNERED' in features:
#                     partnered_guilds.append(guild)
#                 if 'VERIFIED' in features:
#                     verified_guilds.append(guild)
        
#         # Store analysis
#         self.results['guild_analysis'] = {
#             'total': total_guilds,
#             'owned': len(owner_guilds),
#             'admin': len(admin_guilds),
#             'by_size': {
#                 'large': len(large_guilds),
#                 'medium': len(medium_guilds),
#                 'small': len(small_guilds)
#             },
#             'boosts': {
#                 'boosted_guilds': len(boosted_guilds),
#                 'total_boosts': total_boosts
#             },
#             'special': {
#                 'partnered': len(partnered_guilds),
#                 'verified': len(verified_guilds)
#             },
#             'sample_guilds': []
#         }
        
#         # Add sample guilds (first 5)
#         for i, guild in enumerate(guilds[:5]):
#             self.results['guild_analysis']['sample_guilds'].append({
#                 'name': guild.get('name', 'Unknown'),
#                 'id': guild.get('id', 'Unknown'),
#                 'owner': guild.get('owner', False),
#                 'members': guild.get('approximate_member_count', 'Unknown'),
#                 'boosts': guild.get('premium_subscription_count', 0)
#             })
        
#         return True
    
#     def analyze_relationships(self):
#         """Analyze friends/relationships"""
#         if 'relationships' not in self.results:
#             return False
        
#         relationships = self.results['relationships']
        
#         if not relationships or not isinstance(relationships, list):
#             self.results['relationship_analysis'] = {'error': 'No relationship data'}
#             return False
        
#         # Categorize relationships
#         friends = [r for r in relationships if r.get('type') == 1]
#         blocked = [r for r in relationships if r.get('type') == 2]
#         incoming = [r for r in relationships if r.get('type') == 3]
#         outgoing = [r for r in relationships if r.get('type') == 4]
        
#         # Friend analysis
#         friend_details = []
#         for friend in friends[:10]:  # First 10 friends
#             user = friend.get('user', {})
#             friend_details.append({
#                 'username': f"{user.get('username', 'Unknown')}#{user.get('discriminator', '0000')}",
#                 'id': user.get('id', 'Unknown'),
#                 'global_name': user.get('global_name'),
#                 'avatar': user.get('avatar')
#             })
        
#         self.results['relationship_analysis'] = {
#             'total': len(relationships),
#             'friends': len(friends),
#             'blocked': len(blocked),
#             'incoming': len(incoming),
#             'outgoing': len(outgoing),
#             'sample_friends': friend_details,
#             'friend_ids': [f.get('user', {}).get('id') for f in friends if f.get('user', {}).get('id')]
#         }
        
#         return True
    
#     def analyze_billing(self):
#         """Analyze billing information"""
#         billing_data = {}
        
#         # Payment sources
#         if 'billing' in self.results and self.results['billing']:
#             payment_sources = self.results['billing']
#             billing_data['payment_sources'] = {
#                 'count': len(payment_sources),
#                 'types': [],
#                 'details': []
#             }
            
#             for source in payment_sources:
#                 source_type = source.get('type', 0)
#                 type_name = 'Unknown'
#                 if source_type == 1:
#                     type_name = 'Credit Card'
#                 elif source_type == 2:
#                     type_name = 'PayPal'
                
#                 billing_data['payment_sources']['types'].append(type_name)
#                 billing_data['payment_sources']['details'].append({
#                     'type': type_name,
#                     'id': source.get('id', 'Unknown'),
#                     'invalid': source.get('invalid', False)
#                 })
        
#         # Subscriptions
#         if 'subscriptions' in self.results and self.results['subscriptions']:
#             subscriptions = self.results['subscriptions']
#             billing_data['subscriptions'] = {
#                 'count': len(subscriptions),
#                 'active': [s for s in subscriptions if s.get('status') == 'active'],
#                 'details': []
#             }
            
#             for sub in subscriptions:
#                 billing_data['subscriptions']['details'].append({
#                     'id': sub.get('id', 'Unknown'),
#                     'status': sub.get('status', 'unknown'),
#                     'items': sub.get('items', [])
#                 })
        
#         # Entitlements
#         if 'entitlements' in self.results and self.results['entitlements']:
#             entitlements = self.results['entitlements']
#             billing_data['entitlements'] = {
#                 'count': len(entitlements),
#                 'types': list(set(e.get('type', 'unknown') for e in entitlements))
#             }
        
#         if billing_data:
#             self.results['billing_analysis'] = billing_data
        
#         return bool(billing_data)
    
#     def run_full_analysis(self):
#         """Run complete analysis"""
#         print(f"{LOADING} Starting comprehensive token analysis...", reset)
        
#         # Step 1: Check token validity
#         print(f"{LOADING} Step 1/6: Validating token...", reset)
#         if not self.check_token_validity():
#             print(f"{PREFIX} {ERROR} Token is invalid or unauthorized", reset)
#             return False
        
#         # Step 2: Analyze token structure
#         print(f"{LOADING} Step 2/6: Analyzing token structure...", reset)
#         self.analyze_token_structure()
        
#         # Step 3: Fetch parallel data
#         print(f"{LOADING} Step 3/6: Fetching account data (parallel)...", reset)
#         self.fetch_parallel_data()
        
#         # Step 4: Analyze user data
#         print(f"{LOADING} Step 4/6: Analyzing user profile...", reset)
#         self.analyze_user_data()
        
#         # Step 5: Analyze guilds
#         print(f"{LOADING} Step 5/6: Analyzing servers...", reset)
#         self.analyze_guilds()
        
#         # Step 6: Analyze relationships and billing
#         print(f"{LOADING} Step 6/6: Analyzing relationships & billing...", reset)
#         self.analyze_relationships()
#         self.analyze_billing()
        
#         print(f"{SUCCESS} Analysis complete!", reset)
#         return True

# def display_results(analyzer):
#     """Display analysis results"""
#     results = analyzer.results
    
#     print(f"\n{SUCCESS} DISCORD TOKEN INTELLIGENCE REPORT", reset)
#     print(f"{red}═══════════════════════════════════════════════════════════════{reset}")
    
#     # Token Information
#     print(f"{PREFIX1}🔑 TOKEN INFORMATION{SUFFIX1}")
#     print(f"{SUCCESS} Status{SUFFIX1}        : {red}{results.get('token_status', 'Unknown')}{reset}")
    
#     if 'token_analysis' in results:
#         token_analysis = results['token_analysis']
#         print(f"{SUCCESS} Type{SUFFIX1}          : {red}{token_analysis.get('type', 'Unknown')}{reset}")
#         print(f"{SUCCESS} Format{SUFFIX1}        : {red}{token_analysis.get('format', 'Unknown')}{reset}")
#         print(f"{SUCCESS} Hash{SUFFIX1}          : {red}{token_analysis.get('hash', 'Unknown')}{reset}")
#         print(f"{SUCCESS} Preview{SUFFIX1}       : {red}{token_analysis.get('first_10', 'Unknown')}{reset}")
    
#     # Basic User Info
#     if 'basic_info' in results:
#         user = results['basic_info']
#         print(f"\n{PREFIX1}👤 USER INFORMATION{SUFFIX1}")
        
#         username = user.get('username', 'Unknown')
#         discriminator = user.get('discriminator', '0')
#         if discriminator != '0':
#             print(f"{SUCCESS} Username{SUFFIX1}      : {red}{username}#{discriminator}{reset}")
#         else:
#             print(f"{SUCCESS} Username{SUFFIX1}      : {red}{username}{reset}")
        
#         if global_name := user.get('global_name'):
#             print(f"{SUCCESS} Global Name{SUFFIX1}   : {red}{global_name}{reset}")
        
#         print(f"{SUCCESS} User ID{SUFFIX1}       : {red}{user.get('id', 'Unknown')}{reset}")
#         print(f"{SUCCESS} Email{SUFFIX1}         : {red}{user.get('email', 'Not set')}{reset}")
#         print(f"{SUCCESS} Email Verified{SUFFIX1}: {red}{user.get('verified', 'Unknown')}{reset}")
#         print(f"{SUCCESS} Phone{SUFFIX1}         : {red}{user.get('phone', 'Not set')}{reset}")
        
#         if 'snowflake_analysis' in results:
#             snowflake = results['snowflake_analysis']
#             print(f"{SUCCESS} Created{SUFFIX1}       : {red}{snowflake.get('created_at', 'Unknown')}{reset}")
#             print(f"{SUCCESS} Account Age{SUFFIX1}   : {red}{snowflake.get('age_days', 'Unknown')} days{reset}")
    
#     # Premium & Badges
#     if 'user_analysis' in results:
#         user_analysis = results['user_analysis']
#         print(f"\n{PREFIX1}💎 ACCOUNT STATUS{SUFFIX1}")
#         print(f"{SUCCESS} Premium{SUFFIX1}        : {red}{user_analysis.get('premium', {}).get('type', 'None')}{reset}")
#         print(f"{SUCCESS} Badges{SUFFIX1}         : {red}{user_analysis.get('badge_count', 0)} badges{reset}")
        
#         if badges := user_analysis.get('badges', []):
#             print(f"{SUCCESS} Badge List{SUFFIX1}     : {red}{', '.join(badges[:5])}{reset}")
#             if len(badges) > 5:
#                 print(f"{SUCCESS}               : {red}... and {len(badges)-5} more{reset}")
    
#     # Security
#     if 'user_analysis' in results:
#         security = user_analysis.get('security', {})
#         print(f"{SUCCESS} Security{SUFFIX1}       : {red}{security.get('assessment', 'Unknown')} ({security.get('score', 0)}/100){reset}")
#         print(f"{SUCCESS} MFA Enabled{SUFFIX1}    : {red}{user_analysis.get('mfa', {}).get('enabled', False)}{reset}")
        
#         if mfa_types := user_analysis.get('mfa', {}).get('types', []):
#             print(f"{SUCCESS} MFA Methods{SUFFIX1}   : {red}{', '.join(mfa_types)}{reset}")
    
#     # Guild Analysis
#     if 'guild_analysis' in results:
#         guilds = results['guild_analysis']
#         print(f"\n{PREFIX1}🏰 SERVER ANALYSIS{SUFFIX1}")
#         print(f"{SUCCESS} Total Servers{SUFFIX1}  : {red}{guilds.get('total', 0)}{reset}")
#         print(f"{SUCCESS} Owned Servers{SUFFIX1}  : {red}{guilds.get('owned', 0)}{reset}")
#         print(f"{SUCCESS} Admin Servers{SUFFIX1}  : {red}{guilds.get('admin', 0)}{reset}")
        
#         if boosts := guilds.get('boosts', {}):
#             print(f"{SUCCESS} Boosted Servers{SUFFIX1}: {red}{boosts.get('boosted_guilds', 0)}{reset}")
#             print(f"{SUCCESS} Total Boosts{SUFFIX1}  : {red}{boosts.get('total_boosts', 0)}{reset}")
        
#         # Sample guilds
#         if sample_guilds := guilds.get('sample_guilds', []):
#             print(f"{SUCCESS} Sample Servers{SUFFIX1}:")
#             for guild in sample_guilds[:3]:
#                 print(f"{SUCCESS}   • {red}{guild.get('name', 'Unknown')} ({guild.get('members', '?')} members){reset}")
    
#     # Relationship Analysis
#     if 'relationship_analysis' in results:
#         rels = results['relationship_analysis']
#         print(f"\n{PREFIX1}👥 RELATIONSHIPS{SUFFIX1}")
#         print(f"{SUCCESS} Total{SUFFIX1}          : {red}{rels.get('total', 0)}{reset}")
#         print(f"{SUCCESS} Friends{SUFFIX1}        : {red}{rels.get('friends', 0)}{reset}")
#         print(f"{SUCCESS} Blocked{SUFFIX1}        : {red}{rels.get('blocked', 0)}{reset}")
        
#         if sample_friends := rels.get('sample_friends', []):
#             print(f"{SUCCESS} Sample Friends{SUFFIX1}:")
#             for friend in sample_friends[:3]:
#                 print(f"{SUCCESS}   • {red}{friend.get('username', 'Unknown')}{reset}")
    
#     # Billing Analysis
#     if 'billing_analysis' in results:
#         billing = results['billing_analysis']
#         print(f"\n{PREFIX1}💰 BILLING INFORMATION{SUFFIX1}")
        
#         if 'payment_sources' in billing:
#             ps = billing['payment_sources']
#             print(f"{SUCCESS} Payment Methods{SUFFIX1}: {red}{ps.get('count', 0)}{reset}")
#             if ps.get('types'):
#                 print(f"{SUCCESS} Types{SUFFIX1}         : {red}{', '.join(set(ps['types']))}{reset}")
        
#         if 'subscriptions' in billing:
#             subs = billing['subscriptions']
#             active = len(subs.get('active', []))
#             print(f"{SUCCESS} Subscriptions{SUFFIX1}  : {red}{subs.get('count', 0)} ({active} active){reset}")
    
#     # Errors/Warnings
#     if analyzer.errors:
#         print(f"\n{PREFIX1}⚠️ ERRORS & WARNINGS{SUFFIX1}")
#         for key, error in list(analyzer.errors.items())[:5]:
#             print(f"{SUCCESS} {key}{SUFFIX1}: {red}{error}{reset}")
#         if len(analyzer.errors) > 5:
#             print(f"{SUCCESS} ...{SUFFIX1}            : {red}and {len(analyzer.errors)-5} more errors{reset}")
    
#     print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
#     print(f"{PREFIX1}📊 Data Points Collected{SUFFIX1}: {red}{len(results)}{reset}")
#     print(f"{PREFIX1}⏱️ Analysis Time{SUFFIX1}     : {red}{datetime.now().strftime('%H:%M:%S')}{reset}")
#     print(f"{red}═══════════════════════════════════════════════════════════════{reset}")

# def save_comprehensive_report(analyzer, filename=None):
#     """Save full report to file"""
#     try:
#         if not filename:
#             timestamp = int(time.time())
#             user_id = analyzer.results.get('basic_info', {}).get('id', 'unknown')
#             filename = f"token_intel_{user_id}_{timestamp}.txt"
        
#         with open(filename, 'w', encoding='utf-8') as f:
#             f.write("=" * 70 + "\n")
#             f.write("DISCORD TOKEN INTELLIGENCE REPORT\n")
#             f.write("=" * 70 + "\n\n")
            
#             f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
#             f.write(f"Token Status: {analyzer.results.get('token_status', 'Unknown')}\n\n")
            
#             # Token info
#             f.write("TOKEN INFORMATION:\n")
#             f.write("-" * 40 + "\n")
#             if 'token_analysis' in analyzer.results:
#                 for key, value in analyzer.results['token_analysis'].items():
#                     f.write(f"  {key}: {value}\n")
            
#             # User info
#             f.write("\nUSER INFORMATION:\n")
#             f.write("-" * 40 + "\n")
#             if 'basic_info' in analyzer.results:
#                 user = analyzer.results['basic_info']
#                 for key, value in user.items():
#                     if key not in ['flags', 'public_flags', 'avatar_decoration_data']:
#                         f.write(f"  {key}: {value}\n")
            
#             # Analysis sections
#             sections = ['user_analysis', 'guild_analysis', 'relationship_analysis', 'billing_analysis']
#             for section in sections:
#                 if section in analyzer.results:
#                     f.write(f"\n{section.upper().replace('_', ' ')}:\n")
#                     f.write("-" * 40 + "\n")
#                     import json
#                     f.write(json.dumps(analyzer.results[section], indent=2, default=str))
#                     f.write("\n")
            
#             # Errors
#             if analyzer.errors:
#                 f.write("\nERRORS & WARNINGS:\n")
#                 f.write("-" * 40 + "\n")
#                 for key, error in analyzer.errors.items():
#                     f.write(f"  {key}: {error}\n")
            
#             f.write("\n" + "=" * 70 + "\n")
#             f.write("End of Report\n")
#             f.write("=" * 70 + "\n")
        
#         return filename
#     except Exception as e:
#         return None

# try:
#     token = ChoiceToken()
    
#     # Create analyzer and run analysis
#     analyzer = DiscordTokenAnalyzer(token)
    
#     if analyzer.run_full_analysis():
#         display_results(analyzer)
        
#         # Options menu
#         while True:
#             print(f"\n{PREFIX} {INFO} Additional Options:", reset)
#             print(f"  {PREFIX1}1{SUFFIX1} Save full report to file")
#             print(f"  {PREFIX1}2{SUFFIX1} View raw JSON data")
#             print(f"  {PREFIX1}3{SUFFIX1} Check another token")
#             print(f"  {PREFIX1}4{SUFFIX1} Return to menu")
            
#             choice = input(f"\n{PREFIX} Select option (1-4): ").strip()
            
#             if choice == '1':
#                 filename = save_comprehensive_report(analyzer)
#                 if filename:
#                     print(f"{PREFIX} {SUCCESS} Report saved to: {red}{filename}{reset}")
#                 else:
#                     print(f"{PREFIX} {ERROR} Failed to save report", reset)
#                 time.sleep(1)
#                 continue
            
#             elif choice == '2':
#                 print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
#                 print(f"{red}                     RAW JSON DATA                           {reset}")
#                 print(f"{red}═══════════════════════════════════════════════════════════════{reset}\n")
                
#                 import json
#                 print(json.dumps(analyzer.results, indent=2, default=str))
                
#                 print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
#                 input(f"\n{PREFIX} Press Enter to continue... {reset}")
#                 continue
            
#             elif choice == '3':
#                 print(f"{LOADING} Restarting...", reset)
#                 time.sleep(1)
#                 exec(open(__file__).read())
#                 exit()
            
#             elif choice == '4':
#                 break
            
#             else:
#                 break
    
#     else:
#         print(f"{PREFIX} {ERROR} Token analysis failed", reset)
#         if analyzer.errors:
#             for key, error in analyzer.errors.items():
#                 print(f"{PREFIX}   {key}: {error}", reset)
    
#     Continue()
#     Reset()

# except KeyboardInterrupt:
#     print(f"\n{PREFIX} {INFO} Analysis cancelled", reset)
#     Continue()
#     Reset()
# except Exception as e:
#     Error(e)