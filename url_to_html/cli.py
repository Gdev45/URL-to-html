#!/usr/bin/env python3
import requests
import urllib.parse
import urllib.robotparser
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

USER_AGENT = "MyCLI/1.0 (learning project)"


def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
  __  _____  __     __________    __ __________  _____ 
 / / / / _ \/ /    /_  __/ __ \  / // /_  __/  |/  / / 
/ /_/ / , _/ /__    / / / /_/ / / _  / / / / /|_/ / /__
\____/_/|_/____/   /_/  \____/ /_//_/ /_/ /_/  /_/____/
                                                       
""")
    print(Fore.CYAN + "Fetch and save webpage HTML safely\n")


def is_allowed(url):
    parsed = urllib.parse.urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)

    try:
        rp.read()
    except Exception:
        # If robots.txt can't be read, allow fetching
        return True

    return rp.can_fetch(USER_AGENT, url)


def fetch_html(url: str) -> str | None:
    """Fetch HTML content from a URL, respecting robots.txt"""
    headers = {"User-Agent": USER_AGENT}

    if not is_allowed(url):
        print(Fore.RED + "Blocked by robots.txt")
        return None

    try:
        print(Fore.YELLOW + "Fetching HTML...")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        time.sleep(1)
        print(Fore.GREEN + "HTML successfully retrieved!\n")
        return response.text

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error: {e}")
        return None


def main():
    """Entry point for CLI"""
    banner()

    url = input(Fore.WHITE + "Enter a URL: ").strip()
    if not url.startswith("http"):
        url = "https://" + url

    html = fetch_html(url)

    if html:
        save = input(Fore.CYAN + "Save HTML to file? (y/n): ").lower()
        if save == "y":
            filename = input(Fore.WHITE + "Filename (default: output.html): ").strip()
            if not filename:
                filename = "output.html"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(html)
            print(Fore.GREEN + f"Saved to {filename}")
        else:
            print(Fore.YELLOW + "Skipped saving.")
    else:
        print(Fore.RED + "Could not retrieve page.")
