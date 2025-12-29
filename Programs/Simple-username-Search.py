import os
import sys
import time
import json
import threading
import concurrent.futures
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from deep_translator import GoogleTranslator
from pystyle import Colors, Colorate, Center
import requests
from bs4 import BeautifulSoup
import dns.resolver
import whois
import socket

class AdvancedUsernameOSINT:
    def __init__(self):
        self.results = {}
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
        
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def banner(self):
        banner_text = """
╔══════════════════════════════════════════════════════════╗
║               ADVANCED USERNAME OSINT TOOL              ║
║                    ULTIMATE EDITION                      ║
╚══════════════════════════════════════════════════════════╝
        """
        print(Colorate.Horizontal(Colors.red_to_blue, Center.XCenter(banner_text)))
        
    def setup_driver(self, browser_type="chrome"):
        try:
            if browser_type == "chrome":
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
            elif browser_type == "firefox":
                firefox_options = FirefoxOptions()
                firefox_options.add_argument("--headless")
                self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
                
            elif browser_type == "edge":
                edge_options = EdgeOptions()
                edge_options.add_argument("--headless")
                self.driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(), options=edge_options)
                
            self.driver.set_window_size(1920, 1080)
            return True
        except Exception as e:
            print(f"{Colors.red}Driver setup failed: {e}")
            return False
            
    def guns_lol_search(self, username):
        try:
            url = f"https://guns.lol/{username}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check for user existence patterns
                not_found_indicators = ["not found", "doesn't exist", "404", "no user"]
                page_text = soup.get_text().lower()
                
                if any(indicator in page_text for indicator in not_found_indicators):
                    return False
                    
                # Extract additional information
                user_data = {
                    "url": url,
                    "profile_exists": True,
                    "page_title": soup.title.string if soup.title else None,
                    "metadata": {}
                }
                
                # Look for meta tags
                for meta in soup.find_all('meta'):
                    if meta.get('name'):
                        user_data['metadata'][meta.get('name')] = meta.get('content')
                    if meta.get('property'):
                        user_data['metadata'][meta.get('property')] = meta.get('content')
                        
                return user_data
            return False
        except Exception as e:
            return f"Error: {e}"
            
    def advanced_tiktok_search(self, username):
        try:
            # Multiple TikTok URL patterns
            urls = [
                f"https://www.tiktok.com/@{username}",
                f"https://tiktok.com/@{username}",
                f"https://vm.tiktok.com/{username}"
            ]
            
            for url in urls:
                self.driver.get(url)
                time.sleep(3)
                
                # Check multiple existence indicators
                page_source = self.driver.page_source.lower()
                
                if "cannot be found" in page_source or "doesn't exist" in page_source or "404" in page_source:
                    continue
                    
                # Extract profile data
                try:
                    scripts = self.driver.find_elements(By.TAG_NAME, 'script')
                    for script in scripts:
                        if 'SIGI_STATE' in script.get_attribute('innerHTML'):
                            data = script.get_attribute('innerHTML')
                            start = data.find('{')
                            end = data.rfind('}') + 1
                            json_data = json.loads(data[start:end])
                            return {
                                "url": url,
                                "user_data": json_data.get('UserModule', {}),
                                "stats": json_data.get('UserModule', {}).get('stats', {})
                            }
                except:
                    pass
                    
                return {"url": url, "status": "exists"}
                
            return False
        except Exception as e:
            return f"Error: {e}"
            
    def deep_instagram_search(self, username):
        try:
            url = f"https://www.instagram.com/{username}/?__a=1&__d=dis"
            headers = {
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "url": f"https://instagram.com/{username}",
                    "user_data": data.get('graphql', {}).get('user', {}),
                    "is_private": data.get('graphql', {}).get('user', {}).get('is_private', False),
                    "follower_count": data.get('graphql', {}).get('user', {}).get('edge_followed_by', {}).get('count', 0)
                }
            return False
        except Exception as e:
            return f"Error: {e}"
            
    def domain_intelligence(self, username):
        try:
            domains_to_check = [
                f"{username}.com",
                f"{username}.net",
                f"{username}.org",
                f"{username}.io"
            ]
            
            domain_results = {}
            
            for domain in domains_to_check:
                try:
                    # DNS resolution
                    answers = dns.resolver.resolve(domain, 'A')
                    ip_addresses = [str(rdata) for rdata in answers]
                    
                    # WHOIS lookup
                    w = whois.whois(domain)
                    
                    domain_results[domain] = {
                        "exists": True,
                        "ip_addresses": ip_addresses,
                        "whois": {
                            "registrar": w.registrar,
                            "creation_date": w.creation_date,
                            "expiration_date": w.expiration_date
                        }
                    }
                except:
                    domain_results[domain] = {"exists": False}
                    
            return domain_results
        except Exception as e:
            return f"Error: {e}"
            
    def email_search(self, username):
        try:
            # Check common email providers
            email_providers = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
            email_results = {}
            
            for provider in email_providers:
                email = f"{username}@{provider}"
                
                # Simple verification attempts
                verification_urls = {
                    'gmail.com': f"https://mail.google.com/mail/gxlu?email={email}",
                    'outlook.com': f"https://login.live.com/login.srf?email={email}"
                }
                
                if provider in verification_urls:
                    response = self.session.head(verification_urls[provider], allow_redirects=False)
                    email_results[email] = {
                        "exists": response.status_code in [200, 302],
                        "verification_method": "http_header"
                    }
                else:
                    email_results[email] = {"exists": "unknown"}
                    
            return email_results
        except Exception as e:
            return f"Error: {e}"
            
    def concurrent_search(self, username, platforms):
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_platform = {}
            
            # Add all search functions
            search_functions = {
                'guns_lol': lambda: self.guns_lol_search(username),
                'tiktok': lambda: self.advanced_tiktok_search(username),
                'instagram': lambda: self.deep_instagram_search(username),
                'domains': lambda: self.domain_intelligence(username),
                'emails': lambda: self.email_search(username),
                'github': lambda: self.github_search(username),
                'twitter': lambda: self.twitter_search(username),
                'reddit': lambda: self.reddit_search(username),
                'telegram': lambda: self.telegram_search(username),
                'snapchat': lambda: self.snapchat_search(username)
            }
            
            for platform in platforms:
                if platform in search_functions:
                    future = executor.submit(search_functions[platform])
                    future_to_platform[future] = platform
                    
            for future in concurrent.futures.as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    results[platform] = future.result()
                except Exception as e:
                    results[platform] = f"Error: {e}"
                    
        return results
        
    def generate_report(self, username, results):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osint_report_{username}_{timestamp}.json"
        
        report = {
            "username": username,
            "timestamp": timestamp,
            "search_results": results,
            "summary": {
                "platforms_found": sum(1 for r in results.values() if r and r != False and not isinstance(r, str) or (isinstance(r, dict) and r.get('url'))),
                "total_checks": len(results)
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4, default=str)
            
        return filename
        
    def display_results(self, username, results):
        self.clear()
        self.banner()
        
        print(f"\n{Colors.blue}[+] OSINT Results for: {Colors.green}{username}\n")
        print(f"{Colors.yellow}{'='*60}")
        
        for platform, result in results.items():
            if result and result != False and not isinstance(result, str):
                if isinstance(result, dict) and 'url' in result:
                    print(f"{Colors.green}[✓] {platform.upper():15} {Colors.white}Found: {result['url']}")
                elif result is True:
                    print(f"{Colors.green}[✓] {platform.upper():15} {Colors.white}Exists")
            elif isinstance(result, str) and 'Error' not in result:
                print(f"{Colors.green}[✓] {platform.upper():15} {Colors.white}{result}")
            else:
                print(f"{Colors.red}[✗] {platform.upper():15} {Colors.white}Not Found")
                
        print(f"\n{Colors.yellow}{'='*60}")
        
        # Show guns.lol specific results
        if 'guns_lol' in results and results['guns_lol']:
            gl_result = results['guns_lol']
            if isinstance(gl_result, dict) and gl_result.get('profile_exists'):
                print(f"\n{Colors.cyan}[!] GUNS.LOL Intelligence:")
                print(f"    URL: {gl_result.get('url')}")
                if gl_result.get('page_title'):
                    print(f"    Title: {gl_result.get('page_title')}")
                if gl_result.get('metadata'):
                    print(f"    Metadata: {len(gl_result['metadata'])} items found")
                    
    def run(self):
        try:
            self.clear()
            self.banner()
            
            username = input(f"\n{Colors.blue}[?] Enter username: {Colors.white}")
            
            if not username:
                print(f"{Colors.red}[!] Username cannot be empty")
                return
                
            print(f"\n{Colors.yellow}[+] Selecting browser...")
            print(f"{Colors.blue}1. Chrome (Headless)")
            print(f"{Colors.blue}2. Firefox (Headless)")
            print(f"{Colors.blue}3. Edge (Headless)")
            
            choice = input(f"\n{Colors.blue}[?] Select browser (1-3): {Colors.white}")
            
            browser_map = {"1": "chrome", "2": "firefox", "3": "edge"}
            browser = browser_map.get(choice, "chrome")
            
            print(f"\n{Colors.yellow}[+] Initializing {browser.capitalize()} driver...")
            if not self.setup_driver(browser):
                return
                
            print(f"{Colors.green}[✓] Driver ready")
            
            platforms = [
                'guns_lol', 'tiktok', 'instagram', 'github', 'twitter',
                'reddit', 'telegram', 'snapchat', 'domains', 'emails'
            ]
            
            print(f"\n{Colors.yellow}[+] Starting concurrent search on {len(platforms)} platforms...")
            
            results = self.concurrent_search(username, platforms)
            
            self.display_results(username, results)
            
            # Generate report
            report_file = self.generate_report(username, results)
            print(f"\n{Colors.green}[✓] Report saved to: {report_file}")
            
            if self.driver:
                self.driver.quit()
                
            input(f"\n{Colors.red}Press Enter to exit...")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.red}[!] Interrupted by user")
        except Exception as e:
            print(f"\n{Colors.red}[!] Error: {e}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass

# Additional search methods (compatible with original)
def guns_lol_search(driver, username):
    tool = AdvancedUsernameOSINT()
    return tool.guns_lol_search(username)

def github_search(driver, username):
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)
        if response.status_code == 200:
            return {"url": f"https://github.com/{username}", "data": response.json()}
        return False
    except:
        return False

def twitter_search(driver, username):
    try:
        url = f"https://twitter.com/{username}"
        driver.get(url)
        time.sleep(3)
        if "This account doesn’t exist" in driver.page_source:
            return False
        return {"url": url, "page_source": driver.page_source[:500]}
    except:
        return False

def reddit_search(driver, username):
    try:
        url = f"https://www.reddit.com/user/{username}/about.json"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            return {"url": f"https://reddit.com/user/{username}", "data": response.json()}
        return False
    except:
        return False

def telegram_search(driver, username):
    try:
        url = f"https://t.me/{username}"
        driver.get(url)
        time.sleep(2)
        if "If you have Telegram, you can contact" in driver.page_source:
            return False
        return url
    except:
        return False

def snapchat_search(driver, username):
    try:
        url = f"https://www.snapchat.com/add/{username}"
        driver.get(url)
        time.sleep(2)
        if "This content could not be found" in driver.page_source:
            return False
        return url
    except:
        return False

if __name__ == "__main__":
    tool = AdvancedUsernameOSINT()
    tool.run()