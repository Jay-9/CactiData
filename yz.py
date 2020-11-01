# pyinstaller -F yz.py
import os
import wget
wget.download('ftp://shiyan:123@10.2.205.6/jay/ok.xlsx', out=os.getcwd()+'\\ok.xlsx')