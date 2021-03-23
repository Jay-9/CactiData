#coding=gbk

import matplotlib
matplotlib.use('Agg')
from PIL import Image
from threading import Timer
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import os
import time
import json
import pandas
import pymysql
import datetime
import requests
import paramiko
import cx_Oracle
''' matplotlib pillow openpyxl pandas pymysql requests paramiko cx_Oracle '''


def get_sor_data():
    the_current = int(time.mktime((datetime.datetime.now() + datetime.timedelta(minutes=-5)).timetuple()))
    the_current_ago = int(time.mktime((datetime.datetime.now() + datetime.timedelta(hours=-1)).timetuple()))
    the_url = 'http://10.2.205.55/graph_xport.php?local_graph_id=1729&rra_id=1&view_type=&graph_start=%d&graph_end=%d'\
              % (the_current_ago, the_current)
    the_result = requests.post(url=the_url,
                               data={'action': 'login', 'login_username': 'admin', 'login_password': 'syc@9036idcJk'})\
        .text.replace('"', '')
    with open(datetime.datetime.now().strftime('%Y-%m-%d') + '.csv', 'w', encoding='utf-8') as f:
        f.write(the_result)

    con_boss_oracle = cx_Oracle.connect('inter/inter#2016@10.2.75.23:1521/orcl')
    cursor_boss = con_boss_oracle.cursor()
    cursor_boss.execute("select sum(BRD_NUM) from inter.realbrd_num where DAY_ID=%s" % datetime.datetime.now().strftime('%Y%m%d'))
    the_all_user = round(cursor_boss.fetchone()[0] / 10000, 2)
    cursor_boss.close()
    con_boss_oracle.close()
    return datetime.datetime.now().strftime('%Y-%m-%d') + '.csv', the_all_user


def data_calculation(the_sor_file, the_all_user, the_dic_online):
    the_all_data = pandas.read_csv(the_sor_file, skiprows=9, usecols=[0, 8, 9, 10, 34])
    today_data = pandas.DataFrame(columns=the_all_data.columns)
    for row in the_all_data.itertuples():
        if int(row.Date.replace('/', '-').split(' ')[0].split('-')[2]) == int(datetime.datetime.now().strftime('%d')) and int(row.Date.replace('/', '-').split(' ')[1].split(':')[0]) >= 19:
            today_data = today_data.append(the_all_data.iloc[row.Index, :])
    today_data = today_data.reset_index(drop=True)
    max_time = today_data.iloc[today_data.iloc[:, 4].astype(float).idxmax(), 0]
    ck_flow = round(today_data.iloc[today_data.iloc[:, 4].astype(float).idxmax(), 1]/1000/1000/1000, 2)
    hl_flow = round(today_data.iloc[today_data.iloc[:, 4].astype(float).idxmax(), 2]/1000/1000/1000, 2)
    idc_flow = round(today_data.iloc[today_data.iloc[:, 4].astype(float).idxmax(), 3]/1000/1000/1000, 2)
    total_flow = round(today_data.iloc[:, 4].max()/1000/1000/1000, 2)
    ck_per = round(ck_flow/total_flow*100, 2)
    hl_per = round(hl_flow/total_flow*100, 2)
    idc_per = round(idc_flow/total_flow*100, 2)
    nwl_per = round(hl_per + idc_per, 2)
    all_user = the_all_user
    all_bandwidth = round(total_flow/all_user*100, 2)
    if max_time[-8:-3] in the_dic_online.keys():
        online_user = round(the_dic_online[max_time[-8:-3]]/10000, 2)
    else:
        online_user = 1
    online_bandwidth = round(total_flow/online_user*100, 2)

    os.remove(the_sor_file)
    return [max_time, ck_flow, hl_flow, idc_flow, total_flow, ck_per, hl_per, idc_per, nwl_per,
            all_user, all_bandwidth, online_user, online_bandwidth]


def log_csv(the_one_data_log):
    columns = ['max_time', 'ck_flow', 'hl_flow', 'idc_flow', 'total_flow', 'ck_per', 'hl_per', 'idc_per', 'nwl_per',
               'all_user', 'all_bandwidth', 'online_user', 'online_bandwidth']
    the_insert_data = pandas.DataFrame(columns=columns, data=[the_one_data_log])
    the_insert_data.to_csv('/jay/all_data_log.csv', mode='a', header=False, index=False, columns=columns)


def drawing():
    x_lab = []
    ck_flow = []
    hl_flow = []
    idc_flow = []
    total_flow = []
    ck_per = []
    hl_per = []
    idc_per = []
    nwl_per = []
    all_user = []
    all_bandwidth = []
    the_all_data_log = pandas.read_csv('/jay/all_data_log.csv').iloc[-30:, :].reset_index(drop=True)

    for i in range(the_all_data_log.shape[0]-1, -1, -1):
        x_lab.append(the_all_data_log.at[i, 'max_time'][5:].replace(' ', '\n'))
        ck_flow.append(the_all_data_log.at[i, 'ck_flow'])
        hl_flow.append(the_all_data_log.at[i, 'hl_flow'])
        idc_flow.append(the_all_data_log.at[i, 'idc_flow'])
        total_flow.append(the_all_data_log.at[i, 'total_flow'])
        ck_per.append(the_all_data_log.at[i, 'ck_per'])
        hl_per.append(the_all_data_log.at[i, 'hl_per'])
        idc_per.append(the_all_data_log.at[i, 'idc_per'])
        nwl_per.append(the_all_data_log.at[i, 'nwl_per'])
        all_user.append(the_all_data_log.at[i, 'all_user'])
        all_bandwidth.append(the_all_data_log.at[i, 'all_bandwidth'])

    plt.figure(figsize=(30, 30))
    ax1 = plt.subplot2grid((30, 10), (23, 0), rowspan=10, colspan=11)
    font_title = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=20)
    font_week = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=10)
    font_num = matplotlib.font_manager.FontProperties(fname=r'/jay/the_font.ttf', size=8)

    # ax1.set_xlabel("日       期", fontproperties = font_title)
    ax1.set_ylabel("流       量", fontproperties=font_title)
    ax1.set_title("流    量    统    计    图\n", fontproperties=font_title)
    ax1.set_ylim([0, max(total_flow) + 50])
    ax1.set_xticks([])

    legend_ck = ax1.bar(x_lab, ck_flow, color=['#FF7648'], align='center')
    legend_hl = ax1.bar(x_lab, hl_flow, color=['#8FD9F8'], bottom=ck_flow, align='center')
    legend_idc = ax1.bar(x_lab, idc_flow, color=['#DDEFBF'], bottom=hl_flow, align='center')
    ax1.set_xticks(range(0, 30))

    # ax1.spines['bottom'].set_color('r')
    ax1.spines['left'].set_position(('data', -1.5))
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')

    for xx, yy, zz in zip(x_lab, ck_flow, ck_per):
        ax1.text(xx, 10, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
    for xx, yy, zz in zip(x_lab, hl_flow, hl_per):
        ax1.text(xx, max(ck_flow)+5, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
    for xx, yy, zz in zip(x_lab, idc_flow, idc_per):
        ax1.text(xx, max(ck_flow+hl_flow) + 5, str(yy) + 'G\n' + str(zz) + '%', ha='center', fontsize=7)
    for xx, yy, zz in zip(x_lab, nwl_per, total_flow):
        ax1.text(xx, max(total_flow)-60, '总流量\n' + str(zz) + 'G\n\n' + '内网率\n' + str(yy) + '%', ha='center',
                 fontproperties=font_num)
    for xx, yy, zz in zip(x_lab, all_user, all_bandwidth):
        ax1.text(xx, max(ck_flow+hl_flow)+260, '总用户数\n' + str(yy) + '\n'*4 +
                 '户均带宽\n' + str(zz) + '\nKbps/户', ha='center', fontproperties=font_num)
    for xx in x_lab:
        ax1.text(xx, -90, xx.split('\n')[0] + '\n' + xx.split('\n')[1][:5], ha='center', fontsize=9)

    week_dic = {'0': '日', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六'}
    for xx in x_lab:
        the_num = datetime.datetime(year=2021,
                                month=int(xx.split('\n')[0].replace('-', ',').replace('/', ',').split(',')[0]),
                                day=int(xx.split('\n')[0].replace('-', ',').replace('/', ',').split(',')[1]))\
            .strftime('%w')
        ax1.text(xx, max(ck_flow+hl_flow)+120, week_dic[the_num], ha='center', fontproperties=font_week)

    ax2 = plt.subplot2grid((30, 10), (19, 0), colspan=1, rowspan=2)
    ax2.legend(handles=[legend_idc, legend_hl, legend_ck], labels=["I D C", "互联互通", "出    口"], loc=2, prop=font_title)
    ax2.axis('off')

    ax3 = ax1.twinx()
    ax3.spines['left'].set_color('none')
    ax3.spines['right'].set_position(('data', -1.5))
    ax3.spines['top'].set_color('none')
    ax3.plot(x_lab, nwl_per, color='r', linewidth=1)
    ax3.set_ylim([70, 98])
    ax3.set_xticks([])
    ax1.set_xticks([])

    ax4 = ax1.twinx()
    ax4.spines['left'].set_color('none')
    ax4.spines['top'].set_color('none')
    all_user = [eval(x) for x in all_user]
    ax4.plot(x_lab, all_user, color='b', linewidth=1)
    ax4.set_ylim([int(min(all_user)-5), int(max(all_user)+1)])
    ax4.set_xticks([])

    plt.savefig('/jay/pic_data.png')


def mix_pic():
    the_pic_data = Image.open('/jay/pic_data.png').convert('RGBA')
    the_pic_back = Image.open('/jay/pic_back.png').convert('RGBA')
    the_pic_ok = Image.alpha_composite(the_pic_data, the_pic_back)
    the_pic_ok.save('/jay/pic_ok.png')
    os.remove('/jay/pic_data.png')


def update_pic():
    """
    ssh = paramiko.SSHClient()
    know_host = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(know_host)
    ssh.connect(hostname='10.2.205.55', port=22, username='tommy', password='jf7d$HoA6n!9')
    the_cmd = r'wget "ftp://10.2.205.6/jay/pic_ok.png" --ftp-user=shiyan --ftp-password=jf7d$HoA6n!9 ' \
              r'-O /var/www/html/plugins/weathermap/images/pic_ok.png'
    stdin, stdout, stderr = ssh.exec_command(the_cmd)
    ssh.close()"""
    j = paramiko.Transport(('10.2.205.55', 22))
    j.connect(username='tommy', password='jf7d$HoA6n!9')
    sftp = paramiko.SFTPClient.from_transport(j)
    sftp.put('/jay/pic_ok.png', '/var/www/html/plugins/weathermap/images/pic_ok.png')


def update_excel(the_excel, the_data):
    workbook = load_workbook(filename=the_excel)
    sheet = workbook.active
    cell_max_time = sheet['A1']
    cell_max_time.value = the_data[0][:4] + '年\n' + the_data[0][5:7] + '月\n' + the_data[0][8:10] + '日'
    cell_ck_flow = sheet['C3']
    cell_ck_flow.value = str(the_data[1]) + ' Gbps'
    cell_hl_flow = sheet['C4']
    cell_hl_flow.value = str(the_data[2]) + ' Gbps'
    cell_idc_flow = sheet['C5']
    cell_idc_flow.value = str(the_data[3]) + ' Gbps'
    cell_total_flow = sheet['C6']
    cell_total_flow.value = str(the_data[4]) + ' Gbps'
    cell_all_user = sheet['C7']
    cell_all_user.value = str(the_data[9]) + ' 万'
    cell_online_user = sheet['C8']
    cell_online_user.value = str(the_data[11]) + ' 万'
    cell_ck_per = sheet['D3']
    cell_ck_per.value = str(the_data[5]) + ' %'
    cell_hl_per = sheet['D4']
    cell_hl_per.value = str(the_data[6]) + ' %'
    cell_idc_per = sheet['D5']
    cell_idc_per.value = str(the_data[7]) + ' %'
    cell_nwl_per = sheet['E6']
    cell_nwl_per.value = str(the_data[8]) + ' %'
    cell_all_bandwidth = sheet['E7']
    cell_all_bandwidth.value = str(the_data[10]) + ' kbps'
    cell_online_bandwidth = sheet['E8']
    cell_online_bandwidth.value = str(the_data[12]) + ' kbps'
    workbook.save(filename=the_excel)


def star_process():
    con_aaa_mysql = pymysql.connect(
        host='172.28.0.29', port=3306, user='cacti', password='8NM)V6hb', database='ua_new', charset='utf8')
    cursor_aaa = con_aaa_mysql.cursor(pymysql.cursors.DictCursor)
    cursor_aaa.execute('select count(*) from ua_broadband_user_online')
    count_online = cursor_aaa.fetchone()
    cursor_aaa.close()
    con_aaa_mysql.close()

    time_now = datetime.datetime.now().strftime("%H:%M")
    the_timer = Timer(60, star_process)
    the_timer.start()
    dic_online.update({time_now: count_online['count(*)']})


    if time_now == '21:30':
        aaa_csv_data = json.dumps(dic_online)
        with open("/jay/aaa_online.csv", "w+", encoding='utf-8') as aaa_csv:
            aaa_csv.write(aaa_csv_data)
        sor_file, all_user = get_sor_data()
        one_data_log = data_calculation(sor_file, all_user, dic_online)
        log_csv(one_data_log)
        drawing()
        mix_pic()
        update_pic()
        update_excel('/jay/every_duty.xlsx', one_data_log)
        the_timer.cancel()


if __name__ == '__main__':
    dic_online = {}
    star_process()
