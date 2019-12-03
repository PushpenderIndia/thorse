#!/usr/bin/env bash

rm /var/lib/dpkg/lock
rm /var/cache/apt/archives/lock
rm /var/lib/apt/lists/lock
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y wine32 python-pip pyinstaller
wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe
wine msiexec /i python-3.7.4.exe
sudo wine ~/.wine/drive_c/Python37/python.exe -m pip install pyinstaller mss==4.0.3 essential_generators==0.9.2 six==1.12.0 pywin32 python-xlib==0.25
sudo pip install mss==4.0.3
sudo pip install essential_generators==0.9.2
sudo pip install six==1.12.0 
sudo pip install python-xlib==0.25
sudo pip install pywin32
