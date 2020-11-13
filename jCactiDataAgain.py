#coding:utf-8
# 用于更新ll_data_log.csv（数据库）文件后的重新生成cacti监控图
import matplotlib
import os
import datetime
import pandas
import paramiko
import matplotlib.pyplot as plt
from PIL import Image
from openpyxl import load_workbook


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
    average_bandwidth = []
    the_all_data_log = pandas.read_csv('all_data_log.csv').iloc[-30:, :].reset_index(drop=True)

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
        average_bandwidth.append(the_all_data_log.at[i, 'average_bandwidth'])

    plt.figure(figsize=(30, 30))
    ax1 = plt.subplot2grid((30, 10), (23, 0), rowspan=10, colspan=11)
    font_title = matplotlib.font_manager.FontProperties(fname=r'the_font.ttf', size=20)
    font_week = matplotlib.font_manager.FontProperties(fname=r'the_font.ttf', size=10)
    font_num = matplotlib.font_manager.FontProperties(fname=r'the_font.ttf', size=8)

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
    for xx, yy, zz in zip(x_lab, all_user, average_bandwidth):
        ax1.text(xx, max(ck_flow+hl_flow)+260, '总用户数\n' + str(yy) + '\n'*4 +
                 '户均带宽\n' + str(zz) + '\nKbps/户', ha='center', fontproperties=font_num)
    for xx in x_lab:
        ax1.text(xx, -90, xx.split('\n')[0] + '\n' + xx.split('\n')[1][:5], ha='center', fontsize=9)

    week_dic = {'0': '日', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六'}
    for xx in x_lab:
        the_num = datetime.datetime(year=2020,
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

    plt.savefig('pic_data.png')


def mix_pic():
    the_pic_data = Image.open('pic_data.png').convert('RGBA')
    the_pic_back = Image.open('pic_back.png').convert('RGBA')
    the_pic_ok = Image.alpha_composite(the_pic_data, the_pic_back)
    the_pic_ok.save('pic_ok.png')
    os.remove('pic_data.png')


def update_pic():
    ssh = paramiko.SSHClient()
    know_host = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(know_host)
    ssh.connect(hostname='10.2.205.55', port=22, username='root', password='jsm@96633')
    the_cmd = r'wget "ftp://10.2.205.6/jay/pic_ok.png" --ftp-user=shiyan --ftp-password=123 ' \
              r'-O /var/www/html/plugins/weathermap/images/pic_ok.png'
    stdin, stdout, stderr = ssh.exec_command(the_cmd)
    ssh.close()


def update_excel(the_excel):
    the_data = pandas.read_csv('all_data_log.csv').iloc[-1:, :]
    the_data = the_data.values.tolist()[0]
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
    cell_average_bandwidth = sheet['C7']
    cell_average_bandwidth.value = str(the_data[10]) + ' kbps'
    cell_ck_per = sheet['D3']
    cell_ck_per.value = str(the_data[5]) + ' %'
    cell_hl_per = sheet['D4']
    cell_hl_per.value = str(the_data[6]) + ' %'
    cell_idc_per = sheet['D5']
    cell_idc_per.value = str(the_data[7]) + ' %'
    cell_nwl_per = sheet['E7']
    cell_nwl_per.value = str(the_data[8]) + ' %'
    cell_all_user = sheet['E6']
    cell_all_user.value = str(the_data[9]) + ' 万'
    workbook.save(filename=the_excel)


if __name__ == '__main__':
    drawing()  # 1
    mix_pic()  # 2
    # 执行1和2后，rz上传pic_ok.png

    # update_pic()
    # 3 更新cacti监控图

    # update_excel('ok.xlsx')
    # 4 更新每晚值班报表
