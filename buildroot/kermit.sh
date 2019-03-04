#!/usr/bin/kermit + -q

# issue single command via serial port

# $port
set port \%1
if fail exit 1 "invalid port"

# $rate
set baud \%2
if fail exit 1 "invalid rate"

# serial setup
set serial 8n1
set flow-control none
set carrier-watch off
set modem type none

# monitor progress
set term echo local
set term cr crlf

# $command
lineout \%3

exit 0
