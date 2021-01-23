import os
import wget
from PIL import ImageGrab, Image
from win32com.client import DispatchEx


print('\n正在运行，稍后窗口会自动关闭……')
for file_name in os.listdir(os.getcwd()):
    if file_name == 'on_duty.xlsx':
        os.remove(os.getcwd() + '\\' + file_name)

wget.download('ftp://shiyan:123@10.2.205.6/jay/on_duty.xlsx', out=os.getcwd()+'\\on_duty.xlsx')
os.system(r'attrib +H on_duty.xlsx')
excel = DispatchEx("Excel.Application")
excel.Visible = excel.DisplayAlerts = False
wb = excel.Workbooks.Open(os.getcwd()+'\\on_duty.xlsx')
ws = wb.Sheets(1)
ws.Range('A1:E9').CopyPicture()
ws.Paste()
excel.Selection.ShapeRange.Name = 'J'
ws.Shapes('J').Copy()
img = ImageGrab.grabclipboard()
img.save(os.getcwd()+'\\temp.png')
os.system(r'attrib +H temp.png')
wb.Close(SaveChanges=0)
excel.Quit()
os.remove(os.getcwd()+'\\on_duty.xlsx')

img = Image.open(os.getcwd()+'\\temp.png')
alpha = img.convert('RGBA').split()[-1]
img_ok = Image.new("RGBA", img.size, (255, 255, 255) + (255,))
img_ok.paste(img, mask=alpha)
img_ok.save(os.getcwd()+'\\Duty.png')
os.remove(os.getcwd()+'\\temp.png')
