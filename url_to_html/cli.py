#!/usr/bin/env python3
import requests
import urllib.parse as up
import urllib.robotparser as urp
import time
from colorama import Fore, Style, init

# turn on colorama
init(autoreset=True)

UA = "MyCLI/1.0 (learning project)"


def show_banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
  __  _____  __     __________    __ __________  _____ 
 / / / / _ \/ /    /_  __/ __ \  / // /_  __/  |/  / / 
/ /_/ / , _/ /__    / / / /_/ / / _  / / / / /|_/ / /__
\____/_/|_/____/   /_/  \____/ /_//_/ /_/ /_/  /_/_____/
""")
    print(Fore.CYAN + "Fetch and save webpage HTML safely\n")


def allowed(url):
    parsed = up.urlparse(url)
    robots = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    parser = urp.RobotFileParser()
    parser.set_url(robots)

    try:
        parser.read()
    except Exception:
        # if robots.txt fails, just allow it
        return True

    return parser.can_fetch(UA, url)


def get_html(url):
    headers = {"User-Agent": UA}

    if not allowed(url):
        print(Fore.RED + "Blocked by robots.txt")
        return None

    try:
        print(Fore.YELLOW + "Fetching HTML...")
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()

        # small delay so we’re not hammering anything
        time.sleep(1)

        print(Fore.GREEN + "Got it!\n")
        return res.text

    except requests.exceptions.RequestException as err:
        print(Fore.RED + f"Request failed: {err}")
        return None


def main():
    show_banner()

    url = input(Fore.WHITE + "Enter a URL: ").strip()

    if not url.startswith("http"):
        url = "https://" + url

    html = get_html(url)

    if not html:
        print(Fore.RED + "Could not retrieve page.")
        return

    choice = input(Fore.CYAN + "Save HTML to file? (y/n): ").strip().lower()

    if choice == "y":
        name = input(Fore.WHITE + "Filename (default: output.html): ").strip()
        if not name:
            name = "output.html"

        with open(name, "w", encoding="utf-8") as f:
            f.write(html)

        print(Fore.GREEN + f"Saved to {name}")
    else:
        print(Fore.YELLOW + "Skipped saving.")


if __name__ == "__main__":
    main()
