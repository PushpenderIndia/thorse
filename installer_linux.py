#!/usr/bin/python3

import os, sys
from datetime import datetime
from datetime import date

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def isRoot():
    if not os.geteuid() == 0:
        sys.exit("{RED}[!] Installer must be run as root")

def getCurrentTime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")  
    
def getCurrentDate():
    return date.today().strftime("%Y-%m-%d")
    
def printInfo(text):
    print(f"[{BLUE}{getCurrentTime()}{WHITE}] [{GREEN}INFO{WHITE}] " + text)
    
def printWarning(text):
    print(f"[{BLUE}{getCurrentTime()}{WHITE}] [{YELLOW}WARNING{WHITE}] " + text)    

def install_wine():
    result = os.system("wine > /dev/null 2>&1")
    if result != 0:
        printWarning(f"wine is not installed. {GREEN}Installing...{WHITE}")
        os.system("apt-get update && apt-get install wine")
        
def install_wine32_pip_and_pyinstaller():
    printInfo(f"installing wine32, python3-pip, pyinstaller ...")
    os.system("dpkg --add-architecture i386 && apt-get update && apt-get install wine32 python3-pip pyinstaller && apt-get install python3-dev")
    
def download_python():
    printInfo(f"downloading Python v3.7 (32 Bit) ...")
    os.system("wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe")

def download_pywin32():
    printInfo(f"downloading Pywin32 (32 Bit) ...")
    os.system("wget https://github.com/mhammond/pywin32/releases/download/b227/pywin32-227.win32-py3.7.exe")    
   
def install_python():
    printInfo(f"installing Python3.7, you must continue its installation manually")
    print("\n=====================================================================")
    print(f"{YELLOW}[*] PLEASE NOTE : {WHITE}Choose Custom Install & Install Python to drive_c")
    print("=====================================================================\n")
    os.system("wine python-3.7.4.exe")
    
def install_pywin32():
    printInfo(f"installing Pywin32, you must continue its installation manually")
    os.system("wine pywin32-227.win32-py3.7.exe")
    
def install_python_dependencies():
    printInfo(f"installing Python3.7 dependencies ...")
    os.system("wine ~/.wine/drive_c/Python37-32/python.exe -m pip install pyinstaller mss==4.0.3 essential_generators==0.9.2 six==1.12.0 python-xlib==0.25 win32gui")

def install_python_main_dependencies():
    printInfo(f"installing main host Python3 dependencies ...")
    os.system("pip3 install mss==4.0.3")
    os.system("pip3 install essential_generators==0.9.2")
    os.system("pip3 install six==1.12.0")
    os.system("pip3 install python-xlib==0.25")
    
    printInfo(f"{GREEN}[+] Done!")

        
if __name__ == '__main__':
    isRoot()
    
    print(f"\n[*] starting installation @ {getCurrentTime()} /{getCurrentDate()}/\n")
    
    if os.path.exists("~/.wine/drive_c/Python37-32/") == False:
        install_wine()
        install_wine32_pip_and_pyinstaller()
        download_python()
        download_pywin32
        install_python()
        install_pywin32()
        install_python_dependencies()
        install_python_main_dependencies()
        
        
        
        
        
