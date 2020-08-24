#!/bin/bash


if [[ "$(id -u)" -ne 0 ]]; then
    printf "\e[1;77mPlease, run this program as root!\n\e[0m"
    exit 1
fi

command -v wine > /dev/null 2>&1 || { echo >&2 "[-] Wine is not installed. Installing..."; apt-get update && apt-get install wine; } 

if [[ ! -d ~/.wine/drive_c/Python37-32/ ]]; then

printf "\e[1;93m[*] Installing wine32, python3-pip, pyinstaller ...\e[0m"
printf "\e[1;93m===================================================\e[0m\n"
dpkg --add-architecture i386 && apt-get update && apt-get install wine32 python3-pip pyinstaller && apt-get install python3-dev

printf "\e[1;93m[*] Downloading Python v3.7 (32 Bit)\e[0m"
printf "\e[1;93m====================================\e[0m\n"
wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe

printf "\e[1;93m[*] Downloading PyWin32 (32 Bit)\e[0m"
printf "\e[1;93m================================\e[0m\n"
wget https://github.com/mhammond/pywin32/releases/download/b227/pywin32-227.win32-py3.7.exe

printf "\e[1;93m[*] Installing Python3.7, you must continue its installation manually\e[0m"
printf "\e[1;93m=====================================================================\e[0m"
printf "\e[1;93m[*] PLEASE NOTE : Choose Custom Install & Install Python to drive_c  \e[0m"
printf "\e[1;93m=====================================================================\e[0m\n"
wine python-3.7.4.exe

printf "\e[1;93m[*] Installing Pywin32, you must continue its installation manually\e[0m"
printf "\e[1;93m=====================================================================\e[0m\n"
wine pywin32-227.win32-py3.7.exe

printf "\e[1;93m[*] Installing Python3.7 dependencies\e[0m"
printf "\e[1;93m=====================================\e[0m\n"
wine ~/.wine/drive_c/Python37-32/python.exe -m pip install pyinstaller mss==4.0.3 essential_generators==0.9.2 six==1.12.0 python-xlib==0.25 win32gui pywin32
wine ~/.wine/drive_c/Python37-32/python.exe -m pip install --upgrade pywin32

printf "\e[1;93m[*] Installing Main Host Python3 dependencies\e[0m"
printf "\e[1;93m=============================================\e[0m\n"
pip3 install mss==4.0.3
pip3 install essential_generators==0.9.2
pip3 install six==1.12.0 
pip3 install python-xlib==0.25

else
exit 1
fi

printf "\e[1;92m[+] Done!\e[0m\n"
