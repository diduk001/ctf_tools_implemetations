'''
Python 3 minimal version of port scanner

USAGE: python3 {SCAN TYPE} nmap.py

SCAN TYPES:
    no option - scan ports 1-10000
    -f - fast scan, {len(MOST_COMMON_PORTS)} most common ports;
    -p- - scan all ports 1-65535;
    -p <port range> - scan port range;

'''

import sys
import socket

ALLOWED_OPTIONS = ALLOWED_SCAN_TYPES = ["-f", "-p-", "-p"]

# You can shrink this list if you want
MOST_COMMON_PORTS = (80, 443, 21, 22, 110, 995, 143, 993, 25,
                     26, 587, 3306, 2082, 2083, 2086, 2087, 2095, 2096, 2077, 2078)


def scan_port(hostname, port, timeout=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((hostname, port))
        print(f"Port {port} is open")
        s.close()
    except ConnectionError:
        pass


def main():
    # Arguments parsing
    argv_cnt = len(sys.argv)
    hostname = sys.argv[-1]

    scan_range = list(range(1, 10000))

    if len(argv_cnt) >= 3:
        if sys.argv[1] == "-f":
            scan_range = MOST_COMMON_PORTS
        elif sys.argv[1] == "-p-":
            scan_range = list(range(1, 65535 + 1))
        else:
            scan_range_start, scan_range_end = map(int, sys.argv[2].split('-'))
            scan_range = list(range(scan_range_start, scan_range_end + 1))
    
    # Port scanning
    for port in scan_range:
        scan_port(hostname, port)