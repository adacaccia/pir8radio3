#!/usr/bin/env bash
#
# Script di avvio pir8radio3 su docker (test)
set -ex
#
NAME=$(basename $0)
DIR=$(dirname $0)
#
cd $DIR
python3 pir8radio3.py