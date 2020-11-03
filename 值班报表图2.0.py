# pyinstaller -F Zhiban2.0.py
from win32com.client import DispatchEx
from PIL import ImageGrab
import pythoncom
import os
import wget

print('\n程序正在执行请等待……')
wget.download('ftp://shiyan:123@10.2.205.6/jay/ok.xlsx', out=os.getcwd()+'\\ok.xlsx')
pythoncom.CoInitialize()
excel = DispatchEx("Excel.Application")
excel.Visible = False
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
x = input('\n\n程序执行完毕,按回车键后退出！')

'''import xlwings as xw
def excel_pic2_linux(the_every_duty_file):
    app = xw.App(visible=True, add_book=False)
    wb = app.books.open(the_every_duty_file)
    sht = wb.sheets['Sheet1']
    range_val = sht.range((1, 1), (8, 5))
    range_val.api.CopyPicture()
    sht.api.Paste()
    pic = sht.pictures[0]
    pic.api.Copy()
    img = ImageGrab.grabclipboard()
    img.save('/jay/ok.png')
    pic.delete()
    wb.close()
    app.quit()
    # os.remove('/jay/ok.xlsx')'''
