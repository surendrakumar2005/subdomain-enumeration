#!/usr/bin/env python3
"""
Subdomain Enumeration Script
Description:
    Enumerates subdomains of a given main domain using a wordlist.
    - If no wordlist is provided, a small built-in default list is used.
    - Saves reachable subdomains to 'found_subdomains.txt'.
    - Fully thread-safe and works on Windows, Linux, and macOS.
"""

import requests
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse
import os

passed = []
lock = threading.Lock()


DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "webdisk", "pop", "cpanel", "whm",
    "ns1", "ns2", "autodiscover", "autoconfig", "ns", "test", "m", "blog", "dev", "www2",
    "ns3", "pop3", "forum", "admin", "mail2", "vpn", "mx", "imap", "old", "new",
    "mobile", "mysql", "beta", "support", "cp", "secure", "shop", "demo", "dns1", "dns2",
    "static", "lists", "web", "www1", "img", "news", "portal", "server", "wiki", "api",
    "media", "images", "www.blog", "backup", "dns", "sql", "intranet", "stats", "host", "video",
    "mail1", "mx1", "www3", "staging", "www.m", "sip", "chat", "search", "crm", "mx2",
    "ads", "ipv4", "remote", "email", "my", "wap", "svn", "store", "cms", "download",
    "proxy", "www.dev", "mssql", "apps", "dns3", "exchange", "mail3", "forums", "ns5", "db",
    "office", "live", "files", "info", "owa", "monitor", "helpdesk", "panel", "sms", "newsletter"
]

def sub_enum(sub, host):
    """
    Enumerates a single subdomain:
    - Resolves DNS to get IP
    - Checks if reachable via HTTPS
    - Writes successful subdomains to a file
    """
    url = f'https://{sub}.{host}'
    try:
        ip = socket.gethostbyname(f'{sub}.{host}')
    except socket.gaierror:
        return

    try:
        response = requests.get(url, timeout=5)
        with lock:
            passed.append(url)
            with open("found_subdomains.txt", "a") as f:
                f.write(url + "\n")
        print(f"{url} ({ip}): {response.status_code}\n")
    except requests.RequestException:
        return


parser = argparse.ArgumentParser(
    description="Subdomain Enumeration Script"
)
parser.add_argument(
    "-H", "--host", required=True, help="The main domain to scan (e.g., example.com)"
)
parser.add_argument(
    "-w", "--wordlist", help="Path to subdomain wordlist file (optional)"
)
parser.add_argument(
    "-t", "--threads", type=int, default=50,
    help="Number of concurrent threads (default: 50)"
)

args = parser.parse_args()

host = args.host
wordlist_file = args.wordlist
max_threads = args.threads

try:
    main_ip = socket.gethostbyname(host)
    print(f"[+] Main domain {host} resolved to {main_ip}")
except socket.gaierror:
    print("[!] Hostname could not be resolved. Exiting.")
    exit()

if wordlist_file:
    if os.path.exists(wordlist_file):
        with open(wordlist_file, "r") as f:
            subdomains = [line.strip() for line in f if line.strip()]
        print(f"[+] Loaded {len(subdomains)} subdomains from {wordlist_file}")
    else:
        print(f"[!] Wordlist file '{wordlist_file}' not found. Using default list.")
        subdomains = DEFAULT_WORDLIST
else:
    print("[+] No wordlist provided. Using default built-in list.")
    subdomains = DEFAULT_WORDLIST

with ThreadPoolExecutor(max_workers=max_threads) as executor:
    for sub in subdomains:
        executor.submit(sub_enum, sub, host)

print(f"[+] Enumeration completed. Found {len(passed)} reachable subdomains.")
print("[+] Results saved in 'found_subdomains.txt'")
