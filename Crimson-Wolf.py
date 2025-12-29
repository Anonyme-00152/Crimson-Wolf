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
    
    # Définir le contenu de chaque page
    if page == 1:
        # PAGE 1 - TOUS les outils 01 à 30 (comme avant)
        tools_display = f"""
   ├─ {PREFIX1}01{SUFFIX1} Discord Token Information      ├─ {PREFIX1}11{SUFFIX1} Discord Token House Changer    ├─ {PREFIX1}21{SUFFIX1} Discord Token Mass Dm
   ├─ {PREFIX1}02{SUFFIX1} Discord Token Login            ├─ {PREFIX1}12{SUFFIX1} Discord Token Theme Changer    ├─ {PREFIX1}22{SUFFIX1} Discord Token Delete Dm
   ├─ {PREFIX1}03{SUFFIX1} Discord Token Onliner          ├─ {PREFIX1}13{SUFFIX1} Discord Token Joiner           ├─ {PREFIX1}23{SUFFIX1} Discord Id To Token
   ├─ {PREFIX1}04{SUFFIX1} Discord Token Generator        ├─ {PREFIX1}14{SUFFIX1} Discord Token Leaver           ├─ {PREFIX1}24{SUFFIX1} Discord Snowflake Decoder
   ├─ {PREFIX1}05{SUFFIX1} Discord Token Disabler         ├─ {PREFIX1}15{SUFFIX1} Discord Server Information     ├─ {PREFIX1}25{SUFFIX1} Discord Bot Id To Invite
   ├─ {PREFIX1}06{SUFFIX1} Discord Token Bio Changer      ├─ {PREFIX1}16{SUFFIX1} Discord Token Nuker            ├─ {PREFIX1}26{SUFFIX1} Discord Webhook Information
   ├─ {PREFIX1}07{SUFFIX1} Discord Token Alias Changer    ├─ {PREFIX1}17{SUFFIX1} Discord Token Delete Friends   ├─ {PREFIX1}27{SUFFIX1} Discord Webhook Generator
   ├─ {PREFIX1}08{SUFFIX1} Discord Token CStatus Changer  ├─ {PREFIX1}18{SUFFIX1} Discord Token Block Friends    ├─ {PREFIX1}28{SUFFIX1} Discord Webhook Spammer
   ├─ {PREFIX1}09{SUFFIX1} Discord Token Pfp Changer      ├─ {PREFIX1}19{SUFFIX1} Discord Token Unblock Users    ├─ {PREFIX1}29{SUFFIX1} Discord Webhook Deleter
   └─ {PREFIX1}10{SUFFIX1} Discord Token Language Changer └─ {PREFIX1}20{SUFFIX1} Discord Token Spammer          └─ {PREFIX1}30{SUFFIX1} Discord Nitro Generator"""
        
        navigation_info = f"{red}> Page 1/5 - Type 'n' for Page 2                                                                      {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 2:
        # PAGE 2 - OSINT TOOLS intégrés
        tools_display = f"""
   ├─ {PREFIX1}31{SUFFIX1} Username-Search                ├─ {PREFIX1}36{SUFFIX1} OSINT-Leakcheck-Searcher       ├─ {PREFIX1}41{SUFFIX1} OSINT-GitHub-Email-Finder
   ├─ {PREFIX1}32{SUFFIX1} Discord-Id-Info                ├─ {PREFIX1}37{SUFFIX1} Leak-Search-Bot                ├─ {PREFIX1}42{SUFFIX1} OSINT-Phone-Lookup-CS
   ├─ {PREFIX1}33{SUFFIX1} OSINT-Menu-Full                ├─ {PREFIX1}38{SUFFIX1} Comming Soon                   ├─ {PREFIX1}43{SUFFIX1} OSINT-WHOIS-Lookup-CS
   ├─ {PREFIX1}34{SUFFIX1} OSINT-DNS-Lookup               ├─ {PREFIX1}39{SUFFIX1} OSINT-GitHub-Info-Searcher     ├─ {PREFIX1}44{SUFFIX1} OSINT-Email-Verifier-CS
   └─ {PREFIX1}35{SUFFIX1} OSINT-Subdomains-Finder        └─ {PREFIX1}40{SUFFIX1} OSINT-All-Websites             └─ {PREFIX1}45{SUFFIX1} OSINT-Email-Breach-Checker-CS"""
        
        navigation_info = f"{red}> Page 2/5 - Type 'n' for Page 3 | 'p' for Page 1                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 3:
        # PAGE 3 - Suite des outils OSINT et autres
        tools_display = f"""
   ├─ {PREFIX1}46{SUFFIX1} OSINT-Instagram-Lookup       ├─ {PREFIX1}51{SUFFIX1} OSINT-Genderize-IO-CS        ├─ {PREFIX1}56{SUFFIX1} Image-Metadata/Exif-Extr
   ├─ {PREFIX1}47{SUFFIX1} OSINT-IP-Informations-metrew ├─ {PREFIX1}52{SUFFIX1} Discord-Server-Information   ├─ {PREFIX1}57{SUFFIX1} Virus Generator
   ├─ {PREFIX1}48{SUFFIX1} Screen-Locker-Builder        ├─ {PREFIX1}53{SUFFIX1} Search-Database              ├─ {PREFIX1}58{SUFFIX1} Comming Soon
   ├─ {PREFIX1}49{SUFFIX1} Simple-Username-Search  AM   ├─ {PREFIX1}54{SUFFIX1} Steganography Tool           ├─ {PREFIX1}59{SUFFIX1} Comming Soon
   └─ {PREFIX1}50{SUFFIX1} Discord-Statut-Rotator       └─ {PREFIX1}55{SUFFIX1} Social Media Account Finder  └─ {PREFIX1}60{SUFFIX1} Comming Soon"""
        
        navigation_info = f"{red}> Page 3/5 - Type 'n' for Page 4 | 'p' for Page 2                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    elif page == 4:
        # PAGE 4 - COMING SOON
        tools_display = f"""
   ├─ {PREFIX1}61{SUFFIX1} Comming Soon                 ├─ {PREFIX1}66{SUFFIX1} Comming Soon                 ├─ {PREFIX1}71{SUFFIX1} Comming Soon
   ├─ {PREFIX1}62{SUFFIX1} Comming Soon                 ├─ {PREFIX1}67{SUFFIX1} Comming Soon                 ├─ {PREFIX1}72{SUFFIX1} Comming Soon
   ├─ {PREFIX1}63{SUFFIX1} Comming Soon                 ├─ {PREFIX1}68{SUFFIX1} Comming Soon                 ├─ {PREFIX1}73{SUFFIX1} Comming Soon
   ├─ {PREFIX1}64{SUFFIX1} Comming Soon                 ├─ {PREFIX1}69{SUFFIX1} Comming Soon                 ├─ {PREFIX1}74{SUFFIX1} Comming Soon
   └─ {PREFIX1}65{SUFFIX1} Comming Soon                 └─ {PREFIX1}70{SUFFIX1} Comming Soon                 └─ {PREFIX1}75{SUFFIX1} Comming Soon"""
        
        navigation_info = f"{red}> Page 4/5 - Type 'n' for Page 5 | 'p' for Page 3                                              {white}Exit {name_tool} {PREFIX}E{SUFFIX} {red}<"
    
    else:  # page == 5
        # PAGE 5 - COMING SOON
        tools_display = f"""
   ├─ {PREFIX1}76{SUFFIX1} Comming Soon                 ├─ {PREFIX1}81{SUFFIX1} Comming Soon                 ├─ {PREFIX1}86{SUFFIX1} Comming Soon
   ├─ {PREFIX1}77{SUFFIX1} Comming Soon                 ├─ {PREFIX1}82{SUFFIX1} Comming Soon                 ├─ {PREFIX1}87{SUFFIX1} Comming Soon
   ├─ {PREFIX1}78{SUFFIX1} Comming Soon                 ├─ {PREFIX1}83{SUFFIX1} Comming Soon                 ├─ {PREFIX1}88{SUFFIX1} Comming Soon
   ├─ {PREFIX1}79{SUFFIX1} Comming Soon                 ├─ {PREFIX1}84{SUFFIX1} Comming Soon                 ├─ {PREFIX1}89{SUFFIX1} Comming Soon
   └─ {PREFIX1}80{SUFFIX1} Comming Soon                 └─ {PREFIX1}85{SUFFIX1} Comming Soon                 └─ {PREFIX1}90{SUFFIX1} Comming Soon"""
        
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
# def phonelookup():
#     ascii_art = """
# ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗    ██╗███╗   ██╗███████╗ ██████╗ 
# ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝    ██║████╗  ██║██╔════╝██╔═══██╗
# ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗      ██║██╔██╗ ██║█████╗  ██║   ██║
# ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝      ██║██║╚██╗██║██╔══╝  ██║   ██║
# ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗    ██║██║ ╚████║██║     ╚██████╔╝
# ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
                                                                             
#     """

#     print((ascii_art))
#     phone_number = input(Fore.LIGHTBLUE_EX+"Enter the phone number : ")
#     response = requests.get(f"https://api.numlookupapi.com/v1/validate/{phone_number}?apikey=num_live_pWHeBCRhv2VgqQ9nFOBTaDEDgVsKeHBa6VE6oghz")
#     data = response.json()
#     phone_lookup_result = (
#     f"[*] Valid              : {data.get('valid')}\n"
#     f"[*] Number             : {data.get('number')}\n"
#     f"[*] Local Format       : {data.get('local_format')}\n"
#     f"[*] International      : {data.get('international_format')}\n"
#     f"[*] Country Prefix     : {data.get('country_prefix')}\n"
#     f"[*] Country Code       : {data.get('country_code')}\n"
#     f"[*] Country Name       : {data.get('country_name')}\n"
#     f"[*] Location           : {data.get('location')}\n"
#     f"[*] Carrier            : {data.get('carrier')}\n"
#     f"[*] Line Type          : {data.get('line_type')}"
#     )
#     print()
#     print(phone_lookup_result)
#     print()
#     input("Press enter for return to the menu...")


    
def telegram_bot_search():
    """Display available Telegram OSINT bots with educational disclaimer"""
    
    print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
    print(f"{red}║              TELEGRAM OSINT BOTS SEARCH                   ║")
    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
    
    print(f"{yellow}⚠  IMPORTANT DISCLAIMER ⚠{reset}")
    print(f"   {PREFIX1}1{SUFFIX1} This list is for {yellow}EDUCATIONAL PURPOSES ONLY{reset}")
    print(f"   {PREFIX1}2{SUFFIX1} Respect privacy and applicable laws")
    print(f"   {PREFIX1}3{SUFFIX1} Use at your own risk and responsibility")
    print(f"   {PREFIX1}4{SUFFIX1} Some bots may require payment or have limits\n")
    
    print(f"{green}═══════════════════════════════════════════════════════════")
    print(f"{green}                  AVAILABLE BOTS                          ")
    print(f"{green}═══════════════════════════════════════════════════════════{reset}\n")
    
    # Bot 1: Zebisint Bot
    print(f"   {PREFIX1}01{SUFFIX1} {blue}Zebisint Bot{reset}")
    print(f"   {red}├─ {PREFIX1}Link{SUFFIX1}: {yellow}https://t.me/zebisint_bot{reset}")
    print(f"   {red}├─ {PREFIX1}Trial{SUFFIX1}: {green}1 week free trial{reset}")
    print(f"   {red}├─ {PREFIX1}Credits{SUFFIX1}: {yellow}10,000 credits/day{reset}")
    print(f"   {red}└─ {PREFIX1}Note{SUFFIX1}: {red}After trial: Payment required{reset}\n")
    
    # Bot 2: Intelligence Security Bot
    print(f"   {PREFIX1}02{SUFFIX1} {blue}Intelligence Security Bot{reset}")
    print(f"   {red}├─ {PREFIX1}Link{SUFFIX1}: {yellow}https://t.me/intelligencesecurityiobot{reset}")
    print(f"   {red}├─ {PREFIX1}Type{SUFFIX1}: Multi-purpose OSINT")
    print(f"   {red}└─ {PREFIX1}Status{SUFFIX1}: {green}Active{reset}\n")
    
    # Bot 3: Tixonov Bot
    print(f"   {PREFIX1}03{SUFFIX1} {blue}Tixonov Bot{reset}")
    print(f"   {red}├─ {PREFIX1}Link{SUFFIX1}: {yellow}https://t.me/Tixonov_bot{reset}")
    print(f"   {red}├─ {PREFIX1}Type{SUFFIX1}: Russian OSINT bot")
    print(f"   {red}└─ {PREFIX1}Language{SUFFIX1}: {yellow}Russian/English{reset}\n")
    
    # Bot 4: Sherlook Bot
    print(f"   {PREFIX1}04{SUFFIX1} {blue}Sherlook Bot{reset}")
    print(f"   {red}├─ {PREFIX1}Link{SUFFIX1}: {yellow}https://t.me/Sherlook{reset}")
    print(f"   {red}├─ {PREFIX1}Type{SUFFIX1}: Username search")
    print(f"   {red}└─ {PREFIX1}Features{SUFFIX1}: Cross-platform search\n")
    
    # Bot 5: Additional resources
    print(f"   {PREFIX1}05{SUFFIX1} {blue}Other Resources{reset}")
    print(f"   {red}├─ {PREFIX1}OSINT Framework{SUFFIX1}: https://osintframework.com")
    print(f"   {red}├─ {PREFIX1}GitHub Tools{SUFFIX1}: Sherlock, Maigret")
    print(f"   {red}└─ {PREFIX1}Websites{SUFFIX1}: Whois, Shodan, HaveIBeenPwned\n")
    
    # Usage instructions
    print(f"{yellow}═══════════════════════════════════════════════════════════")
    print(f"{yellow}                  HOW TO USE                             ")
    print(f"{yellow}═══════════════════════════════════════════════════════════{reset}\n")
    
    print(f"   {PREFIX1}1{SUFFIX1} Open Telegram app")
    print(f"   {PREFIX1}2{SUFFIX1} Click on any bot link above")
    print(f"   {PREFIX1}3{SUFFIX1} Press 'Start' or send /start")
    print(f"   {PREFIX1}4{SUFFIX1} Follow bot instructions")
    print(f"   {PREFIX1}5{SUFFIX1} Use commands like /help or /search\n")
    
    # Legal warning
    print(f"{red}═══════════════════════════════════════════════════════════")
    print(f"{red}⚠  LEGAL WARNING ⚠                                      ")
    print(f"{red}═══════════════════════════════════════════════════════════{reset}")
    print(f"   {red}•{reset} Unauthorized access to data is {red}ILLEGAL{reset}")
    print(f"   {red}•{reset} Respect {yellow}privacy laws{reset} (GDPR, CCPA, etc.)")
    print(f"   {red}•{reset} Use only for {green}authorized security testing{reset}")
    print(f"   {red}•{reset} Or {green}your own personal data{reset}")
    print(f"   {red}•{reset} {blue}Ethical hacking principles apply{reset}\n")
    
    # Quick access option
    print(f"{green}═══════════════════════════════════════════════════════════")
    copy_choice = input(f"{PREFIX}Copy a bot link to clipboard? (1-4 or N) {red}->{reset} ").strip()
    
    if copy_choice == '1':
        print(f"{SUCCESS} Link copied: https://t.me/zebisint_bot")
    elif copy_choice == '2':
        print(f"{SUCCESS} Link copied: https://t.me/intelligencesecurityiobot")
    elif copy_choice == '3':
        print(f"{SUCCESS} Link copied: https://t.me/Tixonov_bot")
    elif copy_choice == '4':
        print(f"{SUCCESS} Link copied: https://t.me/Sherlook")
    
    # Auto-return
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    print(f"{LOADING} Returning to menu in 3 seconds...")
    time.sleep(3)
    
def osint_website_reference():
    """Display categorized OSINT websites and tools reference"""
    
    print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
    print(f"{red}║               OSINT WEBSITES & TOOLS REFERENCE            ║")
    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
    
    # Menu display using your tool's styling
    menu_display = f"""
{blue}┌──────────────┐   ┌───────────────┐   ┌───────────────┐
│ {PREFIX1}01{SUFFIX1} Email   │   │ {PREFIX1}03{SUFFIX1} Face     │   │ {PREFIX1}05{SUFFIX1} Username │
│     OSINT    │   │     OSINT     │   │     OSINT     │
│--------------│   │---------------│   │---------------│
│ Email Sites  │   │ Face Sites    │   │ Username Sites│
└──────────────┘   └───────────────┘   └───────────────┘

┌──────────────┐   ┌──────────────┐   ┌───────────────┐
│ {PREFIX1}02{SUFFIX1} IP      │   │ {PREFIX1}04{SUFFIX1} Person  │   │{PREFIX1}06{SUFFIX1} Frameworks│
│     OSINT    │   │     Lookup   │   │               │
│--------------│   │--------------│   │---------------│
│ IP Sites     │   │ Person Sites │   │Framework Sites│
└──────────────┘   └──────────────┘   └───────────────┘

{yellow}────────────────────────────────────────────────────────────────────────────
                     {PREFIX1}07{SUFFIX1} Return to Main Menu
{yellow}────────────────────────────────────────────────────────────────────────────{reset}
"""
    print(menu_display)
    
    try:
        choice = input(f"{PREFIX}Select category (1-7) {red}->{reset} ").strip()
        
        if choice in ["1", "01"]:
            display_email_sites()
        elif choice in ["2", "02"]:
            display_ip_sites()
        elif choice in ["3", "03"]:
            display_face_sites()
        elif choice in ["4", "04"]:
            display_person_sites()
        elif choice in ["5", "05"]:
            display_username_sites()
        elif choice in ["6", "06"]:
            display_framework_sites()
        elif choice in ["7", "07"]:
            print(f"{LOADING} Returning to main menu...")
            time.sleep(1)
            return
        else:
            print(f"{ERROR} Invalid selection!")
            time.sleep(1.5)
            osint_website_reference()
            
    except KeyboardInterrupt:
        print(f"\n{ERROR} Operation cancelled.")
        return
def github_info_search():
    """GitHub User Information Searcher"""
    
    print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
    print(f"{red}║                GITHUB USER INFORMATION                    ║")
    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
    
    try:
        # Get username
        target = input(f"{PREFIX}Enter GitHub username {red}->{reset} ").strip()
        
        if not target:
            print(f"{ERROR} No username provided!")
            time.sleep(1.5)
            return
        
        print(f"\n{LOADING} Fetching GitHub data for '{target}'...")
        
        # API request
        url = f"https://api.github.com/users/{target}"
        headers = {
            'User-Agent': f'{name_tool}-Tool/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            print(f"{ERROR} User '{target}' not found on GitHub!")
            time.sleep(2)
            return
        elif response.status_code == 403:
            print(f"{ERROR} GitHub API rate limit exceeded. Try again later.")
            time.sleep(2)
            return
        elif response.status_code != 200:
            print(f"{ERROR} GitHub API error: Status {response.status_code}")
            time.sleep(2)
            return
        
        data = response.json()
        
        # Extract data
        login = data.get('login', 'N/A')
        user_id = data.get('id', 'N/A')
        avatar_url = data.get('avatar_url', 'N/A')
        bio = data.get('bio', 'N/A')
        location = data.get('location', 'N/A')
        public_repos = data.get('public_repos', 'N/A')
        twitter_username = data.get('twitter_username', 'N/A')
        followers = data.get('followers', 'N/A')
        following = data.get('following', 'N/A')
        created_at = data.get('created_at', 'N/A')
        updated_at = data.get('updated_at', 'N/A')
        company = data.get('company', 'N/A')
        blog = data.get('blog', 'N/A')
        email = data.get('email', 'N/A')
        
        # Display results
        print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
        print(f"{green}║                  GITHUB PROFILE INFO                      ║")
        print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
        
        # Display in table format
        print(f"{red}┌─────────────────────────────────────────────────────────┐")
        print(f"{red}│                BASIC INFORMATION                       │")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│ {PREFIX1}Username{SUFFIX1}: {yellow}{login}{reset}")
        print(f"{red}│ {PREFIX1}User ID{SUFFIX1}: {user_id}{reset}")
        print(f"{red}│ {PREFIX1}Profile URL{SUFFIX1}: {blue}https://github.com/{login}{reset}")
        
        if avatar_url != 'N/A':
            print(f"{red}│ {PREFIX1}Avatar{SUFFIX1}: {avatar_url}{reset}")
        
        if bio != 'N/A' and bio:
            bio_display = bio[:50] + "..." if len(bio) > 50 else bio
            print(f"{red}│ {PREFIX1}Bio{SUFFIX1}: {bio_display}{reset}")
        
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│                LOCATION & CONTACT                      │")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        
        if location != 'N/A':
            print(f"{red}│ {PREFIX1}Location{SUFFIX1}: {location}{reset}")
        
        if company != 'N/A':
            print(f"{red}│ {PREFIX1}Company{SUFFIX1}: {company}{reset}")
        
        if blog != 'N/A':
            print(f"{red}│ {PREFIX1}Website{SUFFIX1}: {blue}{blog}{reset}")
        
        if twitter_username != 'N/A':
            print(f"{red}│ {PREFIX1}Twitter{SUFFIX1}: @{twitter_username}{reset}")
        
        if email != 'N/A':
            print(f"{red}│ {PREFIX1}Email{SUFFIX1}: {blue}{email}{reset}")
        
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│                STATISTICS                              │")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│ {PREFIX1}Public Repos{SUFFIX1}: {green}{public_repos}{reset}")
        print(f"{red}│ {PREFIX1}Followers{SUFFIX1}: {green}{followers}{reset}")
        print(f"{red}│ {PREFIX1}Following{SUFFIX1}: {following}{reset}")
        
        # Calculate account age if possible
        if created_at != 'N/A':
            try:
                from datetime import datetime
                created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                now = datetime.now()
                years = now.year - created.year
                months = now.month - created.month
                if months < 0:
                    years -= 1
                    months += 12
                print(f"{red}│ {PREFIX1}Account Age{SUFFIX1}: ~{years} years, {months} months{reset}")
            except:
                print(f"{red}│ {PREFIX1}Created{SUFFIX1}: {created_at}{reset}")
        
        print(f"{red}└─────────────────────────────────────────────────────────┘{reset}")
        
        # Additional insights
        print(f"\n{yellow}═══════════════════════════════════════════════════════════")
        print(f"{yellow}💡 INSIGHTS & ANALYSIS                               ")
        print(f"{yellow}═══════════════════════════════════════════════════════════{reset}")
        
        # Calculate follower ratio
        if followers != 'N/A' and following != 'N/A' and followers > 0 and following > 0:
            try:
                ratio = followers / following
                if ratio > 5:
                    print(f"   {PREFIX1}•{SUFFIX1} High influence: {yellow}Many followers relative to following{reset}")
                elif ratio < 0.2:
                    print(f"   {PREFIX1}•{SUFFIX1} Curator: {blue}Follows many users{reset}")
            except:
                pass
        
        if public_repos != 'N/A' and int(public_repos) > 50:
            print(f"   {PREFIX1}•{SUFFIX1} Active developer: {green}Many public repositories{reset}")
        
        if bio != 'N/A' and len(bio) > 100:
            print(f"   {PREFIX1}•{SUFFIX1} Detailed profile: {yellow}Comprehensive bio{reset}")
        
        # Save option
        print(f"\n{red}═══════════════════════════════════════════════════════════")
        save = input(f"{PREFIX}Save profile to file? (Y/N) {red}->{reset} ").strip().lower()
        
        if save in ['y', 'yes']:
            filename = f"GitHub_Profile_{login}.txt"
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"GitHub Profile: {login}\n")
                    file.write(f"{'='*50}\n")
                    file.write(f"User ID: {user_id}\n")
                    file.write(f"Profile: https://github.com/{login}\n")
                    file.write(f"Avatar: {avatar_url}\n")
                    file.write(f"Bio: {bio}\n")
                    file.write(f"Location: {location}\n")
                    file.write(f"Company: {company}\n")
                    file.write(f"Website: {blog}\n")
                    file.write(f"Twitter: {twitter_username}\n")
                    file.write(f"Email: {email}\n")
                    file.write(f"\nStatistics:\n")
                    file.write(f"- Public Repositories: {public_repos}\n")
                    file.write(f"- Followers: {followers}\n")
                    file.write(f"- Following: {following}\n")
                    file.write(f"- Account Created: {created_at}\n")
                    file.write(f"- Last Updated: {updated_at}\n")
                    file.write(f"\nReport Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"Tool: {name_tool}\n")
                
                print(f"{SUCCESS} Profile saved to: {filename}")
                time.sleep(1)
            except Exception as e:
                print(f"{ERROR} Save failed: {str(e)}")
        
        # Quick links
        print(f"\n{blue}═══════════════════════════════════════════════════════════")
        print(f"{blue}🔗 QUICK LINKS                                         ")
        print(f"{blue}═══════════════════════════════════════════════════════════{reset}")
        print(f"   {PREFIX1}1{SUFFIX1} {yellow}GitHub Profile{reset}: https://github.com/{login}")
        if twitter_username != 'N/A':
            print(f"   {PREFIX1}2{SUFFIX1} {blue}Twitter Profile{reset}: https://twitter.com/{twitter_username}")
        
    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out.")
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Invalid API response.")
    except KeyboardInterrupt:
        print(f"\n{ERROR} Operation cancelled.")
    except Exception as e:
        print(f"{ERROR} Error: {str(e)}")
    
    # Auto-return
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    print(f"{LOADING} Returning to menu in 3 seconds...")
    time.sleep(3)
    
def display_email_sites():
    """Display Email OSINT websites"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║                  EMAIL OSINT SITES                        ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    email_sites = [
        "https://epieos.com",
        "https://haveibeenpwned.com",
        "https://emailrep.io",
        "https://hunter.io",
        "https://leakcheck.io",
        "https://snusbase.com",
        "https://dehashed.com"
    ]
    
    print(f"   {PREFIX1}Total Sites{SUFFIX1}: {len(email_sites)}\n")
    
    for i, site in enumerate(email_sites, 1):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {yellow}{site}{reset}")
    
    # Quick actions
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    action = input(f"{PREFIX}Copy URL (1-7) or Press Enter to return {red}->{reset} ").strip()
    
    if action.isdigit() and 1 <= int(action) <= len(email_sites):
        selected = email_sites[int(action)-1]
        print(f"{SUCCESS} URL ready: {selected}")
        # Optional: Add clipboard copy functionality here
        time.sleep(1)
    
    print(f"\n{LOADING} Returning to OSINT sites menu...")
    time.sleep(1.5)
    osint_website_reference()

def display_ip_sites():
    """Display IP OSINT websites"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║                    IP OSINT SITES                         ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    ip_sites = [
        "https://www.shodan.io",
        "https://ipinfo.io",
        "https://portscanner.online",
        "https://www.abuseipdb.com",
        "https://search.censys.io",
        "https://threatfox.abuse.ch"
    ]
    
    print(f"   {PREFIX1}Total Sites{SUFFIX1}: {len(ip_sites)}\n")
    
    for i, site in enumerate(ip_sites, 1):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {yellow}{site}{reset}")
    
    print(f"\n{yellow}═══════════════════════════════════════════════════════════")
    print(f"{yellow}💡 Tip: Shodan and Censys are powerful for device search")
    print(f"{yellow}═══════════════════════════════════════════════════════════{reset}")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    input(f"{PREFIX}Press Enter to return {red}->{reset} ")
    osint_website_reference()

def display_face_sites():
    """Display Face Recognition OSINT websites"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║                  FACE OSINT SITES                         ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    face_sites = [
        "https://pimeyes.com/en",
        "https://yandex.com/images",
        "https://facecheck.id"
    ]
    
    print(f"   {PREFIX1}Total Sites{SUFFIX1}: {len(face_sites)}\n")
    
    for i, site in enumerate(face_sites, 1):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {yellow}{site}{reset}")
    
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    print(f"{red}⚠  PRIVACY WARNING                                       ")
    print(f"{red}═══════════════════════════════════════════════════════════{reset}")
    print(f"   {PREFIX1}•{SUFFIX1} Use face search tools {yellow}ethically{reset}")
    print(f"   {PREFIX1}•{SUFFIX1} Respect individuals' {green}privacy rights{reset}")
    print(f"   {PREFIX1}•{SUFFIX1} Comply with local {blue}laws and regulations{reset}")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    input(f"{PREFIX}Press Enter to return {red}->{reset} ")
    osint_website_reference()

def display_person_sites():
    """Display Person Lookup OSINT websites"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║                PERSON LOOKUP SITES                        ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    person_sites = [
        "https://www.pagesjaunes.fr",
        "https://webmii.com",
        "https://www.idcrawl.com",
        "https://www.whitepages.com",
        "https://www.truepeoplesearch.com",
        "https://www.peekyou.com"
    ]
    
    print(f"   {PREFIX1}Total Sites{SUFFIX1}: {len(person_sites)}\n")
    
    for i, site in enumerate(person_sites, 1):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {yellow}{site}{reset}")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    region = input(f"{PREFIX}Filter by region? (US/EU/ALL) {red}->{reset} ").strip().upper()
    
    if region == "US":
        print(f"\n{PREFIX1}US-focused sites{SUFFIX1}:")
        us_sites = [s for s in person_sites if "whitepages" in s or "truepeople" in s or "peekyou" in s]
        for site in us_sites:
            print(f"   {red}•{reset} {site}")
    elif region == "EU":
        print(f"\n{PREFIX1}EU-focused sites{SUFFIX1}:")
        eu_sites = [s for s in person_sites if "pagesjaunes" in s or "webmii" in s]
        for site in eu_sites:
            print(f"   {red}•{reset} {site}")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    input(f"{PREFIX}Press Enter to return {red}->{reset} ")
    osint_website_reference()

def display_username_sites():
    """Display Username OSINT websites and tools"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║               USERNAME OSINT RESOURCES                    ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    username_resources = [
        "https://whatsmyname.app",
        "https://www.namecheckr.com",
        "https://usersearch.org",
        "https://github.com/sherlock-project/sherlock (CLI Tool)",
        "https://github.com/soxoj/maigret (CLI Tool)"
    ]
    
    print(f"   {PREFIX1}Websites{SUFFIX1}:")
    for i, site in enumerate(username_resources[:3], 1):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {yellow}{site}{reset}")
    
    print(f"\n   {PREFIX1}Command Line Tools{SUFFIX1}:")
    for i, tool in enumerate(username_resources[3:], 4):
        print(f"   {red}├─ {PREFIX1}{i:02d}{SUFFIX1} {blue}{tool}{reset}")
    
    print(f"\n{yellow}═══════════════════════════════════════════════════════════")
    print(f"{yellow}💡 Sherlock & Maigret are powerful Python tools[citation:5]")
    print(f"{yellow}═══════════════════════════════════════════════════════════{reset}")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    input(f"{PREFIX}Press Enter to return {red}->{reset} ")
    osint_website_reference()

def display_framework_sites():
    """Display OSINT Framework websites"""
    print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
    print(f"{green}║               OSINT FRAMEWORKS & TOOLS                    ║")
    print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
    
    frameworks = [
        "https://osintframework.com",
        "https://www.maltego.com",
        "https://www.spiderfoot.net",
        "https://github.com/lanmaster53/recon-ng (CLI Framework)"
    ]
    
    print(f"   {PREFIX1}Total Resources{SUFFIX1}: {len(frameworks)}\n")
    
    for i, framework in enumerate(frameworks, 1):
        prefix = f"{PREFIX1}{i:02d}{SUFFIX1}"
        if "github.com" in framework:
            print(f"   {red}├─ {prefix} {blue}{framework}{reset}")
        else:
            print(f"   {red}├─ {prefix} {yellow}{framework}{reset}")
    
    print(f"\n{yellow}═══════════════════════════════════════════════════════════")
    print(f"{yellow}🌟 Featured: Recon-ng is a powerful modular framework[citation:5]")
    print(f"{yellow}═══════════════════════════════════════════════════════════{reset}")
    
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    print(f"{red}⚠  LEGAL DISCLAIMER                                      ")
    print(f"{red}═══════════════════════════════════════════════════════════{reset}")
    print(f"   {PREFIX1}•{SUFFIX1} Use OSINT tools for {green}authorized purposes{reset} only")
    print(f"   {PREFIX1}•{SUFFIX1} Respect {yellow}terms of service{reset} of all platforms")
    print(f"   {PREFIX1}•{SUFFIX1} Comply with {blue}data protection laws{reset} (GDPR, etc.)")
    
    print(f"\n{blue}═══════════════════════════════════════════════════════════")
    save = input(f"{PREFIX}Save this list to file? (Y/N) {red}->{reset} ").strip().lower()
    
    if save in ['y', 'yes']:
        try:
            filename = f"OSINT_Frameworks_{int(time.time())}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("OSINT Frameworks & Tools Reference\n")
                f.write("="*50 + "\n\n")
                for framework in frameworks:
                    f.write(f"• {framework}\n")
                f.write(f"\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Tool: {name_tool}\n")
            print(f"{SUCCESS} List saved to: {filename}")
            time.sleep(1)
        except Exception as e:
            print(f"{ERROR} Failed to save: {str(e)}")
    
    print(f"\n{LOADING} Returning to OSINT sites menu...")
    time.sleep(1)
    osint_website_reference()
        
def StartSherlock():
    """Lance le script Sherlock pour la recherche d'usernames DIRECTEMENT dans l'interface"""
    try:
        # Afficher directement sous l'interface
        print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
        print(f"{red}║                 USERNAME SEARCH TOOL                      ║")
        print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
        
        # Demander le username directement
        username = input(f"{PREFIX}Enter username to search: {reset}").strip()
        
        if not username:
            print(f"\n{ERROR} No username entered!")
            time.sleep(1.5)
            return
        
        # Chemin vers le script Sherlock
        sherlock_path = r"Programs\sherlock-master\sherlock_project\sherlock.py"
        
        # Vérifier si Sherlock existe
        if not os.path.exists(sherlock_path):
            print(f"\n{ERROR} Sherlock not found at: {sherlock_path}")
            print(f"{yellow}Make sure Sherlock is installed in Programs/sherlock-master/{reset}")
            time.sleep(2)
            return
        
        # Afficher le message de recherche
        print(f"\n{LOADING} Searching for '{username}' across social networks...")
        print(f"{yellow}This may take a few moments...{reset}\n")
        
        # Construire et exécuter la commande Sherlock
        command = f'python "{sherlock_path}" "{username}"'
        
        # Exécuter Sherlock
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Afficher les résultats
        print(f"{red}═══════════════════════════════════════════════════════════")
        print(f"{red}             SEARCH RESULTS FOR: {username}")
        print(f"{red}═══════════════════════════════════════════════════════════{reset}\n")
        
        if result.stdout:
            # Limiter l'affichage pour ne pas dépasser
            lines = result.stdout.split('\n')
            for i, line in enumerate(lines[:50]):  # Afficher seulement 50 lignes max
                if line.strip():
                    print(line)
            
            if len(lines) > 50:
                print(f"\n{yellow}... and {len(lines)-50} more lines (truncated){reset}")
        
        elif result.stderr:
            print(f"{ERROR} Error occurred during search:")
            print(result.stderr)
        else:
            print(f"{ERROR} No results found.")
        
        # Attendre avant de retourner au menu
        print(f"\n{red}═══════════════════════════════════════════════════════════")
        print(f"{red}Press Enter to return to menu...{reset}")
        input()
        
    except Exception as e:
        print(f"\n{ERROR} Failed to run Sherlock: {str(e)}")
        time.sleep(2)

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
        
            
        # Options pour toutes les pages
        options = {
            # Page 1 - Outils Discord
            '01': "Discord-Token-Information",      '11': "Discord-Token-House-Changer",  '21': "Discord-Token-Mass-Dm",       '?': "Changelog-Version",
            '02': "Discord-Token-Login",            '12': "Discord-Token-Theme-Changer",  '22': "Discord-Token-Delete-Dm",     '!': "Tool-Information",
            '03': "Discord-Token-Onliner",          '13': "Discord-Token-Joiner",         '23': "Discord-Id-To-Token",         'f': "Tokens-File",
            '04': "Discord-Token-Generator",        '14': "Discord-Token-Leaver",         '24': "Discord-Snowflake-Decoder",
            '05': "Discord-Token-Disabler",         '15': "Discord-Server-Information",   '25': "Discord-Bot-Id-To-Invite",
            '06': "Discord-Token-Bio-Changer",      '16': "Discord-Token-Nuker",          '26': "Discord-Webhook-Information",
            '07': "Discord-Token-Alias-Changer",    '17': "Discord-Token-Delete-Friends", '27': "Discord-Webhook-Generator",
            '08': "Discord-Token-CStatus-Changer",  '18': "Discord-Token-Block-Friends",  '28': "Discord-Webhook-Spammer",
            '09': "Discord-Token-Pfp-Changer",      '19': "Discord-Token-Unblock-Users",  '29': "Discord-Webhook-Deleter",
            '10': "Discord-Token-Language-Changer", '20': "Discord-Token-Spammer",        '30': "Discord-Nitro-Generator",
            '31': "Username-Search",                '32': "Discord-Id-Info",              
        }

        special_choices = ['?', '!', 'f']
        
        # Gestion des choix selon la page
        if current_page == 1:
            # Page 1 - Outils Discord normaux
            if choice in special_choices:
                StartProgram(options[choice] + '.py')
            elif choice.zfill(2) in options:
                StartProgram(options[choice.zfill(2)] + '.py')
            else:
                ErrorChoice()
        
        elif current_page == 2:
            # Page 2 - Gestion de tous les outils OSINT et autres
            # Traite d'abord les choix spécifiques
            if choice == '31':
                # Lancer Sherlock DIRECTEMENT dans l'interface actuelle
                StartSherlock()
                continue
            elif choice == '32':
                # Lancer Discord-Id-Info
                StartProgram("Discord-Id-Info.py")
                continue
            elif choice == '42':
                # Lancer Numinfo
                StartProgram("Numinfo.py")
                continue
            elif choice == '48':
                # Lancer Screen-Locker-Builder
                script_path = "Programs/ScreenLocker-Builder/village_builder.py"
                
                if os.path.exists(script_path):
                    try:
                        if os.name == 'nt':
                            subprocess.run(['python', script_path])
                        else:
                            subprocess.run(['python3', script_path])
                    except:
                        print(f"{ERROR} Failed to launch: {script_path}")
                else:
                    print(f"{ERROR} File not found: {script_path}")
                    print(f"{yellow}Create the file at: {script_path}{reset}")
                
                time.sleep(2)
                continue
            elif choice == '33':
                leakcheck()
                continue
            elif choice == '34':
                ip()
                continue
            elif choice == '35':
                launch_gui()
                continue
            elif choice == '36':
                # Lancer Leak-Check-Searcher
                StartProgram("Leak-Check-Searcher.py")
                continue
            elif choice == '37':
                telegram_bot_search()
                continue
            elif choice == '39':
                github_info_search()
                continue
            elif choice == '41':
                # Lancer GitHub-Email-Finder
                StartProgram("github-email-finder.py")
                continue
            elif choice == '40':
                osint_website_reference()
                continue
            elif choice == '43':
                whhois()
                continue
            elif choice == '44':
                emailverif()
                continue
            elif choice == '45':
                mailcompromise()
                continue
            elif choice == '46':
                instagraminfo()
                continue
            elif choice == '47':
                genderiz()
                continue
            elif choice in special_choices:
                StartProgram(options[choice] + '.py')
                continue
            
            # Ensuite, vérifie si c'est un autre nombre dans la plage de la page 2
            elif choice.isdigit():
                num_choice = int(choice)
                # Vérifie si c'est un numéro d'option valide pour la page 2
                # Mais PAS ceux déjà traités ci-dessus
                handled_numbers = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]
                if 31 <= num_choice <= 48 and num_choice not in handled_numbers:
                    print(f"{ERROR} This feature is coming soon!")
                    time.sleep(1.5)
                    continue
                else:
                    # Si c'est un nombre mais pas dans la plage traitée ou déjà géré
                    ErrorChoice()
            else:
                ErrorChoice()
        
        elif current_page == 3:
            
            if choice == '49':
                # Lancer Numinfo
                StartProgram("Simple-username-Search.py")
                continue
            if choice == '55':
                # Lancer Numinfo
                StartProgram("Social-Media-Account-Finder.py")
                continue
            if choice == '56':
                # Lancer Numinfo
                StartProgram("Image-Metadata-Extractor.py")
                continue
            if choice == '57':
                # Lancer Numinfo
                StartProgram("Virus-Builder.py")
                continue
            if choice == '50':
                # Lancer Numinfo
                StartProgram("Discord-Statut-Rotator.py")
                continue
            if choice == '54':
                # Lancer Numinfo
                StartProgram("Steganography-Tool.py")
                continue
            if choice == '52':
                # Lancer Numinfo
                StartProgram("Discord-server-information.py")
                continue
            if choice == '53':
                # Lancer Numinfo
                StartProgram("Search-Database.py")
                continue
            
            # Page 3 - Gestion des options 46 à 60
            if choice == '48':
                # Lancer Screen-Locker-Builder
                script_path = "Programs/ScreenLocker-Builder/village_builder.py"
                
                print(f"\n{LOADING} Launching ScreenLocker Builder...")
                print(f"{PREFIX} Path: {script_path}")
                
                if os.path.exists(script_path):
                    try:
                        if os.name == 'nt':
                            subprocess.run(['python', script_path], check=True)
                        else:
                            os.chmod(script_path, 0o755)
                            subprocess.run(['python3', script_path], check=True)
                        
                        print(f"\n{SUCCESS} ScreenLocker Builder completed")
                    except Exception as e:
                        print(f"{ERROR} Execution failed: {e}")
                else:
                    print(f"{ERROR} File not found: {script_path}")
                
                input(f"\n{PREFIX} Press Enter to continue...")
                continue
            elif choice.isdigit():
                num_choice = int(choice)
                if 46 <= num_choice <= 60:
                    print(f"{ERROR} This feature is coming soon!")
                    time.sleep(1.5)
                    continue
                else:
                    ErrorChoice()
            else:
                ErrorChoice()
        
        else:
            # Pages 4-5 - Coming Soon
            if choice.isdigit() or choice in special_choices:
                print(f"{ERROR} This feature is coming soon!")
                time.sleep(1.5)
                continue
            else:
                ErrorChoice()

    except Exception as e:
        Error(e)