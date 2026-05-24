import sys
import time

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

def main_menu():
    banner()
    print("\nSelect an advanced scanning module:")
    print("[1] Smart Port Scanner & Service Detector (Fast)")
    print("[2] Directory Bruteforcer & Hidden File Finder")
    print("[3] Subdomain Enumerator (DNS Recon)")
    print("[4] Exit Framework")
    print("-" * 60)
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        print("\n[!] Launching Port Scanner Module...")
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
      
