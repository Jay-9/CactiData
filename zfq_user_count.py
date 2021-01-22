#coding=utf-8
import sys
import time
import datetime
import re
import math
import MySQLdb
import requests
import json
import cPickle
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding('utf-8')


pbs=['和龙','图们','安图','延吉','延边州','珲春']
pdb=[]

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
s = requests.Session()
head = {
    "Connection" : "keep-alive",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    "charset": "UTF-8"}


#获取lt
response = s.get('http://10.2.75.2:8080/sso/login') 
soup = BeautifulSoup(response.content, "html.parser")
lt = soup.select('form > input')[0].get('value')

#登陆
response = s.post('http://10.2.75.2:8080/sso/login',data='username=177777&password=123456&lt='+lt+'&_eventId=submit', headers = head)
#print response.content

#进入报表统计
response = s.get('http://10.2.75.4:8088/sdp/p1496641595315_AutoCreateZul_42.zul')
pos0=response.content.find('dt:')+4
pos1=response.content.find('\'',pos0)
pos2=response.content.find('zul.wgt.Button')+17
pos3=response.content.find('\'',pos2)
pos4=response.content.find('zul.mesh.Paging')+18
pos5=response.content.find('\'',pos4)
pos6=response.content.find('zul.utl.Timer')+16
pos7=response.content.find('\'',pos6)

dtid = response.content[pos0:pos1]
uuid_0 = response.content[pos2:pos3]
uuid_1 = response.content[pos4:pos5]
Timer = response.content[pos6:pos7]


print dtid,uuid_0,uuid_1#,Timer




#取消本地网全部
pos8=response.content.find("',{$onCheck:true,label:'全部',checked:true")
print response.content[pos8-6:pos8].replace("'","")
response = s.post('http://10.2.75.4:8088/sdp/zkau',data='dtid='+dtid+'&cmd_0=onCheck&uuid_0='+response.content[pos8-6:pos8].replace("'","")+'&data_0={"":false}', headers = head)
#print response.content
#取消分公司全部
pos9=response.content.find("',{$onCheck:true,label:'全部',checked:true")
print response.content[pos9-6:pos9].replace("'","")
response = s.post('http://10.2.75.4:8088/sdp/zkau',data='dtid='+dtid+'&cmd_0=onCheck&uuid_0='+response.content[pos9-6:pos9].replace("'","")+'&data_0={"":false}', headers = head)




totalUser=allUser=0

#查询第一页
response = s.post('http://10.2.75.4:8088/sdp/zkau',data='dtid='+dtid+'&cmd_0=onClick&uuid_0='+uuid_0+'&data_0={"pageX":668,"pageY":141,"which":1,"x":22,"y":12}', headers = head)
#print json.loads(response.content)
list=re.findall(r"tooltiptext:'([^']+)'",str(response.content))
    



#查询第二页
response = s.post('http://10.2.75.4:8088/sdp/zkau',data='dtid='+dtid+'&cmd_0=onPaging&uuid_0='+uuid_1+'&data_0={"":1}', headers = head)
#print response.content
list=list+re.findall(r"tooltiptext:'([^']+)'",str(response.content))


#查询第三页
response = s.post('http://10.2.75.4:8088/sdp/zkau',data='dtid='+dtid+'&cmd_0=onPaging&uuid_0='+uuid_1+'&data_0={"":2}', headers = head)
#print response.content
list=list+re.findall(r"tooltiptext:'([^']+)'",str(response.content))

    
list1=[]

for i in range (1,len(list)):
    if list[i-1].isdigit()==False and list[i].isdigit()==False:
        print list[i-1]
            
    else:
        list1.append(list[i-1])
#print list1


for i in range(0, len(list1)/11):
    print list1[i*11],list1[i*11+2]
    if not list1[i*11] in pbs:
        totalUser+=int(list1[i*11+2])
    allUser+=int(list1[i*11+2])

print totalUser,allUser


'''
db = MySQLdb.connect(host="localhost",user="root",passwd="110324",db="Internet",charset="utf8")
cursor = db.cursor()
sql="INSERT INTO bandwidth(date,totalBandwidth,ckBandwidth,hlhtBandwidth,idcBandwidth,intranetRate,totalUsers,allUsers ) VALUES('1970-01-01 00:00:00','0','0','0','0','0',"+str(float(totalUser)/10000)+","+str(float(allUser)/10000)+");"
try:
    cursor.execute(sql)
except Exception,e:
    db.rollback()
    print Exception,e,sql,"写入失败"
db.commit()
'''
response = s.get('http://10.2.205.6/cgi-bin/updata.py?Number_of_users='+str(float(totalUser)/10000)+'&ALL_users='+str(float(allUser)/10000))
print response.content

