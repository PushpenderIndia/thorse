sudo dpkg --add-architecture i386 && apt-get update && apt-get install -y wine32 python3-pip pyinstaller
#Downloading Required Executables
wget https://www.python.org/ftp/python/3.7.4/python-3.7.4.exe
wget https://github.com/mhammond/pywin32/releases/download/b227/pywin32-227.win32-py3.7.exe
#Installing Executables in Wine
sudo wine msiexec /i python-3.7.4.exe
sudo wine pywin32-227.win32-py3.7.exe
#Installing Dependencies [Python Modules] in Wine
sudo wine ~/.wine/drive_c/Python37-32/python.exe -m pip install pyinstaller mss==4.0.3 essential_generators==0.9.2 six==1.12.0 python-xlib==0.25 win32gui pywin32
#Installing Dependencies in Linux 
sudo pip3 install mss==4.0.3
sudo pip3 install essential_generators==0.9.2
sudo pip3 install six==1.12.0 
sudo pip3 install python-xlib==0.25
