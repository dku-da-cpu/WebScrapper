import urllib.request
import os
import re
from urllib.parse import urljoin, urlparse
import time


"""ASCII"""

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
def show_ascii_art():
    art = """

        █     █▓█████ ▄▄▄▄        ██████ ▄████▄  ██▀███  ▄▄▄      ██▓███  ██▓███ ▓█████ ██▀███  
        ▓█░ █ ░█▓█   ▀▓█████▄    ▒██    ▒▒██▀ ▀█ ▓██ ▒ ██▒████▄   ▓██░  ██▓██░  ██▓█   ▀▓██ ▒ ██▒
        ▒█░ █ ░█▒███  ▒██▒ ▄██   ░ ▓██▄  ▒▓█    ▄▓██ ░▄█ ▒██  ▀█▄ ▓██░ ██▓▓██░ ██▓▒███  ▓██ ░▄█ ▒
        ░█░ █ ░█▒▓█  ▄▒██░█▀       ▒   ██▒▓▓▄ ▄██▒██▀▀█▄ ░██▄▄▄▄██▒██▄█▓▒ ▒██▄█▓▒ ▒▓█  ▄▒██▀▀█▄  
        ░░██▒██▓░▒████░▓█  ▀█▓   ▒██████▒▒ ▓███▀ ░██▓ ▒██▒▓█   ▓██▒██▒ ░  ▒██▒ ░  ░▒████░██▓ ▒██▒
        ░ ▓░▒ ▒ ░░ ▒░ ░▒▓███▀▒   ▒ ▒▓▒ ▒ ░ ░▒ ▒  ░ ▒▓ ░▒▓░▒▒   ▓▒█▒▓▒░ ░  ▒▓▒░ ░  ░░ ▒░ ░ ▒▓ ░▒▓░
        ▒ ░ ░  ░ ░  ▒░▒   ░    ░ ░▒  ░ ░ ░  ▒    ░▒ ░ ▒░ ▒   ▒▒ ░▒ ░    ░▒ ░     ░ ░  ░ ░▒ ░ ▒░
        ░   ░    ░   ░    ░    ░  ░  ░ ░         ░░   ░  ░   ▒  ░░      ░░         ░    ░░   ░ 
            ░      ░  ░░               ░ ░ ░        ░          ░  ░                  ░  ░  ░     
                            ░            ░                                                       

"""
    print(f"{GREEN}{art}{RESET}")
    print(f"{RED}                                                                             Web Scrapper-v1{RESET}")
    print(f"{GREEN}                                                                                 By: GreenBug{RESET}\n")


def fetch_html(url):
    """"Fetch the main HTML content of the given URL"""
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_assets(html, base_url):
    """Extract CSS and JS file URL's from the HTML"""
    css_files = re.findall(r'<link[^>]+href=["\'](.*?\.css)["\']', html, re.IGNORECASE)
    js_files = re.findall(r'<script[^>]+src=["\'](.*?\.js)["\']', html, re.IGNORECASE)

    css_files = [urljoin(base_url, css) for css in css_files]
    js_files = [urljoin(base_url, js) for js in js_files]

    return css_files, js_files

def save_files(url, folder, filename=None):
    """Download and save a file to the specified folder"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    try:
        if not filename:
            filename = os.path.basename(urlparse(url).path) or "index.html"

        filepath = os.path.join(folder, filename)
        urllib.request.urlretrieve(url, filepath)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error Downloading {url}: {e}")

def scrape_website():
    """Main Function to Scrape the website based on user Input"""
    url = input("Enter the URL to scrape: ").strip()
    folder_name = input("Enter the folder name to store scraped files: ").strip()

    base_folder = os.path.join("scraped_sites", folder_name)
    os.makedirs(base_folder, exist_ok=True)

    print("\nFetching HTML content...")
    html_content = fetch_html(url)
    if not html_content:
        print("Failed to retrieve HTML content. Exiting...")
        return
    
    save_files(url, base_folder, "index.html")

    css_files, js_files = extract_assets(html_content, url)

    print("\nDownloading CSS files...")
    for css in css_files:
        save_files(css, os.path.join(base_folder, "css"))

    print("\nDownloading JS files...")
    for js in js_files:
        save_files(js, os.path.join(base_folder, "js"))

    print(f"\n{RED}Scraping Complete!{RESET}\n")

def scrapper_menu():
    while True:
        print(f"{GREEN}Main Menu:{RESET}")
        print("1: Scrap it!")
        print("2: Quit")
        choice = input("Select an option: ")

        if choice == "1":
            while True:
                scrape_website()
                print("1: Scrap Again?")
                print("2: Go Back")
                sub_choice = input("Select an option: ")

                if sub_choice == "1":
                    continue
                elif sub_choice == "2":
                    break
                else:
                    print("Invalid Option!")
        elif choice == "2":
            print("Exiting...")
            time.sleep(1)
            break
        else:
            print("Invalid Option!")

if __name__ == "__main__":
    show_ascii_art()
    scrapper_menu()