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
    import threading
    import json
    import random
    import re
    import time
    import os
except Exception as e:
    MissingModule(e)

def main():
    Clear()
    Title("Dox3R Finder")
    Connection()

    print(f"""
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    {red}▓█████▄  ▒█████  ▒██   ██▒▓█████  ██▀███  
    {red}▒██▀ ██▌▒██▒  ██▒▒▒ █ █ ▒░▓█   ▀ ▓██ ▒ ██▒
    {red}░██   █▌▒██░  ██▒░░  █   ░▒███   ▓██ ░▄█ ▒
    {red}░▓█▄   ▌▒██   ██░ ░ █ █ ▒ ▒▓█  ▄ ▒██▀▀█▄  
    {red}░▒████▓ ░ ████▓▒░▒██▒ ▒██▒░▒████▒░██▓ ▒██▒
    {red} ▒▒▓  ▒ ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░░░ ▒░ ░░ ▒▓ ░▒▓░
    {red} ░ ▒  ▒   ░ ▒ ▒░ ░░   ░▒ ░ ░ ░  ░  ░▒ ░ ▒░
    {red} ░ ░  ░ ░ ░ ░ ▒   ░    ░     ░     ░░   ░ 
    {red}   ░        ░ ░   ░    ░     ░  ░   ░     
    {red} ░                                        
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    {INFO} Tool:{red} Dox3R Advanced Search Tool
    {INFO} Author:{red} haisenberg (adapted by Colin)
    {INFO} Description:{red} Advanced doxing tool for finding profiles
    {PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}
    """)

    username = input(f"{INPUT} Enter username {red}->{reset} ").strip()
    if not username:
        ErrorInput()
    
    print(f"\n{SUCCESS} Analysis sent for:{red} {username}{reset}")
    print(f"{LOADING} Analysis in progress, please wait...{reset}")
    time.sleep(1)
    
    # WEBSITE LIST - French version adaptation
    WEBSITES = [
        (f'https://www.instagram.com/{username}', 'Instagram'),
        (f'https://www.facebook.com/{username}', 'Facebook'),
        (f'https://www.twitter.com/{username}', 'Twitter'),
        (f'https://www.youtube.com/{username}', 'YouTube'),
        (f'https://www.reddit.com/user/{username}', 'Reddit'),
        (f'https://{username}.wordpress.com', 'WordPress'),
        (f'https://www.pinterest.com/{username}', 'Pinterest'),
        (f'https://www.github.com/{username}', 'GitHub'),
        (f'https://steamcommunity.com/id/{username}', 'Steam'),
        (f'https://imgur.com/user/{username}', 'Imgur'),
        (f'https://open.spotify.com/user/{username}', 'Spotify'),
        (f'https://www.badoo.com/en/{username}', 'Badoo'),
        (f'https://www.dailymotion.com/{username}', 'Dailymotion'),
        (f'https://keybase.io/{username}', 'Keybase'),
        (f'https://pastebin.com/u/{username}', 'Pastebin'),
        (f'https://www.roblox.com/user.aspx?username={username}', 'Roblox'),
        (f'https://tripadvisor.com/members/{username}', 'TripAdvisor'),
        (f'https://www.wikipedia.org/wiki/User:{username}', 'Wikipedia'),
        (f'https://news.ycombinator.com/user?id={username}', 'HackerNews'),
        (f'https://www.ebay.com/usr/{username}', 'eBay'),
        (f'https://www.tiktok.com/@{username}', 'TikTok'),
        (f'https://www.snapchat.com/add/{username}', 'Snapchat'),
        (f'https://{username}.tumblr.com', 'Tumblr'),
        (f'https://www.twitch.tv/{username}', 'Twitch'),
        (f'https://soundcloud.com/{username}', 'SoundCloud'),
        (f'https://{username}.deviantart.com', 'DeviantArt'),
        (f'https://www.linkedin.com/in/{username}', 'LinkedIn'),
    ]

    # --- SIMPLE SITE CHECKER ---
    def check_site(url, site_name, results, lock):
        try:
            headers = {'User-Agent': RandomUserAgents()}
            r = requests.get(url, headers=headers, timeout=15, verify=False)
            
            if r.status_code == 200:
                # Check if username appears in page content
                if username.lower() in r.text.lower():
                    with lock:
                        results.append((site_name, url, r.status_code, "FOUND"))
                else:
                    with lock:
                        results.append((site_name, url, r.status_code, "EXISTS"))
            elif r.status_code == 404:
                with lock:
                    results.append((site_name, url, r.status_code, "NOT_FOUND"))
            elif r.status_code == 403:
                with lock:
                    results.append((site_name, url, r.status_code, "BLOCKED"))
            elif r.status_code == 429:
                with lock:
                    results.append((site_name, url, r.status_code, "RATE_LIMIT"))
            else:
                with lock:
                    results.append((site_name, url, r.status_code, "ERROR"))
                    
        except requests.exceptions.Timeout:
            with lock:
                results.append((site_name, url, "TIMEOUT", "ERROR"))
        
        except requests.exceptions.ConnectionError:
            with lock:
                results.append((site_name, url, "CONN_ERR", "ERROR"))
        
        except Exception:
            with lock:
                results.append((site_name, url, "EXCEPTION", "ERROR"))

    # --- MAIN SCAN ---
    results = []
    lock = threading.Lock()
    threads = []
    
    total_sites = len(WEBSITES)
    print(f"{LOADING} Scanning {red}{total_sites}{white} websites...{reset}")
    
    for i, (url, site_name) in enumerate(WEBSITES):
        t = threading.Thread(target=check_site, args=(url, site_name, results, lock))
        threads.append(t)
        t.start()
        
        # Progress indicator
        if i % 5 == 0:
            progress = (i + 1) / total_sites * 100
            print(f"{LOADING} Progress: {red}{progress:.1f}%{white} ({i+1}/{total_sites}){reset}", end="\r")
            time.sleep(0.1)
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    print(f"{LOADING} Progress: {red}100.0%{white} ({total_sites}/{total_sites}){reset}")
    
    # --- ORGANIZE RESULTS ---
    found = []
    exists = []
    not_found = []
    blocked = []
    errors = []
    
    for site_name, url, status, result_type in results:
        if result_type == "FOUND":
            found.append((site_name, url, status))
        elif result_type == "EXISTS":
            exists.append((site_name, url, status))
        elif result_type == "NOT_FOUND":
            not_found.append((site_name, url, status))
        elif result_type == "BLOCKED":
            blocked.append((site_name, url, status))
        else:
            errors.append((site_name, url, status))

    # --- DISPLAY RESULTS ---
    print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
    print(f"{red}                     SCAN RESULTS{white}")
    print(f"{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
    
    print(f"{INFO} Statistics:{red}")
    print(f"  • Found (username in page): {len(found)}")
    print(f"  • Profile exists: {len(exists)}")
    print(f"  • Not found: {len(not_found)}")
    print(f"  • Blocked/Access denied: {len(blocked)}")
    print(f"  • Errors: {len(errors)}{reset}")
    
    # FOUND RESULTS
    if found:
        print(f"\n{green}✓ USERNAME FOUND IN CONTENT:{reset}")
        for site_name, url, status in found[:10]:  # Show first 10
            print(f"  {PREFIX}+{SUFFIX} {site_name}: {red}{url}{white} [{status}]")
        if len(found) > 10:
            print(f"  {red}... and {len(found)-10} more{reset}")
    
    # EXISTS BUT NO USERNAME IN CONTENT
    if exists:
        print(f"\n{yellow}⚠ PROFILE EXISTS (check manually):{reset}")
        for site_name, url, status in exists[:5]:
            print(f"  {PREFIX}!{SUFFIX} {site_name}: {red}{url}{white} [{status}]")
        if len(exists) > 5:
            print(f"  {red}... and {len(exists)-5} more{reset}")
    
    # NOT FOUND
    if not_found:
        print(f"\n{red}✗ NOT FOUND:{reset}")
        # Group by status code
        status_groups = {}
        for site_name, url, status in not_found:
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(site_name)
        
        for status, sites in list(status_groups.items())[:3]:
            sites_str = ", ".join(sites[:3])
            if len(sites) > 3:
                sites_str += f" (+{len(sites)-3})"
            print(f"  {PREFIX}-{SUFFIX} HTTP {status}: {red}{sites_str}{reset}")
    
    # BLOCKED
    if blocked:
        print(f"\n{red}⛔ BLOCKED/ACCESS DENIED:{reset}")
        for site_name, url, status in blocked[:3]:
            print(f"  {PREFIX}#{SUFFIX} {site_name}: {red}{url}{white} [{status}]")
    
    # ERRORS
    if errors:
        print(f"\n{yellow}⚠ ERRORS:{reset}")
        error_types = {}
        for site_name, url, status in errors:
            if status not in error_types:
                error_types[status] = []
            error_types[status].append(site_name)
        
        for status, sites in list(error_types.items())[:3]:
            sites_str = ", ".join(sites[:3])
            if len(sites) > 3:
                sites_str += f" (+{len(sites)-3})"
            print(f"  {PREFIX}~{SUFFIX} {status}: {red}{sites_str}{reset}")
    
    print(f"\n{PREFIX1}──────────────────────────────────────────────────────────────{SUFFIX1}")
    
    # Save results
    save = input(f"{INPUT} Save detailed results? {YESORNO} {red}->{reset} ").lower()
    if save == 'y':
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join(tool_path, 'Programs', 'Results')
        filename = os.path.join(results_dir, f'dox3r_scan_{username}_{timestamp}.txt')
        
        os.makedirs(results_dir, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"DOX3R Scan Results\n")
            f.write(f"Target: {username}\n")
            f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total sites scanned: {total_sites}\n")
            f.write("="*60 + "\n\n")
            
            f.write("FOUND (Username in page content):\n")
            for site_name, url, status in found:
                f.write(f"[+] {site_name}: {url} [{status}]\n")
            
            f.write("\nEXISTS (Profile exists):\n")
            for site_name, url, status in exists:
                f.write(f"[!] {site_name}: {url} [{status}]\n")
            
            f.write("\nNOT FOUND:\n")
            for site_name, url, status in not_found:
                f.write(f"[-] {site_name}: {url} [{status}]\n")
            
            f.write("\nBLOCKED/ACCESS DENIED:\n")
            for site_name, url, status in blocked:
                f.write(f"[#] {site_name}: {url} [{status}]\n")
            
            f.write("\nERRORS:\n")
            for site_name, url, status in errors:
                f.write(f"[~] {site_name}: {url} [{status}]\n")
        
        print(f"{SUCCESS} Results saved to:{red} Programs/Results/{os.path.basename(filename)}{reset}")
    
    # Additional options
    print(f"\n{INFO} Additional options:{red}")
    print(f"  1. Scan with email (breach check)")
    print(f"  2. Deep search (more sites)")
    print(f"  3. Back to main menu{reset}")
    
    choice = input(f"{INPUT} Choice {red}->{reset} ").strip()
    
    if choice == "1":
        email = input(f"{INPUT} Enter email for breach check {red}->{reset} ").strip()
        if email:
            print(f"{LOADING} Checking breach data...{reset}")
            try:
                headers = {'User-Agent': RandomUserAgents()}
                r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", headers=headers, timeout=10)
                if r.status_code == 200:
                    breaches = json.loads(r.text)
                    print(f"\n{red}⚠ BREACHES FOUND:{white}")
                    for breach in breaches[:5]:
                        print(f"  {red}•{white} {breach['Name']} - {breach['BreachDate']} ({breach['PwnCount']} accounts)")
                    if len(breaches) > 5:
                        print(f"  {red}... and {len(breaches)-5} more breaches{reset}")
                else:
                    print(f"{SUCCESS} No known breaches found{reset}")
            except:
                print(f"{ERROR} Could not check breaches{reset}")
            Continue()
    
    elif choice == "2":
        print(f"{LOADING} Starting deep search...{reset}")
        # Could add more sites here
        time.sleep(2)
        print(f"{INFO} Deep search feature requires API keys{reset}")
        Continue()
    
    Reset()

if __name__ == "__main__":
    main()