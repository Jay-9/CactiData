import os
import wget
from PIL import ImageGrab, Image
from win32com.client import DispatchEx


print('\n正在运行，请稍后……')
for file_name in os.listdir(os.getcwd()):
    full_name = os.getcwd() + '\\' + file_name
    if os.path.isdir(full_name):
        continue
    elif os.path.isfile(full_name):
        if len(file_name) >= 7 and file_name[:2] == 'ok' and file_name[-5:] == '.xlsx':
            os.remove(full_name)

wget.download('ftp://shiyan:123@10.2.205.6/jay/ok.xlsx', out=os.getcwd()+'\\ok.xlsx')
os.system(r'attrib +H ok.xlsx')
excel = DispatchEx("Excel.Application")
excel.Visible = excel.DisplayAlerts = False
wb = excel.Workbooks.Open(os.getcwd()+'\\ok.xlsx')
ws = wb.Sheets(1)
ws.Range('A1:E8').CopyPicture()
ws.Paste()
excel.Selection.ShapeRange.Name = 'J'
ws.Shapes('J').Copy()
img = ImageGrab.grabclipboard()
img.save(os.getcwd()+'\\no.png')
os.system(r'attrib +H no.png')
wb.Close(SaveChanges=0)
excel.Quit()
os.remove(os.getcwd()+'\\ok.xlsx')

img = Image.open(os.getcwd()+'\\no.png')
alpha = img.convert('RGBA').split()[-1]
img_ok = Image.new("RGBA", img.size, (255, 255, 255) + (255,))
img_ok.paste(img, mask=alpha)
img_ok.save(os.getcwd()+'\\ok.png')
os.remove(os.getcwd()+'\\no.png')


'''def excel_pic2():
    print('\n正在运行，请稍后……')
    wget.download('ftp://shiyan:123@10.2.205.6/jay/ok.xlsx')
    os.system(r'attrib +H ok.xlsx')
    app = xlwings.App(visible=False, add_book=False)
    wb = app.books.open('ok.xlsx')
    sht = wb.sheets[0]
    range_val = sht.range((1, 1), (8, 5))
    range_val.api.CopyPicture()
    sht.api.Paste()
    pic = sht.pictures[0]
    pic.api.Copy()
    img = ImageGrab.grabclipboard()
    img.save('ok.png')
    pic.delete()
    wb.close()
    app.quit()
    os.remove(os.getcwd()+'\\ok.xlsx')'''
