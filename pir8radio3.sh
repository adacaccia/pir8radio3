#!/usr/bin/env bash
#
# Script di avvio pir8radio3 su bare-metal
set -ex
#
NAME=$(basename $0)
DIR=$(dirname $0)
#
cd $DIR
pip3 install -r requirements.txt
python3 pir8radio3.py