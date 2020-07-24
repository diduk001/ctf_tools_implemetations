#!/bin/bash

# Usage:
# ./nmap.sh {port_range_start} {port_range_end} {hostname}

# If you can input something, that means the port is open
# Use ^], ctrl+D to exit input

for ((port=$1; port <= $2; port++))
do
    echo "Testing port $port"
    telnet $3 $port 1>/dev/null 2>/dev/null
done

exit 0