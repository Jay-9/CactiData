import time
import os
import datetime
import requests
import pandas
from matplotlib import pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')


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
    return datetime.datetime.now().strftime('%Y-%m-%d') + '.csv'


def data_calculation(the_sor_file):
    the_all_data = pandas.read_csv(the_sor_file, skiprows=9, usecols=[0, 8, 9, 10, 34])
    the_num_data = pandas.read_csv('/wjq/Number_of_users/Number_of_users.csv')
    os.remove(the_sor_file)
    max_time = the_all_data.iloc[the_all_data.iloc[:, 4].idxmax(), 0]
    ck_flow = round(the_all_data.iloc[the_all_data.iloc[:, 4].idxmax(), 1]/1000/1000/1000, 2)
    hl_flow = round(the_all_data.iloc[the_all_data.iloc[:, 4].idxmax(), 2]/1000/1000/1000, 2)
    idc_flow = round(the_all_data.iloc[the_all_data.iloc[:, 4].idxmax(), 3]/1000/1000/1000, 2)
    total_flow = round(the_all_data.iloc[:, 4].max()/1000/1000/1000, 2)
    # print(max_time, ck_flow, hl_flow, idc_flow, total_flow)
    ck_per = round(ck_flow/total_flow*100, 2)
    hl_per = round(hl_flow/total_flow*100, 2)
    idc_per = round(idc_flow/total_flow*100, 2)
    nwl_per = round(hl_per + idc_per, 2)
    # print(ck_per, hl_per, idc_per, nwl_per)
    ben_user = round(the_num_data.iloc[-1, 1], 2)
    all_user = round(the_num_data.iloc[-1, 2], 2)
    average_bandwidth = round(total_flow/ben_user*100, 2)
    # print(all_user, ben_user, average_bandwidth)
    return [max_time, ck_flow, hl_flow, idc_flow, total_flow, ck_per, hl_per, idc_per, nwl_per,
            all_user, ben_user, average_bandwidth]


def log_csv(the_one_data_log):
    columns = ['max_time', 'ck_flow', 'hl_flow', 'idc_flow', 'total_flow', 'ck_per', 'hl_per', 'idc_per',
               'nwl_per', 'all_user', 'ben_user', 'average_bandwidth']
    the_all_data_log = pandas.DataFrame()
    the_all_data_log.at[0, 'max_time'] = the_one_data_log[0]
    the_all_data_log.at[0, 'ck_flow'] = the_one_data_log[1]
    the_all_data_log.at[0, 'hl_flow'] = the_one_data_log[2]
    the_all_data_log.at[0, 'idc_flow'] = the_one_data_log[3]
    the_all_data_log.at[0, 'total_flow'] = the_one_data_log[4]
    the_all_data_log.at[0, 'ck_per'] = the_one_data_log[5]
    the_all_data_log.at[0, 'hl_per'] = the_one_data_log[6]
    the_all_data_log.at[0, 'idc_per'] = the_one_data_log[7]
    the_all_data_log.at[0, 'nwl_per'] = the_one_data_log[8]
    the_all_data_log.at[0, 'all_user'] = the_one_data_log[9]
    the_all_data_log.at[0, 'ben_user'] = the_one_data_log[10]
    the_all_data_log.at[0, 'average_bandwidth'] = the_one_data_log[11]
    the_all_data_log.to_csv('all_data_log.csv', mode='a', header=False, index=False, columns=columns)


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
    ben_user = []
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
        ben_user.append(the_all_data_log.at[i, 'ben_user'])
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
    for xx, yy, zz, aa in zip(x_lab, ben_user, all_user, average_bandwidth):
        ax1.text(xx, max(ck_flow+hl_flow)+260, '总用户数\n' + str(zz) + '\n' + '本网用户\n' + str(yy) + '\n\n\n' +
                 '户均带宽\n' + str(aa) + '\nKbps/户', ha='center', fontproperties=font_num)
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


if __name__ == '__main__':
    sor_file = get_sor_data()
    one_data_log = data_calculation(sor_file)
    log_csv(one_data_log)
    drawing()
    mix_pic()
