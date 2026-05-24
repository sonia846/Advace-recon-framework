#!/usr/bin/env python3
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.error
import sys
import time

# --- MODULE 1: SMART PORT SCANNER ---
def scan_single_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            banner = ""
            try:
                sock.sendall(b"Hello\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip().replace('\n', ' ')
            except:
                pass
            if banner:
                print(f"[+] Port {port:5} : OPEN  --> Banner: {banner[:50]}")
            else:
                print(f"[+] Port {port:5} : OPEN  --> Banner: No response")
        sock.close()
    except:
        pass

def advanced_port_scanner():
    print("\n" + "="*25 + " SMART PORT SCANNER " + "="*25)
    target = input("[?] Enter Target Domain or IP (e.g., scanme.nmap.org): ").strip()
    if not target:
        print("[-] Target cannot be empty!")
        return

    print("[*] Resolving target DNS...")
    try:
        target_ip = socket.gethostbyname(target)
        print(f"[+] Target IP Address: {target_ip}")
    except socket.gaierror:
        print("[-] Error: Could not resolve domain name.")
        return

    print("\n[ Choice ] Scan Type:\n1. Common Ports Scan (Top 20 Ports)\n2. Extended Scan (Top 100 Ports)")
    choice = input("[?] Select Option (1-2): ").strip()

    if choice == '1':
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]
    elif choice == '2':
        ports = list(range(1, 101))
    else:
        print("[-] Invalid selection. Defaulting to Top 20 Ports.")
        ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080]

    print(f"\n[*] Scanning started at: {time.strftime('%H:%M:%S')}")
    print("[*] Using Multithreading Engine (Super Fast Mode) ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports:
            executor.submit(scan_single_port, target_ip, port)

    print("-"*60 + "\n[+] Scanning finished successfully.")
    input("\nPress Enter to return to Main Menu ...")

# --- MODULE 2: DIRECTORY BRUTEFORCER ---
def check_directory(target_url, folder):
    url = f"{target_url}/{folder}"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                print(f"[+] FOUND: {url} (Status: 200 OK)")
    except urllib.error.HTTPError as e:
        if e.code in [200, 403, 301, 302]:
            print(f"[+] FOUND: {url} (Status: {e.code})")
    except:
        pass

def directory_bruteforcer():
    print("\n" + "="*25 + " DIRECTORY BRUTEFORCER " + "="*25)
    target_url = input("[?] Enter Target URL (e.g., http://example.com): ").strip()
    if not target_url:
        print("[-] URL cannot be empty!")
        return
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url

    common_folders = [
        "admin", "login", "wp-admin", "images", "uploads", "css", "js", "api", 
        "config", "backup", "db", "administrator", "robots.txt", "index.php", "panel"
    ]

    print(f"\n[*] Starting Bruteforce Engine on: {target_url}")
    print("[*] Thread pool active... Scanning hidden folders ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for folder in common_folders:
            executor.submit(check_directory, target_url, folder)

    print("-"*60 + "\n[+] Directory scan finished.")
    input("\nPress Enter to return to Main Menu ...")

# --- MODULE 3: SUBDOMAIN ENUMERATOR ---
def check_subdomain(domain, sub):
    subdomain = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(subdomain)
        print(f"[+] DISCOVERED: {subdomain} --> IP: {ip}")
    except socket.gaierror:
        pass

def subdomain_enumerator():
    print("\n" + "="*25 + " SUBDOMAIN ENUMERATOR " + "="*25)
    domain = input("[?] Enter Base Domain (e.g., google.com, nmap.org): ").strip()
    if not domain:
        print("[-] Domain cannot be empty!")
        return
    
    # Common subdomain wordlist
    subdomains_list = [
        "www", "mail", "ftp", "admin", "blog", "cpanel", "webmail", "server",
        "ns1", "ns2", "api", "dev", "staging", "shop", "secure", "vpn", "test"
    ]

    print(f"\n[*] Starting DNS Recon Engine on: {domain}")
    print("[*] Searching for active subdomains ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=15) as executor:
        for sub in subdomains_list:
            executor.submit(check_subdomain, domain, sub)

    print("-"*60 + "\n[+] Subdomain enumeration finished.")
    input("\nPress Enter to return to Main Menu ...")

# --- MAIN MENU FRAMEWORK ---
def main_menu():
    while True:
        print("\n" + "=" * 60)
        print("   ___  ___  _  _  ___  _  _  ___  ___ ")
        print("  | _ \|  _|| |/ /|   \| |/ /|_ _||_ _|")
        print("  |   /|  _||   < | | |  _ <  | |  | | ")
        print("  |_|_\|___||_|\_\|___/|_|\_\|___| |_| ")
        print("=" * 60)
        print("       [+] ADVANCED RECON & AUTOMATION FRAMEWORK [+]")
        print("       [+] STATUS: ACTIVE | VERSION: 1.1.0        [+]")
        print("=" * 60)
        print("Select an advanced scanning module:")
        print("[1] Smart Port Scanner & Service Detector (Ultra Fast)")
        print("[2] Directory Bruteforcer & Hidden File Finder")
        print("[3] Subdomain Enumerator (DNS Recon) (New!)")
        print("[4] Exit Framework")
        print("-" * 60)

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            advanced_port_scanner()
        elif choice == '2':
            directory_bruteforcer()
        elif choice == '3':
            subdomain_enumerator()
        elif choice == '4':
            print("\n[+] Exiting Framework. Goodbye!\n")
            sys.exit()
        else:
            print("\n[-] Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[-] Program interrupted by user. Exiting...")
        sys.exit()
    
