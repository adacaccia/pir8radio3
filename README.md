# pir8radio3 build instructions
# (C) 2020 AMC SoftWorks Co.Ltd.
#
# WaveShare wm8960-soundcard
# (da: https://www.waveshare.com/w/upload/5/54/WM8960_Audio_HAT_User_Manual_EN.pdf)
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh
sudo reboot
#
# VLC media player 3.0.8 Vetinari (revision 3.0.8-0-gf350b6b5a7)
sudo apt install -y vlc
#
# Python digital_clock based on luma.examples by Richard Hull
# (da: https://github.com/rm-hull/luma.examples)
sudo usermod -a -G i2c,spi,gpio pi
sudo apt install python-dev python-pip libfreetype6-dev libjpeg-dev build-essential
sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev
#
# Log out and in again and clone this repository:
git clone https://github.com/rm-hull/luma.examples.git
cd luma.examples
#
# Finally, install the luma libraries using:
# (avoiding memory problems on rpi0, as pillow-6.0.6 causes memory exception:)
sudo -H pip install -Iv Pillow==4.3.0
sudo -H pip install -e .
#
# digital_clock.py by AMC:
scp digital_clock.sh pi@pir8radio3:
scp digital_clock.py pi@pir8radio3:luma.examples/examples/
scp Arial\ Narrow.ttf pi@pir8radio3:luma.examples/examples/fonts/
#
# .profile:
# Digital Clock by AMC
~/digital_clock.sh
#
# wm8960-soundcard has got a Button on GPIO#17:
# (da: https://www.waveshare.com/w/upload/5/54/WM8960_Audio_HAT_User_Manual_EN.pdf)
sudo apt install python3-gpiozero


