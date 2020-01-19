#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
A Digital Clock with date & time.

"""

import os
import sys
import time
import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)


def main():
    today_last_time = "Unknown"
    ts=[ ":", " "]
    i=0
    font = make_font("Arial_Narrow.ttf", 60)
    while True:
        now = datetime.datetime.now()
        today_time = now.strftime("%-H"+ts[i]+"%M")
        if i == 0:
            i=1 
        else:
            i=0
        if today_time != today_last_time:
            today_last_time = today_time
            device.contrast(0)
            can = canvas(device)
            with can as draw:
                draw.text((0,0), today_time, font=font, fill="gray")
        time.sleep(0.99)

if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
