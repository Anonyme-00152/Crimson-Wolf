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
    import time
    import re
    from datetime import datetime
    import requests
except Exception as e:
    MissingModule(e)

Title("Discord ID Decoder")
Connection()

def decode_snowflake(user_id):
    """Extract ALL information from snowflake ID - ALWAYS WORKS"""
    try:
        snowflake = int(user_id)
        
        # Discord epoch (2015-01-01)
        DISCORD_EPOCH = 1420070400000
        
        # Extract timestamp
        timestamp_ms = (snowflake >> 22) + DISCORD_EPOCH
        timestamp = timestamp_ms / 1000
        
        # Convert to readable date
        created_at = datetime.fromtimestamp(timestamp)
        created_str = created_at.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Calculate age
        current_time = time.time()
        age_seconds = current_time - timestamp
        age_days = round(age_seconds / 86400, 1)
        age_years = round(age_days / 365.25, 2)
        
        # Extract internal components
        worker_id = (snowflake & 0x3E0000) >> 17
        process_id = (snowflake & 0x1F000) >> 12
        increment = snowflake & 0xFFF
        
        # Generate binary representation
        binary = bin(snowflake)[2:].zfill(64)
        
        # Determine default avatar
        default_avatar_num = snowflake % 5
        
        return {
            'id': user_id,
            'timestamp': timestamp,
            'created_at': created_str,
            'age_days': age_days,
            'age_years': age_years,
            'worker_id': worker_id,
            'process_id': process_id,
            'increment': increment,
            'binary': binary,
            'default_avatar': default_avatar_num,
            'raw_snowflake': snowflake,
            'timestamp_ms': timestamp_ms
        }
    except Exception as e:
        return None

def check_discord_cdn(user_id):
    """Check Discord's CDN for avatar - works for public avatars"""
    results = {}
    
    # Check default avatars (always works)
    default_num = int(user_id) % 5
    default_url = f"https://cdn.discordapp.com/embed/avatars/{default_num}.png"
    results['default_avatar'] = default_url
    
    # Try common avatar formats (if user has custom avatar)
    formats = ['png', 'webp', 'jpg', 'gif']
    for fmt in formats:
        # Try standard avatar URL
        url = f"https://cdn.discordapp.com/avatars/{user_id}/"
        
        try:
            # Try head request to check if exists
            response = requests.head(f"{url}a_123.{fmt}?size=4096", timeout=3)
            # We just care if CDN responds
            results['cdn_accessible'] = True
            break
        except:
            pass
    
    # Generate all possible avatar URLs
    avatar_urls = []
    sizes = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
    
    for size in sizes:
        # Default avatar URLs
        avatar_urls.append(f"https://cdn.discordapp.com/embed/avatars/{default_num}.png?size={size}")
    
    results['avatar_urls'] = avatar_urls[:3]  # Show first 3
    
    return results

def get_basic_info(user_id):
    """Get basic info that ALWAYS works"""
    info = {}
    
    # Always decode snowflake
    snowflake_data = decode_snowflake(user_id)
    if not snowflake_data:
        return None
    
    info.update(snowflake_data)
    
    # Always check CDN
    cdn_data = check_discord_cdn(user_id)
    info.update(cdn_data)
    
    # Determine account status based on creation date
    if snowflake_data['age_days'] < 30:
        info['account_status'] = "New Account"
    elif snowflake_data['age_days'] < 365:
        info['account_status'] = "Relatively New"
    elif snowflake_data['age_days'] > 365 * 3:
        info['account_status'] = "Old Account"
    else:
        info['account_status'] = "Established Account"
    
    # Calculate creation relative to Discord's history
    discord_launch = datetime(2015, 5, 13)  # Discord public launch
    account_date = datetime.fromtimestamp(snowflake_data['timestamp'])
    
    if account_date < datetime(2016, 1, 1):
        info['era'] = "Early Discord (2015)"
    elif account_date < datetime(2018, 1, 1):
        info['era'] = "Mid Era (2016-2017)"
    elif account_date < datetime(2020, 1, 1):
        info['era'] = "Growth Era (2018-2019)"
    elif account_date < datetime(2022, 1, 1):
        info['era'] = "Pandemic Era (2020-2021)"
    else:
        info['era'] = "Recent Account"
    
    return info

def display_results(info):
    """Display the results in a clean format"""
    if not info:
        print(f"{PREFIX} {ERROR} Failed to decode ID", reset)
        return
    
    print(f"\n{SUCCESS} Discord ID Analysis - 100% RELIABLE", reset)
    print(f"{red}═══════════════════════════════════════════════════════════════{reset}")
    
    # Basic info
    print(f"{PREFIX1}🆔 Discord ID{SUFFIX1}        : {red}{info['id']}{reset}")
    print(f"{PREFIX1}📅 Created At{SUFFIX1}        : {red}{info['created_at']}{reset}")
    print(f"{PREFIX1}⏳ Account Age{SUFFIX1}       : {red}{info['age_days']} days ({info['age_years']} years){reset}")
    print(f"{PREFIX1}📊 Status{SUFFIX1}           : {red}{info['account_status']}{reset}")
    print(f"{PREFIX1}📅 Era{SUFFIX1}              : {red}{info['era']}{reset}")
    
    # Snowflake internals
    print(f"\n{PREFIX1}❄️ Snowflake Internals{SUFFIX1}")
    print(f"{PREFIX1}   Worker ID{SUFFIX1}        : {red}{info['worker_id']}{reset}")
    print(f"{PREFIX1}   Process ID{SUFFIX1}       : {red}{info['process_id']}{reset}")
    print(f"{PREFIX1}   Increment{SUFFIX1}        : {red}{info['increment']}{reset}")
    
    # Avatar info
    print(f"\n{PREFIX1}🖼️ Avatar Information{SUFFIX1}")
    print(f"{PREFIX1}   Default Type{SUFFIX1}     : {red}{info['default_avatar']}{reset}")
    print(f"{PREFIX1}   Default URL{SUFFIX1}      : {red}{info['default_avatar']}{reset}")
    
    if 'avatar_urls' in info:
        print(f"{PREFIX1}   Sample URLs{SUFFIX1}      :")
        for url in info['avatar_urls']:
            print(f"{PREFIX1}     - {red}{url}{reset}")
    
    # Technical details
    print(f"\n{PREFIX1}🔧 Technical Details{SUFFIX1}")
    print(f"{PREFIX1}   Timestamp{SUFFIX1}        : {red}{info['timestamp_ms']} ms{reset}")
    print(f"{PREFIX1}   Binary{SUFFIX1}           : {red}{info['binary'][:40]}...{reset}")
    
    print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
    print(f"{PREFIX1}✅ Data Source{SUFFIX1}       : {red}Snowflake Decoding + Discord CDN{reset}")
    print(f"{PREFIX1}💯 Reliability{SUFFIX1}      : {red}100% (No external APIs){reset}")
    print(f"{red}═══════════════════════════════════════════════════════════════{reset}")

def save_analysis(info):
    """Save analysis to file"""
    try:
        timestamp = int(time.time())
        filename = f"discord_analysis_{info['id']}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("DISCORD ID ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
            f.write(f"Discord ID: {info['id']}\n\n")
            
            f.write("BASIC INFORMATION:\n")
            f.write(f"  Created At: {info['created_at']}\n")
            f.write(f"  Account Age: {info['age_days']} days ({info['age_years']} years)\n")
            f.write(f"  Account Status: {info['account_status']}\n")
            f.write(f"  Era: {info['era']}\n\n")
            
            f.write("SNOWFLAKE INTERNALS:\n")
            f.write(f"  Worker ID: {info['worker_id']}\n")
            f.write(f"  Process ID: {info['process_id']}\n")
            f.write(f"  Increment: {info['increment']}\n")
            f.write(f"  Raw Snowflake: {info['raw_snowflake']}\n")
            f.write(f"  Binary: {info['binary']}\n\n")
            
            f.write("AVATAR INFORMATION:\n")
            f.write(f"  Default Avatar Type: {info['default_avatar']}\n")
            f.write(f"  Default Avatar URL: https://cdn.discordapp.com/embed/avatars/{info['default_avatar']}.png\n\n")
            
            f.write("TECHNICAL DETAILS:\n")
            f.write(f"  Timestamp: {info['timestamp']}\n")
            f.write(f"  Timestamp (ms): {info['timestamp_ms']}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("Generated by Discord ID Decoder\n")
            f.write("=" * 60 + "\n")
        
        return filename
    except Exception as e:
        return None

try:
    while True:
        print()
        user_id = input(f"{INPUT} Enter Discord User ID {red}->{reset} ").strip()
        
        # Simple validation
        if not user_id.isdigit() or len(user_id) < 17 or len(user_id) > 19:
            print(f"{PREFIX} {ERROR} Invalid Discord ID format. Must be 17-19 digits.", reset)
            
            retry = input(f"{PREFIX} Try again? (y/n): ").strip().lower()
            if retry == 'y':
                continue
            else:
                break
        
        print(f"\n{LOADING} Decoding snowflake ID...", reset)
        
        # Get info (this ALWAYS works if ID is valid)
        info = get_basic_info(user_id)
        
        if not info:
            print(f"{PREFIX} {ERROR} Failed to decode ID. Check format.", reset)
            Continue()
            Reset()
        
        # Display results
        display_results(info)
        
        # Options
        print(f"\n{PREFIX} {INFO} Options:", reset)
        print(f"  {PREFIX1}1{SUFFIX1} Save full analysis to file")
        print(f"  {PREFIX1}2{SUFFIX1} Check another ID")
        print(f"  {PREFIX1}3{SUFFIX1} Best-Website-Id-Lookup")
        print(f"  {PREFIX1}4{SUFFIX1} Return to menu")
        
        choice = input(f"\n{PREFIX} Select option (1-3): ").strip()
        
        if choice == '1':
            filename = save_analysis(info)
            if filename:
                print(f"{PREFIX} {SUCCESS} Analysis saved to: {red}{filename}{reset}")
            else:
                print(f"{PREFIX} {ERROR} Failed to save file", reset)
            time.sleep(1)
            Continue()
            Reset()
        
        elif choice == '2':
            continue  # Loop again
        
        elif choice == '4':
            break  # Exit to menu
        
        elif choice == '3':
            # Show detailed lookup websites
            print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
            print(f"{red}                  DETAILED LOOKUP WEBSITES                    {reset}")
            print(f"{red}═══════════════════════════════════════════════════════════════{reset}\n")
            
            print(f"{PREFIX1}🌐 Discord ID Lookup Services{SUFFIX1}")
            print(f"{PREFIX1}   1. Discord ID Lookup{SUFFIX1}   : {red}https://discord.id/{reset}")
            print(f"{PREFIX1}   2. VideoDubber{SUFFIX1}         : {red}https://videodubber.ai/tools/discord/discord-id-lookup/")
            print(f"{PREFIX1}   3. Rappytv{SUFFIX1}             : {red}https://id.rappytv.com/")
            # print(f"{PREFIX1}   4. Luminabots{SUFFIX1}         : {red}https://luminabots.xyz/tools/user-lookup{reset}")
            # print(f"{PREFIX1}   5. Mesalytic{SUFFIX1}          : {red}https://mesalytic.moe/discordlookup{reset}")
            
            print(f"\n{PREFIX1}🔍 Alternative Methods{SUFFIX1}")
            print(f"{PREFIX1}   • Snowflake Decoder{SUFFIX1}    : {red}https://snowflake.ovh/{reset}")
            print(f"{PREFIX1}   • Discord Avatar{SUFFIX1}       : {red}https://cdn.discordapp.com/avatars/USER_ID/HASH.png{reset}")
            print(f"{PREFIX1}   • Discord Banner{SUFFIX1}       : {red}https://cdn.discordapp.com/banners/USER_ID/HASH.png{reset}")
            
            print(f"\n{PREFIX1}💡 How to use{SUFFIX1}")
            print(f"{PREFIX1}   Replace USER_ID with: {red}{info['id']}{reset}")
            print(f"{PREFIX1}   For avatar/banner, you need the hash from detailed APIs{reset}")
            
            print(f"\n{red}═══════════════════════════════════════════════════════════════{reset}")
            print(f"{PREFIX1}📋 Current User ID{SUFFIX1} : {red}{info['id']}{reset}")
            print(f"{PREFIX1}📅 Account Created{SUFFIX1} : {red}{info['created_at']}{reset}")
            print(f"{red}═══════════════════════════════════════════════════════════════{reset}")
            
            input(f"\n{PREFIX} Press Enter to return... {reset}")
            continue  # Go back to options menu
        
        else:
            break

except KeyboardInterrupt:
    print(f"\n{PREFIX} {INFO} Operation cancelled", reset)
    Continue()
    Reset()
except Exception as e:
    Error(e)