#!/usr/bin/env python3
from subprocess import check_call, Popen
from gpiozero import Button
from signal import pause
from time import sleep
import os, signal, subprocess
from apscheduler.schedulers.background import BackgroundScheduler
#
# Global VLC status
VLC_RUNNING=False
#
# proper shutdown button
def shutdown():
    check_call(['sudo', 'poweroff'])
#
# check running pid
def pidof(cmd):
    cp = subprocess.run(["pidof", cmd],check=True,capture_output=True,text=True)
    if cp.returncode:
        return 0
    else:
        return int(cp.stdout)
#
# fork/exec vlc
def run_vlc():
    global VLC_RUNNING
    pid = os.fork()
    if pid >0:
        # we're in parent: do nothing
        VLC_RUNNING=True
    else:
        # child process: exec the actual work!
        os.system("/usr/bin/vlc -I dummy http://onair15.xdevel.com:7936")
        exit
#
# music on/off button
def vlc_toggle():
    global VLC_RUNNING
    pid = pidof("vlc")
    print("Target PID: ", pid)
    if pid:
        # Determine wheter it is stopped or not
        if VLC_RUNNING:
            os.kill(pid, signal.SIGSTOP)
            VLC_RUNNING=False
        else:
            os.kill(pid, signal.SIGCONT)
            VLC_RUNNING=True
    else:
        run_vlc()
#   
# WaveShare's WM8960-Audio-HAT has got a button on GPIO#17
wm8960_btn = Button(17, hold_time=3)
wm8960_btn.when_held = shutdown
wm8960_btn.when_released = vlc_toggle
#
# main: start vlc
run_vlc()
#
# start clock
os.system("~/digital_clock.sh &")
#
# Impostazione sveglie come da crontab della pir8radio2:
# m h  dom mon dow   command
#30 06	*   *	1-5	$HOME/vlc_send.sh play
scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(vlc_toggle, trigger='cron', minute=30, hour=6, day_of_week='0-4')
scheduler.add_job(vlc_toggle, trigger='cron', minute=00, hour=19, day_of_week='0-6')
#
# wait for next event
pause()
