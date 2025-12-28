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
    import json 
    import string
    import random
    import threading
    import time
    import os
except Exception as e:
    MissingModule(e)

Title("Leakcheck.io Searcher")
Connection()

def leakcheck():
    """Leakcheck.io Searcher - Find if emails/usernames are in data breaches"""
    Clear()
    
    # Header
    print(f"{red}╔═══════════════════════════════════════════════════════════╗")
    print(f"{red}║                 LEAKCHECK.IO SEARCHER                    ║")
    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
    
    # ASCII Art with your colors
    ascii_art = f"""
{yellow}             *         *      *         *
{yellow}          ***          **********          ***
{yellow}       *****           **********           *****
{yellow}     *******           **********           *******
{yellow}   **********         ************         **********
{blue}  ****************************************************
{blue} ******************************************************
{blue}********************************************************
{blue}********************************************************
{blue}********************************************************
{blue} ******************************************************
{blue}  ********      ************************      ********
{blue}   *******       *     *********      *       *******
{blue}     ******             *******              ******
{blue}       *****             *****              *****
{blue}          ***             ***              ***
{blue}            **             *              **
{reset}"""
    print(ascii_art)
    
    try:
        # Get search input using your prompt style
        search = input(f"{PREFIX}Enter username/email to search {red}->{reset} ").strip()
        
        if not search:
            print(f"{ERROR} No input provided!")
            time.sleep(1.5)
            Continue()
            return
        
        print(f"\n{LOADING} Searching Leakcheck.io for '{search}'...")
        
        # API request
        api = f"https://leakcheck.io/api/public?check={search}"
        headers = {'User-Agent': f'{name_tool}-Tool/1.0'}
        res = requests.get(api, headers=headers, timeout=10)
        
        if res.status_code != 200:
            print(f"{ERROR} API Error: Status {res.status_code}")
            time.sleep(2)
            Continue()
            return
            
        data = res.json()
        
        # Results display
        print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
        print(f"{green}║                    SEARCH RESULTS                         ║")
        print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
        
        success = data.get('success', 'N/A')
        fields = data.get('fields', [])
        sources = data.get('sources', [])
        
        # Display info using your prefix/suffix system
        print(f"   {PREFIX1}Search Term{SUFFIX1}: {yellow}{search}{reset}")
        print(f"   {PREFIX1}API Status{SUFFIX1}: {green if success else red}{success}{reset}")
        print(f"   {PREFIX1}Time{SUFFIX1}: {time.strftime('%H:%M:%S')}")
        print(f"   {PREFIX1}Total Results{SUFFIX1}: {len(fields)} fields, {len(sources)} sources")
        
        if fields:
            print(f"\n   {PREFIX1}Compromised Fields{SUFFIX1} ({len(fields)}):")
            for i, field in enumerate(fields, 1):
                if i <= 20:  # Show first 20 only
                    print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {field}{reset}")
                else:
                    print(f"   {red}└─ {PREFIX1}...{SUFFIX1} +{len(fields)-20} more fields")
                    break
        
        if sources:
            print(f"\n   {PREFIX1}Breach Sources{SUFFIX1} ({len(sources)}):")
            for i, source in enumerate(sources[:10], 1):  # Show first 10
                print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {source}{reset}")
            
            if len(sources) > 10:
                print(f"   {red}└─ {PREFIX1}...{SUFFIX1} +{len(sources)-10} more sources")
        
        # Save option
        print(f"\n{red}═══════════════════════════════════════════════════════════")
        save = input(f"{PREFIX}Save results to file? (Y/N) {red}->{reset} ").strip().lower()
        
        if save in ['y', 'yes']:
            # Create safe filename
            safe_search = "".join(c for c in search if c.isalnum() or c in ('@', '.', '_', '-')).replace('@', '_at_')
            filename = f"Leakcheck_{safe_search}_{int(time.time())}.txt"
            
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"{name_tool} Tool - Leakcheck.io Results\n")
                    file.write(f"{'='*60}\n")
                    file.write(f"Search: {search}\n")
                    file.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"Status: {success}\n")
                    file.write(f"\nCompromised Fields ({len(fields)}):\n")
                    file.write(f"{'-'*40}\n")
                    for field in fields:
                        file.write(f"• {field}\n")
                    file.write(f"\nBreach Sources ({len(sources)}):\n")
                    file.write(f"{'-'*40}\n")
                    for source in sources:
                        file.write(f"• {source}\n")
                
                print(f"{SUCCESS} File saved: {yellow}{filename}{reset}")
                time.sleep(1)
            except Exception as e:
                print(f"{ERROR} Save failed: {str(e)}")
                time.sleep(2)
        
        # Security warning if compromised
        if fields or sources:
            print(f"\n{red}═══════════════════════════════════════════════════════════")
            print(f"{red}⚠  SECURITY WARNING: DATA FOUND IN BREACHES              ⚠")
            print(f"{red}═══════════════════════════════════════════════════════════{reset}")
            print(f"{yellow}Recommendations:{reset}")
            print(f"   {PREFIX1}1{SUFFIX1} Change passwords immediately")
            print(f"   {PREFIX1}2{SUFFIX1} Enable two-factor authentication")
            print(f"   {PREFIX1}3{SUFFIX1} Monitor accounts for suspicious activity")
        else:
            print(f"\n{green}═══════════════════════════════════════════════════════════")
            print(f"{green}✓  NO KNOWN BREACHES FOUND - DATA APPEARS SAFE          ✓")
            print(f"{green}═══════════════════════════════════════════════════════════{reset}")
        
    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out. Check your connection.")
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Connection failed. Check your internet.")
    except json.JSONDecodeError:
        print(f"{ERROR} Invalid API response.")
    except KeyboardInterrupt:
        print(f"\n{ERROR} Operation cancelled by user.")
    except Exception as e:
        Error(e)
    
    # Return
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    Continue()

# Main execution
if __name__ == "__main__":
    leakcheck()