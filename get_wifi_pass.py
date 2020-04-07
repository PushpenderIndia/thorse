import subprocess, re

class GetWifiPassword:
    def __init__(self):
        self.command = "netsh wlan show profile"
        self.result = ""
        
    def start(self):
        networks = subprocess.check_output(self.command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        networks = networks.decode(encoding="utf-8", errors="strict")
        network_names_list = re.findall("(?:Profile\s*:\s)(.*)", networks) 

        for network_name in network_names_list:
            try:
                command = "netsh wlan show profile " + network_name + " key=clear"
                current_result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
                current_result = current_result.decode(encoding="utf-8", errors="strict")        
                
                ssid = re.findall("(?:SSID name\s*:\s)(.*)", str(current_result))
                authentication = re.findall(r"(?:Authentication\s*:\s)(.*)", current_result)
                cipher = re.findall("(?:Cipher\s*:\s)(.*)", current_result)
                security_key = re.findall(r"(?:Security key\s*:\s)(.*)", current_result)
                password = re.findall("(?:Key Content\s*:\s)(.*)", current_result)
                
                self.result += "\n\nSSID           : " + ssid[0] + "\n"
                self.result += "Authentication : " + authentication[0] + "\n"
                self.result += "Cipher         : " + cipher[0] + "\n"
                self.result += "Security Key   : " + security_key[0] + "\n"
                self.result += "Password       : " + password[0] 
            except Exception:
                pass
        
        return self.result
        
if __name__ == '__main__':
    test = GetWifiPassword()
    result = test.start()
    print(result)

