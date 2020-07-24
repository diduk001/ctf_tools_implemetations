import sys
import socket
import threading

MOST_COMMON_PORTS = (80, 443, 21, 22, 110, 995, 143, 993, 25,
                     26, 587, 3306, 2082, 2083, 2086, 2087, 2095, 2096, 2077, 2078)
HELP_STRING = f'''

usage: python3 nmap.py [THREADING OPTION] [SCAN TYPE] {{TARGET}}

THREADING OPTION:
    no option - support multi-threading
    -nt - do not support multi-threading

SCAN TYPES:
    no option - scanning ports 1-10000;
    -f - fast scan, {len(MOST_COMMON_PORTS)} most common ports;
    -p- - scan all ports 1-65535;
    -p <port range> - scan port range;

EXAMPLES:
    python3 nmap.py target.com
    python3 nmap.py -p 1-100 target.com
    python3 nmap.py -nt -f target.com

'''

MAX_ARGV_COUNT = 5
ALLOWED_THREADING_OPTIONS = ["-nt"]
ALLOWED_SCAN_TYPES = ["-f", "-p-", "-p"]

ALLOWED_OPTIONS = ALLOWED_THREADING_OPTIONS + ALLOWED_SCAN_TYPES


def scan_port(hostname, port, timeout=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    try:
        s.connect((hostname, port))
        print(f"Port {port} is open")
        s.close()
    except ConnectionError:
        pass


def parse_args():
    argv_count = len(sys.argv)

    # Not allowed count of arguments
    if argv_count == 1:
        print(HELP_STRING)
        raise ValueError("Not enough arguments")
    elif argv_count > MAX_ARGV_COUNT:
        print(HELP_STRING)
        raise ValueError("Too many arguments")

    hostname = sys.argv[-1]

    threading = str()
    scan_type = str()

    threading_flag = False
    scan_type_flag = False
    scan_type_range_flag = False

    # Iterating by command line arguments
    for arg in sys.argv[1:-1]:

        # Append range to scan type
        if scan_type_range_flag:
            _arg = arg.split('-')
            if len(_arg) != 2:
                print(HELP_STRING)
                raise ValueError("Range format is incorrect")

            try:
                map(int, _arg)
            except ValueError:
                print(HELP_STRING)
                raise ValueError("Range format is incorrect")

            scan_type_range_flag = False
            continue

        # Not allowed argument
        if arg not in ALLOWED_OPTIONS:
            print(HELP_STRING)
            raise ValueError(f"Unexpected argument: {arg}")

        elif arg in ALLOWED_THREADING_OPTIONS:
            # 2 or more threading options arguments
            if threading_flag:
                print(HELP_STRING)
                raise ValueError("Two or more threading options")

            threading = arg
            threading_flag = True

        elif arg in ALLOWED_SCAN_TYPES:
            # 2 or more scan types arguments
            if scan_type_flag:
                print(HELP_STRING)
                raise ValueError("Two or more scan types")

            if arg == "-p":
                scan_type_range_flag = True

            scan_type = arg
            scan_type_flag = True

    return threading, scan_type, hostname


def main():
    use_threading = True
    scan_range = list(range(1, 10000 + 1))

    threading_arg, scan_type_arg, hostname = parse_args()

    if threading_arg == "-nt":
        use_threading = False

    if scan_type_arg == "-f":
        scan_range = MOST_COMMON_PORTS
    elif scan_type_arg == "-p-":
        scan_range = list(range(1, 65535 + 1))
    elif scan_type_arg[:2] == "-p":
        scan_range_values = scan_type_arg[2:].split('-')
        scan_range_start, scan_range_end = map(int, scan_range_values)
        scan_range = list(range(scan_range_start, scan_range_end + 1))

    if use_threading:
        print("THREADING FUNCTION IS EXPERIMENTAL")
        print("IF SOMETHING WENT WRONG, USE -nt FLAG TO DISABLE MULTI-THREADING")

        threads = list()

        # Creating Threads
        for port in scan_range:
            t = threading.Thread(target=scan_port, args=(hostname, port))
            threads.append(t)

        # Starting Threads
        for thread in threads:
            thread.start()

        # Waiting until all threads complete
        for thread in threads:
            thread.join()

    else:
        for port in scan_range:
            scan_port(hostname, port)


if __name__ == "__main__":
    main()
