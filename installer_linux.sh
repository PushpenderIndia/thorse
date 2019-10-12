#!/usr/bin/env bash

rm /var/lib/dpkg/lock
rm /var/cache/apt/archives/lock
rm /var/lib/apt/lists/lock
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y wine32 python-pip pyinstaller
wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe
wine msiexec /i python-3.7.4.exe
sudo wine ~/.wine/drive_c/Python37/python.exe -m pip install pyinstaller 
sudo pip install argparse
sudo pip install subprocess
sudo pip install base64
sudo pip install pyfiglet
sudo pip install socket
sudo pip install struct
sudo pip install time 
sudo pip install smtplib  
sudo pip install os
sudo pip install shutil
sudo pip install subprocess
sudo pip install sys
sudo pip install stat
sudo pip install platform
sudo pip install getpass
