import sys
import time
import socket
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
    """Aik akele port ko check karne aur uski service pakadne ka smart function"""
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
    
    if not target:
        print("[-] Target cannot be empty!")
        return

    try:
        print(f"\n[*] Resolving target DNS...")
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
    print("[*] Using Multithreading Engine (Super Fast Mode)...")
    print("-" * 50)

    with ThreadPoolExecutor(max_workers=50) as executor:
        for port in ports_to_scan:
            executor.submit(scan_single_port, target_ip, port)

    print("-" * 50)
    print(f"[+] Scanning finished successfully.")
    input("\nPress Enter to return to Main Menu...")

# ==================== MAIN INTERFACE CONTROLLER ====================
def main_menu():
    banner()
    print("\nSelect an advanced scanning module:")
    print("[1] Smart Port Scanner & Service Detector (Ultra Fast)")
    print("[2] Directory Bruteforcer & Hidden File Finder")
    print("[3] Subdomain Enumerator (DNS Recon)")
    print("[4] Exit Framework")
    print("-" * 60)
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        advanced_port_scanner()
        main_menu()
    elif choice == '2':
        print("\n[!] Launching Directory Finder Module...")
    elif choice == '3':
        print("\n[!] Launching Subdomain Enumerator...")
    elif choice == '4':
        print("\n[+] Exiting Framework. Goodbye!")
        sys.exit()
    else:
        print("\n[-] Invalid option! Please select a valid module.")
        time.sleep(2)
        main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n[-] Framework interrupted by user. Exiting...")
        sys.exit()
    
