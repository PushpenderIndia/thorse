import subprocess
from urllib.request import urlopen
import banners
import time
import os

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def update_client_version(version):
    with open("version.txt", "r") as vnum:
        if vnum.read() != version:
            return True
        else:
            return False

def exit_greet():
    try:
        os.system('cls')
    except Exception as e:
        os.system('clear')        
    print(GREEN + '''Thank You for using TechNowHorse, Think Great & Touch The Sky!  \n''' + END)
    quit() 

def main():
    try:
        version = urlopen("https://raw.githubusercontent.com/PushpenderIndia/technowhorse/master/version.txt").read()
    except Exception as e:
        print("[!] Unable to Fletch Origin version.txt")
        print("[!] Please Check Your Internet Connection!")
        print("[*] Exiting ...")
        quit()
        
    if update_client_version(version) is True:
        subprocess.call(["git", "pull", "origin", "master"])
        return "[+] Updated to latest version: v{}..".format(version)
    else:
        return "[*] You are already up to date with git origin master :)"


if __name__ == '__main__':
    try:
        print(banners.get_banner())
        print(f"\t{YELLOW}Author: {GREEN}Pushpender | {YELLOW}GitHub: {GREEN}PushpenderIndia\n")
        print(f"{YELLOW}[*] Welcome to TechNowHorse's Auto Updater")
        print(f"{GREEN}[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]")
        print(f"{YELLOW}[*] Please Note : Git must be installed in order to use \"updater.py\"")
        time.sleep(5)
        print(f"{GREEN}[++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++]")
        print(f"{YELLOW}[*] Checking TechNowHorse's version information..")
        print(main())
        print(f"{END}[*] Exiting ...")
        
    except KeyboardInterrupt:
        exit_greet()
        quit()