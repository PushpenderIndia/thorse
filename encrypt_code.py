#!/usr/bin/env python
import base64

#==================================================================
#Author : Pushpender Singh
#Website: https://technowlogy.tk
#==================================================================
#Usage: Module is build to Encrypt Source Codes of Python file.
#==================================================================
#Github: https://github.com/Technowlogy-Pushpender/
#==================================================================

class Encrypt:
    def __init__(self):
        self.YELLOW, self.GREEN = '\33[93m',  '\033[1;32m'
        self.text = ""
        self.enc_txt = ""

    def encrypt(self, filename):
        print(f"\n{self.YELLOW}[*] Encrypting Source Codes...")
        with open(filename, "r") as f:
            lines_list = f.readlines()
            for lines in lines_list:
                self.text += lines
              
            self.text = self.text.encode()
            self.enc_txt =  base64.b64encode(self.text)   

        with open(filename, "w") as f:
            f.write(f"import base64; exec(base64.b64decode({self.enc_txt}))")
            
        print(f"{self.GREEN}[+] Operation Completed Successfully!\n")
    
if __name__ == '__main__':   
    test = Encrypt()
    filename = input("Please Enter Filename: ")
    test.encrypt(filename)