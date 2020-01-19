#!/usr/bin/env python3
import os, signal, subprocess, time
from signal import pause
from gpiozero import Button
from apscheduler.schedulers.background import BackgroundScheduler
#
# Global status
VLC_RUNNING=False
CLOCK_RUNNING=False
#
# proper shutdown button
def shutdown():
    subprocess.run(['sudo','poweroff'],check=True)
#
# check running pid
def pidof(cmd):
    cp = subprocess.run(["pidof",cmd],check=True,capture_output=True,text=True)
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
        # child process: do the actual work!
        subprocess.run(["/usr/bin/vlc","-I","dummy","http://onair15.xdevel.com:7936"],check=True,capture_output=True,text=True)
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
# no way of getting PID from pidof() when cmd is like "python digital_clock.py"
def pidof_clock():
    cp = subprocess.run("ps -ux|grep -w python|grep -w digital_clock|awk '{print $2}'",check=True,capture_output=True,text=True)
    if cp.returncode:
        return 0
    else:
        return int(cp.stdout)
#
# verifica se l'orologio è in funzione
def check_clock():
    global CLOCK_RUNNING
    pid = pidof_clock()
    if pid:
        # clock is running already --> do nothing
        CLOCK_RUNNING=True
    else:
        run_clock()
#
# esegue l'orologio in modo thread-safe
def run_clock():
    global CLOCK_RUNNING
    pid = os.fork()
    if pid:
        # we're in parent!
        CLOCK_RUNNING=True
    else:
        # in child: let's do the actual work!
        subprocess.run("cd ~/luma_examples/examples && ./digital_clock.py",check=True)
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
    # start vlc (reentrant, as it forks)
    run_vlc()
    #
    # start clock (reentrant, as it forks as well)
    run_clock()
    #
    # event loop
    pause()