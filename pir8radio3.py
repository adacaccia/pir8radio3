#!/usr/bin/env python3
import apscheduler, gpiozero, os, shlex, signal, subprocess, vlc
from apscheduler.schedulers.background import BackgroundScheduler
from gpiozero import Button
from os import fork
from shlex import split
from signal import pause
from subprocess import run, PIPE, STDOUT, Popen
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
    command='ps -ux|grep -w python|grep -w '+script
    cp = subprocess.run(shlex.split(command),shell=False,stdout=PIPE,stderr=STDOUT,text=True)
    if cp.returncode:
        return 0
    else:
        print(cp.stdout.readline())
        return int(cp.stdout.readline().split()[1])
#
# music on/off button
vlc_playing=False
vlc_process=0
def vlc_toggle():
    if vlc_playing:
        vlc_pause()
    else:
        vlc_play()
def vlc_play():
    #global vlc_player
    global vlc_process,vlc_playing
    print("starting vlc")
    vlc_process.stdin.write('play\n')
    vlc_playing=True
def vlc_pause():
    #global vlc_player
    global vlc_process,vlc_playing
    print("pausing vlc")
    vlc_process.stdin.write('pause\n')
    vlc_playing=False
#
# from: https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-using-python
def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return rc
def run_vlc():
    global vlc_process
    vlc_process=subprocess.Popen(shlex.split('cvlc playlist.m3u'),shell=False,stdout=PIPE,stdin=PIPE)
    output = vlc_process.stdout.readline()
    if output:
        print(output.strip())
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
    # start VLC
    run_vlc()
    #
    # event loop
    pause()