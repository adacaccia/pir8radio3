#!/usr/bin/env python3
import os, subprocess, time, vlc
from signal import pause
from gpiozero import Button
from apscheduler.schedulers.background import BackgroundScheduler
#
# Global status
player = vlc.Instance('--aout=alsa').media_player_new('playlist.m3u')
#
# proper shutdown button
def shutdown():
    subprocess.run(['sudo','poweroff'],check=True)
#
# no way of getting PID from pidof() when cmd is like "python digital_clock.py"
def pidof_python(script):
    cp = subprocess.run(["ps -ux|grep -w python|grep -w",script,"|awk '{print $2}'"],check=True,capture_output=True,text=True,shell=True)
    if cp.returncode:
        return 0
    else:
        return int(cp.stdout)
#
# music on/off button
def vlc_toggle():
    global player
    if player.is_playing():
        player.pause()
    else:
        player.play()
#
# esegue l'orologio in modo thread-safe
def run_clock():
    pid = pidof_python('digital_clock.py')
    if pid:
        # clock is running already --> do nothing
        print(f'clock is running already with pid={pid}')
    else:
        # need to start it!
        pid = os.fork()
        if pid:
            # we're in parent!
            print(f'starting clock with pid={pid}')
        else:
            # in child: let's do the actual work!
            subprocess.run(['cd','~/luma_examples/examples','&&','./digital_clock.py'],shell=True,check=True)
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