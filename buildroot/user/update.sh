#!/bin/bash

# mks firmware updater via remote ssh
# requires octopi user pi as sudoer
# requires ckermit on octopi

set -e

location=$(dirname "$0")

# ssh host name
HOST="octopi2"

# marlin board aaccess
PORT="/dev/ttyACM0"
RATE="115200" # does not affect usb speed

# location of this script
PATH_LOC="$location"

# location of generated firmware.bin 
PATH_BIN="$PATH_LOC/../../.pioenvs/USER_Wanhao_D6_MKS_SBASE/LPC1768"

# working folder on remote host
PATH_REM="/home/pi/marlin"

echo "### copy files"
ssh "$HOST" "rm -rf $PATH_REM/*"
ssh "$HOST" "mkdir -p $PATH_REM"
scp "$PATH_LOC/kermit.sh" "$HOST:$PATH_REM/"
scp "$PATH_LOC/install.sh" "$HOST:$PATH_REM/"
scp "$PATH_BIN/firmware.bin" "$HOST:$PATH_REM/"

restart () {
	echo "### issue restart"
	ssh "$HOST" "$PATH_REM/kermit.sh $PORT $RATE M997"
	sleep 10 # time for marlin reboot
	
	echo "### expose sd-card"
	ssh "$HOST" "$PATH_REM/kermit.sh $PORT $RATE M22"
	sleep 10 # time to mount sd card
	
	ssh "$HOST" "lsblk -o name,label"
}

install () {
	echo "### invoke install"
	ssh "$HOST" "$PATH_REM/install.sh"
}


install

echo "### ready"
