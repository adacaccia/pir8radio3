#!/bin/bash
#
# digital_clock launcher script by AMC
NAME=$(basename $0)
#
# is it already running?
if [ ! -f /tmp/${NAME}.pid ]
then
	# No: init PID file
	echo "$$" > /tmp/${NAME}.pid
	# start python file in current shell's context
	cd ~/luma_examples/examples && ./digital_clock.py > /dev/null
	# nuova riga di comando:
	# ./digital_clock.py --display ssd1327 --width 128 --height 128 --i2c-address 0x1a
	# at exit, removes the PID file
	rm -f /tmp/${NAME}.pid
else
	# get PID value
	PID=$(cat /tmp/${NAME}.pid)
	# Warning message
	echo "$NAME is already running as PID=$PID, not starting again!"
fi
