#!/usr/bin/env python3
import os, subprocess, time
from signal import pause
from gpiozero import Button
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread, ThreadError
from vlc import MediaPlayer, MediaListPlayer, MediaList, Instance
#
# Global status
vlc_instance = Instance('--aout=alsa')
vlc_player = MediaListPlayer(vlc_instance)
vlc_player.set_media_player(MediaPlayer(vlc_instance,'playlist.m3u'))
#
# proper shutdown button
def shutdown():
    subprocess.run(['sudo','poweroff'],check=True)
#
# music on/off button
def vlc_toggle():
    global vlc_player
    if vlc_player.is_playing():
        print("pausig vlc")
        vlc_player.pause()
    else:
        print("starting vlc")
        vlc_player.play()
#    
# esegue il vero comando di run
def clock():
    subprocess.run(['cd','~/luma_examples/examples','&&','./digital_clock.py'],shell=True,check=True)
#
# esegue l'orologio in modo thread-safe
def run_clock():
    ct=Thread(target=clock,name='ClockT')
    ct.start()
#
# Thread-safe initialization
if __name__ == '__main__':
    # WaveShare's WM8960-Audio-HAT has got a button on GPIO#17
    wm8960_btn = Button(17, hold_time=3)
    wm8960_btn.when_held = shutdown
    wm8960_btn.when_released = vlc_toggle
    #
    # Impostazione sveglie come da crontab della pir8radio2:
    # m h  dom mon dow   command
    #30 06	*   *	1-5	$HOME/vlc_send.sh play
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(vlc_toggle, trigger='cron', minute=30, hour=6, day_of_week='0-4')
    #
    # start clock
    run_clock()
    #
    # event loop
    pause()