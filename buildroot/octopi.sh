#!/bin/bash

# firmware update via ssh
# requires user pi as sudoer
# requires ckermit on octopi

location=$(dirname "$0")

HOST="octopi2"
PORT="/dev/ttyACM0"
RATE="250000"
PATH_LOC="$location"
PATH_BIN="$PATH_LOC/../.pioenvs/LPC1768"
PATH_REM="/home/pi/marlin"

echo "### copy files"
ssh "$HOST" "rm -rf $PATH_REM/*"
ssh "$HOST" "mkdir -p $PATH_REM"
scp "$PATH_LOC/reset.sh" "$HOST:$PATH_REM/"
scp "$PATH_LOC/firmware.sh" "$HOST:$PATH_REM/"
scp "$PATH_BIN/firmware.bin" "$HOST:$PATH_REM/"

echo "### run update"
ssh "$HOST" "$PATH_REM/firmware.sh"

# TODO https://github.com/MarlinFirmware/Marlin/issues/11128
#echo "### issue reset"
#ssh "$HOST" "$PATH_REM/reset.sh $PORT $RATE"

echo ""
echo "### ready"
