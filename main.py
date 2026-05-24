import sys
import time
import socket
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def banner():
    print("-" * 60)
    print("   █████  ██████  ██    ██  █████  ███    ██  ██████ ███████ ")
    print("  ██   ██ ██   ██ ██    ██ ██   ██ ████   ██ ██      ██      ")
    print("  ███████ ██   ██ ██    ██ ███████ ██ ██  ██ ██      █████   ")
    print("  ██   ██ ██   ██  ██  ██  ██   ██ ██  ██ ██ ██      ██      ")
    print("  ██   ██ ██████    ████   ██   ██ ██   ████  ██████ ███████ ")
    print("\n        [+] ADVANCED RECON & AUTOMATION FRAMEWORK [+]")
    print("        [+] STATUS: ACTIVE | VERSION: 1.0.0       [+]")
    print("-" * 60)

# ==================== ADVANCED PORT SCANNER MODULE ====================
def scan_single_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            try:
                s.sendall(b"Hello\r\n")
                banner_reply = s.recv(1024).decode().strip()
                service_info = f"OPEN --> Banner: {banner_reply[:40]}"
            except:
                service_info = "OPEN (Service active)"
            print(f"[+] Port {port:<5}: {service_info}")
        s.close()
    except:
        pass

def advanced_port_scanner():
    print("\n" + "="*20 + " SMART PORT SCANNER " + "="*20)
    target = input("[?] Enter Target Domain or IP (e.g., scanme.nmap.org): ")
    if not target: return
    try:
        target_ip = socket.gethostbyname(target)
        print(f"[+] Target IP Address: {target_ip}")
    except socket.gaierror:
        print("[-] Error: Could not resolve domain name.")
        return

    print("\n[ Choice ] Scan Type:")
    print(" 1. Common Ports Scan (Top 20 Ports)")
    print(" 2. Extended Scan (Top 100 Ports)")
    scan_choice = input("[?] Select Option (1-2): ")

    if scan_choice == '1':
        ports_to_scan = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5900, 8080, 8443]
    else:
        ports_to_scan = list(range(1, 101))

    print(f"\n[*] Scanning started at: {time.strftime('%H:%M:%S')}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports_to_scan:
            executor.submit(scan_single_port, target_ip, port)
    input("\nPress Enter to return to Main Menu...")

# ==================== DIRECTORY BRUTEFORCER MODULE ====================
def check_directory(target_url, folder):
    # Har ek directory ko web request bhej kar check karne ka function
    if not target_url.endswith('/'):
        target_url += '/'
    
    url = f"{target_url}{folder}"
    try:
        # Request bhejna bina browser ke
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2.0) as response:
            if response.status == 200:
                print(f"[+] FOUND: {url} (Status: 200 OK)")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"[!] FORBIDDEN: {url} (Status: 403 Restricted)")
    except:
        pass

def directory_bruteforcer():
    print("\n" + "="*18 + " DIRECTORY BRUTEFORCER " + "="*18)
    target_url = input("[?] Enter Target URL (e.g., http://example.com): ")
    if not target_url.startswith('http'):
        print("[-] Invalid URL! Please include http:// or https://")
        input("\nPress Enter to retry...")
        return

    # Built-in short wordlist scanning ke liye
    common_folders = ["admin", "login", "uploads", "images", "config", "backup", "db", "api", "secret", "robots.txt", "index.php", "wp-admin"]
    
    print(f"\n[*] Starting Bruteforce Engine on: {target_url}")
    print("[*] Thread pool active... Scanning hidden folders...")
    print("-" * 50)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for folder in common_folders:
            executor.submit(check_directory, target_url, folder)

    print("-" * 50)
    print("[+] Directory scan finished.")
    input("\nPress Enter to return to Main Menu...")

# ==================== MAIN INTERFACE CONTROLLER ====================
def main_menu():
    banner()
    print("\nSelect an advanced scanning module:")
    print("[1] Smart Port Scanner & Service Detector (Ultra Fast)")
    print("[2] Directory Bruteforcer & Hidden File Finder (New!)")
    print("[3] Subdomain Enumerator (DNS Recon)")
    print("[4] Exit Framework")
    print("-" * 60)
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        advanced_port_scanner()
        main_menu()
    elif choice == '2':
        directory_bruteforcer()
        main_menu()
    elif choice == '3':
        print("\n[!] Launching Subdomain Enumerator...")
    elif choice == '4':
        print("\n[+] Exiting Framework. Goodbye!")
        sys.exit()
    else:
        print("\n[-] Invalid option!")
        time.sleep(1)
        main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        sys.exit()
                               
