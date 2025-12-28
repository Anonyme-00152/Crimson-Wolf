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


from Programs.Plugins.Utils import *
from Programs.Plugins.Config import *

try:
    import time
    import sys
    import subprocess
    import os
    import requests
except Exception as e:
    MissingModule(e)

Title("Main Menu")

def Connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        pass
    except:
        print(f"{ERROR} An internet connection is required to use {name_tool}-Tool!", reset)
        Continue()
        sys.exit()

Connection()

# Variable globale pour la page actuelle
current_page = 1

def Menu(page=1):
    global current_page
    current_page = page
    
    update = Update()
    
    # DÉBUT DE L'INVERSION : PAGE 1 DEVIENT LES OUTILS OSINT (ancienne page 2)
    if page == 1:
        # NOUVELLE PAGE 1 - OUTILS OSINT (anciennement page 2)
        tools_display = f"""
   ├─ {PREFIX1}01{SUFFIX1} Username-Search                ├─ {PREFIX1}11{SUFFIX1} OSINT-Leakcheck-Searcher       ├─ {PREFIX1}21{SUFFIX1} OSINT-GitHub-Email-Finder
   ├─ {PREFIX1}02{SUFFIX1} Discord-Id-Info                ├─ {PREFIX1}12{SUFFIX1} Leak-Search-Bot                ├─ {PREFIX1}22{SUFFIX1} OSINT-Phone-Lookup-CS
   ├─ {PREFIX1}03{SUFFIX1} OSINT-Menu-Full                ├─ {PREFIX1}13{SUFFIX1} Comming Soon                   ├─ {PREFIX1}23{SUFFIX1} OSINT-WHOIS-Lookup-CS
   ├─ {PREFIX1}04{SUFFIX1} OSINT-DNS-Lookup               ├─ {PREFIX1}14{SUFFIX1} OSINT-GitHub-Info-Searcher     ├─ {PREFIX1}24{SUFFIX1} OSINT-Email-Verifier-CS
   └─ {PREFIX1}05{SUFFIX1} OSINT-Subdomains-Finder        └─ {PREFIX1}15{SUFFIX1} OSINT-All-Websites             └─ {PREFIX1}25{SUFFIX1} OSINT-Email-Breach-Checker-CS"""
        
        navigation_info = f"{red}> Page 1/5 - Type 'n' for Page 2                                                                      {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 2:
        # NOUVELLE PAGE 2 - OUTILS DISCORD (anciennement page 1)
        tools_display = f"""
   ├─ {PREFIX1}31{SUFFIX1} Discord Token Information      ├─ {PREFIX1}41{SUFFIX1} Discord Token House Changer    ├─ {PREFIX1}51{SUFFIX1} Discord Token Mass Dm
   ├─ {PREFIX1}32{SUFFIX1} Discord Token Login            ├─ {PREFIX1}42{SUFFIX1} Discord Token Theme Changer    ├─ {PREFIX1}52{SUFFIX1} Discord Token Delete Dm
   ├─ {PREFIX1}33{SUFFIX1} Discord Token Onliner          ├─ {PREFIX1}43{SUFFIX1} Discord Token Joiner           ├─ {PREFIX1}53{SUFFIX1} Discord Id To Token
   ├─ {PREFIX1}34{SUFFIX1} Discord Token Generator        ├─ {PREFIX1}44{SUFFIX1} Discord Token Leaver           ├─ {PREFIX1}54{SUFFIX1} Discord Snowflake Decoder
   ├─ {PREFIX1}35{SUFFIX1} Discord Token Disabler         ├─ {PREFIX1}45{SUFFIX1} Discord Server Information     ├─ {PREFIX1}55{SUFFIX1} Discord Bot Id To Invite
   ├─ {PREFIX1}36{SUFFIX1} Discord Token Bio Changer      ├─ {PREFIX1}46{SUFFIX1} Discord Token Nuker            ├─ {PREFIX1}56{SUFFIX1} Discord Webhook Information
   ├─ {PREFIX1}37{SUFFIX1} Discord Token Alias Changer    ├─ {PREFIX1}47{SUFFIX1} Discord Token Delete Friends   ├─ {PREFIX1}57{SUFFIX1} Discord Webhook Generator
   ├─ {PREFIX1}38{SUFFIX1} Discord Token CStatus Changer  ├─ {PREFIX1}48{SUFFIX1} Discord Token Block Friends    ├─ {PREFIX1}58{SUFFIX1} Discord Webhook Spammer
   ├─ {PREFIX1}39{SUFFIX1} Discord Token Pfp Changer      ├─ {PREFIX1}49{SUFFIX1} Discord Token Unblock Users    ├─ {PREFIX1}59{SUFFIX1} Discord Webhook Deleter
   └─ {PREFIX1}40{SUFFIX1} Discord Token Language Changer └─ {PREFIX1}50{SUFFIX1} Discord Token Spammer          └─ {PREFIX1}60{SUFFIX1} Discord Nitro Generator"""
        
        navigation_info = f"{red}> Page 2/5 - Type 'n' for Page 3 | 'p' for Page 1                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 3:
        # PAGE 3 - Suite des outils OSINT et autres (inchangée)
        tools_display = f"""
   ├─ {PREFIX1}61{SUFFIX1} OSINT-Instagram-Lookup       ├─ {PREFIX1}66{SUFFIX1} OSINT-Genderize-IO-CS        ├─ {PREFIX1}71{SUFFIX1} Image-Metadata/Exif-Extr
   ├─ {PREFIX1}62{SUFFIX1} OSINT-IP-Informations-metrew ├─ {PREFIX1}67{SUFFIX1} Discord-Server-Information   ├─ {PREFIX1}72{SUFFIX1} Virus Generator
   ├─ {PREFIX1}63{SUFFIX1} Screen-Locker-Builder        ├─ {PREFIX1}68{SUFFIX1} Search-Database              ├─ {PREFIX1}73{SUFFIX1} Comming Soon
   ├─ {PREFIX1}64{SUFFIX1} Simple-Username-Search  AM   ├─ {PREFIX1}69{SUFFIX1} Steganography Tool           ├─ {PREFIX1}74{SUFFIX1} Comming Soon
   └─ {PREFIX1}65{SUFFIX1} Discord-Statut-Rotator       └─ {PREFIX1}70{SUFFIX1} Social Media Account Finder  └─ {PREFIX1}75{SUFFIX1} Comming Soon"""
        
        navigation_info = f"{red}> Page 3/5 - Type 'n' for Page 4 | 'p' for Page 2                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 4:
        # PAGE 4 - COMING SOON (inchangée)
        tools_display = f"""
   ├─ {PREFIX1}76{SUFFIX1} Comming Soon                 ├─ {PREFIX1}81{SUFFIX1} Comming Soon                 ├─ {PREFIX1}86{SUFFIX1} Comming Soon
   ├─ {PREFIX1}77{SUFFIX1} Comming Soon                 ├─ {PREFIX1}82{SUFFIX1} Comming Soon                 ├─ {PREFIX1}87{SUFFIX1} Comming Soon
   ├─ {PREFIX1}78{SUFFIX1} Comming Soon                 ├─ {PREFIX1}83{SUFFIX1} Comming Soon                 ├─ {PREFIX1}88{SUFFIX1} Comming Soon
   ├─ {PREFIX1}79{SUFFIX1} Comming Soon                 ├─ {PREFIX1}84{SUFFIX1} Comming Soon                 ├─ {PREFIX1}89{SUFFIX1} Comming Soon
   └─ {PREFIX1}80{SUFFIX1} Comming Soon                 └─ {PREFIX1}85{SUFFIX1} Comming Soon                 └─ {PREFIX1}90{SUFFIX1} Comming Soon"""
        
        navigation_info = f"{red}> Page 4/5 - Type 'n' for Page 5 | 'p' for Page 3                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    else:  # page == 5
        # PAGE 5 - COMING SOON (inchangée)
        tools_display = f"""
   ├─ {PREFIX1}91{SUFFIX1} Comming Soon                 ├─ {PREFIX1}96{SUFFIX1} Comming Soon                 ├─ {PREFIX1}101{SUFFIX1} Comming Soon
   ├─ {PREFIX1}92{SUFFIX1} Comming Soon                 ├─ {PREFIX1}97{SUFFIX1} Comming Soon                 ├─ {PREFIX1}102{SUFFIX1} Comming Soon
   ├─ {PREFIX1}93{SUFFIX1} Comming Soon                 ├─ {PREFIX1}98{SUFFIX1} Comming Soon                 ├─ {PREFIX1}103{SUFFIX1} Comming Soon
   ├─ {PREFIX1}94{SUFFIX1} Comming Soon                 ├─ {PREFIX1}99{SUFFIX1} Comming Soon                 ├─ {PREFIX1}104{SUFFIX1} Comming Soon
   └─ {PREFIX1}95{SUFFIX1} Comming Soon                 └─ {PREFIX1}100{SUFFIX1} Comming Soon                └─ {PREFIX1}105{SUFFIX1} Comming Soon"""
        
        navigation_info = f"{red}> Page 5/5 - Type 'p' for Page 4                                                                      {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    interface = f"""{update}
    
 ▄████▄   ██▀███   ██▓ ███▄ ▄███▓  ██████  ▒█████   ███▄    █     █     █░ ▒█████   ██▓      █████▒
▒██▀ ▀█  ▓██ ▒ ██▒▓██▒▓██▒▀█▀ ██▒▒██    ▒ ▒██▒  ██▒ ██ ▀█   █    ▓█░ █ ░█░▒██▒  ██▒▓██▒    ▓██   ▒ 
▒▓█    ▄ ▓██ ░▄█ ▒▒██▒▓██    ▓██░░ ▓██▄   ▒██░  ██▒▓██  ▀█ ██▒   ▒█░ █ ░█ ▒██░  ██▒▒██░    ▒████ ░ 
▒▓▓▄ ▄██▒▒██▀▀█▄  ░██░▒██    ▒██   ▒   ██▒▒██   ██░▓██▒  ▐▌██▒   ░█░ █ ░█ ▒██   ██░▒██░    ░▓█▒  ░ 
▒ ▓███▀ ░░██▓ ▒██▒░██░▒██▒   ░██▒▒██████▒▒░ ████▓▒░▒██░   ▓██░   ░░██▒██▓ ░ ████▓▒░░██████▒░▒█░    
░ ░▒ ▒  ░░ ▒▓ ░▒▓░░▓  ░ ▒░   ░  ░▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒    ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒░▓  ░ ▒ ░    
  ░  ▒     ░▒ ░ ▒░ ▒ ░░  ░      ░░ ░▒  ░ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░     ▒ ░ ░    ░ ▒ ▒░ ░ ░ ▒  ░ ░      
░          ░░   ░  ▒ ░░      ░   ░  ░  ░  ░ ░ ░ ▒     ░   ░ ░      ░   ░  ░ ░ ░ ▒    ░ ░    ░ ░    
░ ░         ░      ░         ░         ░      ░ ░           ░        ░        ░ ░      ░  ░        
░                                                                                                  
{navigation_info}
{red}> {PREFIX}!{SUFFIX} Tool Information                                                                                 Tokens File {PREFIX}F{SUFFIX} {red}<
{red}> {PREFIX}?{SUFFIX} {version_tool} Changelog                                                                                 Next Page {PREFIX}N{SUFFIX} {red}<

╓──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╖
                                        {github_url} - Page {page}/5
╙──┬──────────────────────────────────────┬──────────────────────────────────────┬─────────────────────────────────────╜
{tools_display}"""
    
    return interface

# ... [le reste du code reste inchangé jusqu'à la partie while True]

while True:
    try:
        Clear()
        
        interface = Menu(current_page)
        Scroll(Gradient(interface))

        choice = input(f"{PREFIX}{username_pc}@{name_tool}{SUFFIX} {red}->{reset} ").strip().lower()
        
        # Gestion de la navigation entre pages (5 pages)
        if choice == 'n' and current_page < 5:
            current_page += 1
            continue
        elif choice == 'p' and current_page > 1:
            current_page -= 1
            continue
        elif choice == 'e':
            print(f"{LOADING} Exiting {name_tool}..")
            time.sleep(0.5)
            sys.exit()
        
        # NOUVELLES OPTIONS POUR LES PAGES INVERSEES
        
        # Options pour la PAGE 1 (maintenant OSINT)
        if current_page == 1:
            osint_options = {
                # Outils OSINT - Page 1
                '01': "Username-Search", '02': "Discord-Id-Info", '03': "OSINT-Menu-Full",
                '04': "OSINT-DNS-Lookup", '05': "OSINT-Subdomains-Finder", '11': "OSINT-Leakcheck-Searcher",
                '12': "Leak-Search-Bot", '13': "Comming-Soon-13", '14': "OSINT-GitHub-Info-Searcher",
                '15': "OSINT-All-Websites", '21': "OSINT-GitHub-Email-Finder", '22': "OSINT-Phone-Lookup-CS",
                '23': "OSINT-WHOIS-Lookup-CS", '24': "OSINT-Email-Verifier-CS", '25': "OSINT-Email-Breach-Checker-CS",
                '?': "Changelog-Version", '!': "Tool-Information", 'f': "Tokens-File"
            }
            
            if choice in ['?', '!', 'f']:
                StartProgram(osint_options[choice] + '.py')
            elif choice in ['03']:
                leakcheck()
                continue
            elif choice in ['04']:
                ip()
                continue
            elif choice in ['05']:
                launch_gui()
                continue
            elif choice in ['11']:
                StartProgram("Leak-Check-Searcher.py")
                continue
            elif choice in ['12']:
                telegram_bot_search()
                continue
            elif choice in ['14']:
                github_info_search()
                continue
            elif choice in ['15']:
                osint_website_reference()
                continue
            elif choice in ['22']:
                StartProgram("Numinfo.py")
                continue
            elif choice in ['23']:
                whhois()
                continue
            elif choice in ['24']:
                emailverif()
                continue
            elif choice in ['25']:
                mailcompromise()
                continue
            elif choice == '01':
                # Lancer Sherlock DIRECTEMENT
                try:
                    print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
                    print(f"{red}║                 USERNAME SEARCH TOOL                      ║")
                    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
                    
                    username = input(f"{PREFIX}Enter username to search: {reset}").strip()
                    
                    if not username:
                        print(f"\n{ERROR} No username entered!")
                        time.sleep(1.5)
                        continue
                    
                    sherlock_path = r"Programs\sherlock-master\sherlock_project\sherlock.py"
                    
                    if not os.path.exists(sherlock_path):
                        print(f"\n{ERROR} Sherlock not found!")
                        time.sleep(2)
                        continue
                    
                    print(f"\n{LOADING} Searching for '{username}'...\n")
                    
                    command = f'python "{sherlock_path}" "{username}"'
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    print(f"{red}═══════════════════════════════════════════════════════════")
                    print(f"{red}             SEARCH RESULTS FOR: {username}")
                    print(f"{red}═══════════════════════════════════════════════════════════{reset}\n")
                    
                    if result.stdout:
                        lines = result.stdout.split('\n')
                        for i, line in enumerate(lines[:50]):
                            if line.strip():
                                print(line)
                        
                        if len(lines) > 50:
                            print(f"\n{yellow}... and {len(lines)-50} more lines{reset}")
                    elif result.stderr:
                        print(f"{ERROR} Error: {result.stderr[:200]}")
                    else:
                        print(f"{ERROR} No results found.")
                    
                    print(f"\n{red}═══════════════════════════════════════════════════════════")
                    print(f"{red}Press Enter to return to menu...{reset}")
                    input()
                    
                except Exception as e:
                    print(f"\n{ERROR} Failed: {str(e)}")
                    time.sleep(2)
                continue
            elif choice.zfill(2) in osint_options:
                # Pour les autres options OSINT
                option_num = choice.zfill(2)
                if option_num in ['13']:
                    print(f"{ERROR} This feature is coming soon!")
                    time.sleep(1.5)
                else:
                    StartProgram(osint_options[option_num] + '.py')
            else:
                ErrorChoice()
        
        # Options pour la PAGE 2 (maintenant Discord)
        elif current_page == 2:
            discord_options = {
                # Outils Discord - Page 2
                '31': "Discord-Token-Information", '32': "Discord-Token-Login", '33': "Discord-Token-Onliner",
                '34': "Discord-Token-Generator", '35': "Discord-Token-Disabler", '36': "Discord-Token-Bio-Changer",
                '37': "Discord-Token-Alias-Changer", '38': "Discord-Token-CStatus-Changer", '39': "Discord-Token-Pfp-Changer",
                '40': "Discord-Token-Language-Changer", '41': "Discord-Token-House-Changer", '42': "Discord-Token-Theme-Changer",
                '43': "Discord-Token-Joiner", '44': "Discord-Token-Leaver", '45': "Discord-Server-Information",
                '46': "Discord-Token-Nuker", '47': "Discord-Token-Delete-Friends", '48': "Discord-Token-Block-Friends",
                '49': "Discord-Token-Unblock-Users", '50': "Discord-Token-Spammer", '51': "Discord-Token-Mass-Dm",
                '52': "Discord-Token-Delete-Dm", '53': "Discord-Id-To-Token", '54': "Discord-Snowflake-Decoder",
                '55': "Discord-Bot-Id-To-Invite", '56': "Discord-Webhook-Information", '57': "Discord-Webhook-Generator",
                '58': "Discord-Webhook-Spammer", '59': "Discord-Webhook-Deleter", '60': "Discord-Nitro-Generator",
                '?': "Changelog-Version", '!': "Tool-Information", 'f': "Tokens-File"
            }
            
            if choice in ['?', '!', 'f']:
                StartProgram(discord_options[choice] + '.py')
            elif choice.zfill(2) in discord_options:
                StartProgram(discord_options[choice.zfill(2)] + '.py')
            else:
                ErrorChoice()
        
        # Les pages 3, 4, 5 restent inchangées
        elif current_page == 3:
            # ... [code de la page 3 inchangé]
            if choice == '61':
                instagraminfo()
                continue
            elif choice == '62':
                genderiz()
                continue
            elif choice == '63':
                script_path = "Programs/ScreenLocker-Builder/village_builder.py"
                if os.path.exists(script_path):
                    try:
                        if os.name == 'nt':
                            subprocess.run(['python', script_path])
                        else:
                            subprocess.run(['python3', script_path])
                    except:
                        print(f"{ERROR} Failed to launch!")
                else:
                    print(f"{ERROR} File not found!")
                time.sleep(2)
                continue
            elif choice == '64':
                StartProgram("Simple-username-Search.py")
                continue
            elif choice == '65':
                StartProgram("Discord-Statut-Rotator.py")
                continue
            elif choice == '66':
                StartProgram("OSINT-Genderize-IO-CS.py")
                continue
            elif choice == '67':
                StartProgram("Discord-server-information.py")
                continue
            elif choice == '68':
                StartProgram("Search-Database.py")
                continue
            elif choice == '69':
                StartProgram("Steganography-Tool.py")
                continue
            elif choice == '70':
                StartProgram("Social-Media-Account-Finder.py")
                continue
            elif choice == '71':
                StartProgram("Image-Metadata-Extractor.py")
                continue
            elif choice == '72':
                StartProgram("Virus-Builder.py")
                continue
            elif choice.isdigit():
                num_choice = int(choice)
                if 73 <= num_choice <= 75:
                    print(f"{ERROR} This feature is coming soon!")
                    time.sleep(1.5)
                    continue
                else:
                    ErrorChoice()
            else:
                ErrorChoice()
        
        else:  # Pages 4-5
            if choice.isdigit() or choice in ['?', '!', 'f']:
                print(f"{ERROR} This feature is coming soon!")
                time.sleep(1.5)
                continue
            else:
                ErrorChoice()

    except Exception as e:
        Error(e)