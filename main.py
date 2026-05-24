#!/usr/bin/env python3
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib.request
import urllib.error
import sys
import time
import os

# Global list to store session results temporary for saving
session_results = []

def save_to_file_prompt():
    global session_results
    if not session_results:
        return
    
    choice = input("\n[?] Do you want to save these results to a file? (y/n): ").strip().lower()
    if choice == 'y':
        filename = input("[?] Enter filename (e.g., scan_report.txt): ").strip()
        if not filename:
            filename = f"scan_report_{int(time.time())}.txt"
        
        try:
            with open(filename, "w") as f:
                f.write(f"=== RECON FRAMEWORK SCAN REPORT ===\n")
                f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*35 + "\n\n")
                for result in session_results:
                    f.write(result + "\n")
            print(f"[+] Success: Results successfully saved to '{os.path.abspath(filename)}'")
        except Exception as e:
            print(f"[-] Error saving file: {e}")
    
    # Clear cache for next operation
    session_results.clear()

# --- MODULE 1: SMART PORT SCANNER ---
def scan_single_port(target_ip, port):
    global session_results
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
                output = f"[+] Port {port:5} : OPEN  --> Banner: {banner[:50]}"
            else:
                output = f"[+] Port {port:5} : OPEN  --> Banner: No response"
            print(output)
            session_results.append(output)
        sock.close()
    except:
        pass

def advanced_port_scanner():
    print("\n" + "="*25 + " SMART PORT SCANNER " + "="*25)
    target = input("[?] Enter Target Domain or IP (e.g., scanme.nmap.org): ").strip()
    if not target: return

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
    else:
        ports = list(range(1, 101))

    print(f"\n[*] Scanning started at: {time.strftime('%H:%M:%S')}")
    print("[*] Using Multithreading Engine (Super Fast Mode) ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports:
            executor.submit(scan_single_port, target_ip, port)

    print("-"*60 + "\n[+] Scanning finished successfully.")
    save_to_file_prompt()
    input("\nPress Enter to return to Main Menu ...")

# --- MODULE 2: DIRECTORY BRUTEFORCER ---
def check_directory(target_url, folder):
    global session_results
    url = f"{target_url}/{folder}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                output = f"[+] FOUND: {url} (Status: 200 OK)"
                print(output)
                session_results.append(output)
    except urllib.error.HTTPError as e:
        if e.code in [200, 403, 301, 302]:
            output = f"[+] FOUND: {url} (Status: {e.code})"
            print(output)
            session_results.append(output)
    except:
        pass

def directory_bruteforcer():
    print("\n" + "="*25 + " DIRECTORY BRUTEFORCER " + "="*25)
    target_url = input("[?] Enter Target URL (e.g., http://example.com): ").strip()
    if not target_url: return
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "http://" + target_url

    common_folders = ["admin", "login", "wp-admin", "images", "uploads", "css", "js", "api", "config", "backup", "db", "robots.txt", "index.php", "panel"]

    print(f"\n[*] Starting Bruteforce Engine on: {target_url}")
    print("[*] Thread pool active... Scanning hidden folders ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for folder in common_folders:
            executor.submit(check_directory, target_url, folder)

    print("-"*60 + "\n[+] Directory scan finished.")
    save_to_file_prompt()
    input("\nPress Enter to return to Main Menu ...")

# --- MODULE 3: SUBDOMAIN ENUMERATOR ---
def check_subdomain(domain, sub):
    global session_results
    subdomain = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(subdomain)
        output = f"[+] DISCOVERED: {subdomain} --> IP: {ip}"
        print(output)
        session_results.append(output)
    except socket.gaierror:
        pass

def subdomain_enumerator():
    print("\n" + "="*25 + " SUBDOMAIN ENUMERATOR " + "="*25)
    domain = input("[?] Enter Base Domain (e.g., google.com): ").strip()
    if not domain: return
    
    subdomains_list = ["www", "mail", "ftp", "admin", "blog", "cpanel", "webmail", "server", "ns1", "ns2", "api", "dev", "staging", "shop", "secure", "vpn", "test"]

    print(f"\n[*] Starting DNS Recon Engine on: {domain}")
    print("[*] Searching for active subdomains ...\n" + "-"*60)

    with ThreadPoolExecutor(max_workers=15) as executor:
        for sub in subdomains_list:
            executor.submit(check_subdomain, domain, sub)

    print("-"*60 + "\n[+] Subdomain enumeration finished.")
    save_to_file_prompt()
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
        print("       [+] ADVANCED RECON & AUTOMATION SUITE      [+]")
        print("       [+] REPORTING ENGINE: ENABLED (TXT)        [+]")
        print("=" * 60)
        print("[1] Smart Port Scanner & Service Detector")
        print("[2] Directory Bruteforcer & Hidden File Finder")
        print("[3] Subdomain Enumerator (DNS Recon)")
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
        print("\n\n[-] Program interrupted. Exiting...")
        sys.exit()
        
