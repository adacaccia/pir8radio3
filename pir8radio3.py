#!/usr/bin/env python3
import apscheduler, gpiozero, os, signal, subprocess, vlc 
from apscheduler.schedulers.background import BackgroundScheduler
from gpiozero import Button
from os import fork
from signal import pause
from subprocess import run
from vlc import MediaPlayer, MediaListPlayer, MediaList, Instance
#
# Global status
vlc_player = Instance('--aout=alsa').media_new_path('playlist.m3u').player_new_from_media()
#
# proper shutdown button
def shutdown():
    subprocess.run(['sudo','poweroff'],check=True)
#
# no way of getting PID from pidof() when cmd is like "python digital_clock.py"
def pidof_python(script):
    cp = subprocess.run('ps -ux|grep -w python|grep -w '+script+'}|awk "{print $2}"',check=True,capture_output=True,text=True)
    if cp.returncode:
        return 0
    else:
        return int(cp.stdout)
#
# music on/off button
def vlc_toggle():
    global vlc_player
    if vlc_player.is_playing():
        print("pausig vlc")
        vlc_player.pause()
    else:
        vlc_player.play()
def vlc_play():
    global player
    vlc_player.play()
#
# esegue l'orologio in modo thread-safe
def run_clock():
    pid = pidof_python('digital_clock.py')
    if pid:
        # clock is running already --> do nothing
        print(f'clock is running already as pid: {pid} --> do nothing')
        pass
    else:
        # need to start it!
        pid = os.fork()
        if pid:
            # we're in parent!
            print(f'just started clock as pid: {pid}')
            pass
        else:
            # in child: let's do the actual work!
            subprocess.run("cd ~/luma_examples/examples && ./digital_clock.py",shell=True,check=True)
#
# Thread-safe initialization
if __name__ == '__main__':
    #
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
    scheduler.add_job(vlc_play, trigger='cron', minute=30, hour=6, day_of_week='0-4')
    #
    # start clock
    run_clock()
    #
    # event loop
    pause()