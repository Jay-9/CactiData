# pyinstaller -F yz.py
from win32com.client import DispatchEx
from PIL import ImageGrab
import pythoncom
import os
import wget

wget.download('ftp://shiyan:123@10.2.205.6/jay/ok.xlsx', out=os.getcwd()+'\\ok.xlsx')
pythoncom.CoInitialize()
excel = DispatchEx("Excel.Application")
excel.Visible = True
excel.DisplayAlerts = False
wb = excel.Workbooks.Open(os.getcwd()+'\\ok.xlsx')
ws = wb.Sheets('Sheet1')
ws.Range('A1:E8').CopyPicture()
ws.Paste()
excel.Selection.ShapeRange.Name = 'ok.png'
ws.Shapes('ok.png').Copy()
img = ImageGrab.grabclipboard()
img.save(os.getcwd()+'\\ok.png')
wb.Close(SaveChanges=0)
excel.Quit()
pythoncom.CoUninitialize()
os.remove(os.getcwd()+'\\ok.xlsx')
