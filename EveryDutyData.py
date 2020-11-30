import pandas # 从‘每日监控互联网宽带业务流量流向数据分析表2020-11-02’中提取用户数

the_data = []
ck_flow = []
hl_flow = []
idc_flow = []
user_bw = []
user_all = []
user_pbs = []
final_data = pandas.DataFrame()
total_flow = []
ck_per = []
hl_per = []
idc_per = []
nwl_per = []
average_bandwidth = []
sor_file = pandas.read_excel('每日监控互联网宽带业务流量流向数据分析表2020-11-02.xlsx', skiprows=36, header=None)

for i in range(0, sor_file.shape[0], 12):
    the_data.append(sor_file.iat[i, 0].replace('\n', ''))
    ck_flow.append(sor_file.iat[i+2, 2])
    hl_flow.append(sor_file.iat[i+3, 2])
    idc_flow.append(sor_file.iat[i+4, 2])
    user_bw.append(sor_file.iat[i+6, 2])
    user_all.append(sor_file.iat[i+7, 2])

for j in range(len(the_data)):
    total_flow.append(ck_flow[j] + hl_flow[j] + idc_flow[j])
    ck_per.append(round(ck_flow[j]/total_flow[j]*100, 2))
    hl_per.append(round(hl_flow[j]/total_flow[j]*100, 2))
    idc_per.append(round(idc_flow[j]/total_flow[j]*100, 2))
    nwl_per.append(round(hl_per[j]+idc_per[j], 2))
    average_bandwidth.append(round(total_flow[j]/user_bw[j]*100, 2))
    user_pbs.append(round(user_all[j]-user_bw[j], 2))


the_data.reverse()
ck_flow.reverse()
hl_flow.reverse()
idc_flow.reverse()
user_bw.reverse()
user_all.reverse()
user_pbs.reverse()
total_flow.reverse()
ck_per.reverse()
hl_per.reverse()
idc_per.reverse()
nwl_per.reverse()
average_bandwidth.reverse()

final_data['the_data'] = the_data
final_data['ck_flow'] = ck_flow
final_data['hl_flow'] = hl_flow
final_data['idc_flow'] = idc_flow
final_data['total_flow'] = total_flow
final_data['ck_per'] = ck_per
final_data['hl_per'] = hl_per
final_data['idc_per'] = idc_per
final_data['nwl_per'] = nwl_per
final_data['average_bandwidth'] = average_bandwidth
final_data['user_bw'] = user_bw
final_data['user_pbs'] = user_pbs
final_data['user_all'] = user_all

final_data.to_excel('final_data.xlsx', index=None,
                    columns=['the_data', 'ck_flow', 'hl_flow', 'idc_flow','total_flow', 'ck_per', 'hl_per', 'idc_per',
                             'nwl_per', 'average_bandwidth', 'user_bw', 'user_pbs', 'user_all'])
