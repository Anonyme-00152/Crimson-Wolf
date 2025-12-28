import requests
import time
from datetime import datetime

# Define color codes and variables for the tool
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
reset = "\033[0m"
PREFIX = f"{red}[{green}*{red}]{reset}"
ERROR = f"{red}[{yellow}!{red}]{reset}"
SUCCESS = f"{red}[{green}+{red}]{reset}"
LOADING = f"{red}[{blue}~{red}]{reset}"
PREFIX1 = f"{green}[{reset}"
SUFFIX1 = f"{green}]{reset}"
name_tool = "GitHubFinder"  # Define the tool name

def github_email_finder():
    """GitHub Email Finder - Extract email from GitHub repository commits"""
    
    print(f"\n{red}╔═══════════════════════════════════════════════════════════╗")
    print(f"{red}║                 GITHUB EMAIL FINDER                       ║")
    print(f"{red}╚═══════════════════════════════════════════════════════════╝\n")
    
    try:
        # Get inputs
        username = input(f"{PREFIX}Enter GitHub username {red}->{reset} ").strip()
        if not username:
            print(f"{ERROR} No username provided!")
            time.sleep(1.5)
            return
        
        repository = input(f"{PREFIX}Enter repository name {red}->{reset} ").strip()
        if not repository:
            print(f"{ERROR} No repository name provided!")
            time.sleep(1.5)
            return
        
        print(f"\n{LOADING} Searching commits for {username}/{repository}...")
        
        # API request
        url = f"https://api.github.com/repos/{username}/{repository}/commits"
        headers = {
            'User-Agent': f'{name_tool}-Tool/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            print(f"{ERROR} Repository not found: {username}/{repository}")
            time.sleep(2)
            return
        elif response.status_code == 403:
            print(f"{ERROR} API rate limit exceeded. Try again later.")
            time.sleep(2)
            return
        elif response.status_code != 200:
            print(f"{ERROR} GitHub API error: Status {response.status_code}")
            time.sleep(2)
            return
        
        data = response.json()
        
        if not data:
            print(f"{ERROR} No commits found in this repository.")
            time.sleep(2)
            return
        
        # Display results
        print(f"\n{green}╔═══════════════════════════════════════════════════════════╗")
        print(f"{green}║                  EMAIL FOUND                             ║")
        print(f"{green}╚═══════════════════════════════════════════════════════════╝{reset}\n")
        
        # Get first commit (most recent)
        first_commit = data[0]
        commit_info = first_commit.get('commit', {})
        author_info = commit_info.get('author', {})
        
        email = author_info.get('email', 'N/A')
        name = author_info.get('name', 'N/A')
        commit_hash = first_commit.get('sha', 'N/A')[:8]
        commit_date = author_info.get('date', 'N/A')
        
        # Format date if available
        if commit_date != 'N/A':
            try:
                dt = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                formatted_date = commit_date
        else:
            formatted_date = 'N/A'
        
        # Display in table style
        print(f"{red}┌─────────────────────────────────────────────────────────┐")
        print(f"{red}│                COMMIT INFORMATION                     │")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│ {PREFIX1}Repository{SUFFIX1}: {yellow}{username}/{repository}{reset}")
        print(f"{red}│ {PREFIX1}Total Commits{SUFFIX1}: {len(data)}{reset}")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│ {PREFIX1}Latest Commit{SUFFIX1}: {commit_hash}{reset}")
        print(f"{red}│ {PREFIX1}Commit Date{SUFFIX1}: {formatted_date}{reset}")
        print(f"{red}├─────────────────────────────────────────────────────────┤{reset}")
        print(f"{red}│ {PREFIX1}Author Name{SUFFIX1}: {name}{reset}")
        print(f"{red}│ {PREFIX1}Author Email{SUFFIX1}: {blue}{email}{reset}")
        print(f"{red}└─────────────────────────────────────────────────────────┘{reset}")
        
        # Additional commits info
        if len(data) > 1:
            print(f"\n{green}═══════════════════════════════════════════════════════════")
            print(f"{green}           ADDITIONAL COMMITS ({len(data)-1})              ")
            print(f"{green}═══════════════════════════════════════════════════════════{reset}")
            
            # Show unique emails from recent commits
            unique_emails = set()
            for i, commit in enumerate(data[1:6], 2):  # Next 5 commits
                commit_data = commit.get('commit', {})
                commit_author = commit_data.get('author', {})
                commit_email = commit_author.get('email', 'N/A')
                commit_name = commit_author.get('name', 'N/A')
                
                if commit_email != 'N/A':
                    unique_emails.add(commit_email)
                
                if i <= 4:  # Show first 3 additional commits
                    commit_sha = commit.get('sha', 'N/A')[:8]
                    print(f"   {PREFIX1}{i:02d}{SUFFIX1} {commit_name} ({commit_sha}): {commit_email}")
            
            if len(data) > 6:
                print(f"   {PREFIX1}...{SUFFIX1} +{len(data)-6} more commits")
            
            if unique_emails:
                print(f"\n{PREFIX1}Unique Emails{SUFFIX1}: {len(unique_emails)} found in recent commits")
        
        # Save option
        print(f"\n{red}═══════════════════════════════════════════════════════════")
        save = input(f"{PREFIX}Save results to file? (Y/N) {red}->{reset} ").strip().lower()
        
        if save in ['y', 'yes']:
            filename = f"GitHub_Email_{username}_{repository}.txt"
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(f"GitHub Email Finder Results\n")
                    file.write(f"{'='*50}\n")
                    file.write(f"Repository: {username}/{repository}\n")
                    file.write(f"Total Commits: {len(data)}\n")
                    file.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    file.write(f"\nLatest Commit Author:\n")
                    file.write(f"- Name: {name}\n")
                    file.write(f"- Email: {email}\n")
                    file.write(f"- Commit: {commit_hash}\n")
                    file.write(f"- Date: {formatted_date}\n")
                    
                    if len(data) > 1:
                        file.write(f"\nRecent Commits ({min(5, len(data)-1)} shown):\n")
                        for i, commit in enumerate(data[1:6], 1):
                            commit_data = commit.get('commit', {})
                            commit_author = commit_data.get('author', {})
                            file.write(f"{i}. {commit_author.get('name', 'N/A')}: {commit_author.get('email', 'N/A')}\n")
                
                print(f"{SUCCESS} Saved to: {filename}")
                time.sleep(1)
            except Exception as e:
                print(f"{ERROR} Save failed: {str(e)}")
        
        # Privacy note
        print(f"\n{yellow}═══════════════════════════════════════════════════════════")
        print(f"{yellow}⚠  PRIVACY NOTE                                         ")
        print(f"{yellow}═══════════════════════════════════════════════════════════{reset}")
        print(f"   {PREFIX1}•{SUFFIX1} Emails from commits are {yellow}public data{reset}")
        print(f"   {PREFIX1}•{SUFFIX1} Users can set email to {green}private{reset} in Git config")
        print(f"   {PREFIX1}•{SUFFIX1} Respect GitHub's {red}Terms of Service{reset}")
        
    except requests.exceptions.Timeout:
        print(f"{ERROR} Request timed out.")
    except requests.exceptions.ConnectionError:
        print(f"{ERROR} Invalid API response.")
    except IndexError:
        print(f"{ERROR} No commits found or invalid repository.")
    except KeyboardInterrupt:
        print(f"\n{ERROR} Operation cancelled.")
    except Exception as e:
        print(f"{ERROR} Error: {str(e)}")
    
    # Auto-return
    print(f"\n{red}═══════════════════════════════════════════════════════════")
    print(f"{LOADING} Returning to menu in 3 seconds...")
    time.sleep(3)

# To run the function directly
if __name__ == "__main__":
    github_email_finder()