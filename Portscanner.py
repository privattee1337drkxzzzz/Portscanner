import socket
import sys
from datetime import datetime

# Termux terminalı üçün rənglər
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def banner():
    print(BLUE + "=" * 55)
    print(r"""
 ____   ___  ____ _____   ____   ____    _    _   _ _   _ _____ ____  
|  _ \ / _ \|  _ \_   _| / ___| / ___|  / \  | \ | | \ | | ____|  _ \ 
| |_) | | | | |_) || |   \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
|  __/| |_| |  _ < | |    ___) | |___ / ___ \| |\  | |\  | |___|  _ < 
|_|    \___/|_| \_\|_|   |____/ \____/_/   \_|_| \_|_| \_|_____|_| \_\
""")
    print("                 Developer by privatte1337            ")
    print("=" * 55 + RESET)

def scan_ports(target_host, start_port, end_port):
    try:
        target_ip = socket.gethostbyname(target_host)
    except socket.gaierror:
        print(RED + "\n[!] Xəta: Host tapılmadı!" + RESET)
        sys.exit()

    print(f"\n{YELLOW}[+] Hədəf IP: {target_ip}{RESET}")
    print(f"{YELLOW}[+] Skan başlama vaxtı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Hər port üçün 0.5 saniyə gözləyir
        
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"{GREEN}[+] Port {port:<5} : AÇIQDIR{RESET}")
            open_ports.append(port)
        s.close()

    print(BLUE + "\n" + "=" * 55 + RESET)
    print(f"{YELLOW}[+] Skan tamamlandı! Tapılan açıq port sayı: {len(open_ports)}{RESET}")
    return open_ports

if __name__ == "__main__":
    banner()
    
    target = input("Hədəf Sayt və ya IP yazın (məs: scanme.nmap.org): ").strip()
    
    try:
        start_p = int(input("Başlanğıc portu (məs: 1): "))
        end_p = int(input("Bitiş portu (məs: 100): "))
    except ValueError:
        print(RED + "[!] Xəta: Port nömrəsi rəqəm olmalıdır!" + RESET)
        sys.exit()

    if start_p > end_p:
        print(RED + "[!] Başlanğıc portu bitişdən böyük ola bilməz!" + RESET)
        sys.exit()

    open_ports = scan_ports(target, start_p, end_p)

    # Nəticəni fayla saxlamaq
    save = input("\nNəticəni fayla yazmaq istəyirsiniz? (e/h): ").lower()
    if save == 'e':
        with open("scan_result.txt", "w") as f:
            f.write(f"Hədəf: {target}\nAçıq portlar: {open_ports}\n")
        print(GREEN + "[+] Nəticə 'scan_result.txt' faylına yazıldı!" + RESET)
