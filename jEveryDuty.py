from openpyxl import load_workbook
import os
import paramiko


def get_date():
    ssh = paramiko.SSHClient()
    know_host = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(know_host)
    ssh.connect(hostname='10.2.205.6', port=22, username='root', password='123')
    stdin, stdout, stderr = ssh.exec_command('tail -1 /jay/all_data_log.csv')
    the_get_info = stdout.readlines()[0].split(',')
    ssh.close()
    return the_get_info


def update_excel(the_excel, the_data):
    workbook = load_workbook(filename=the_excel)
    sheet = workbook.active
    cell_max_time = sheet['A1']
    cell_max_time.value = the_data[0][:4] + '年\n' + the_data[0][5:7] + '月\n' + the_data[0][8:10] + '日'
    cell_ck_flow = sheet['C3']
    cell_ck_flow.value = the_data[1] + ' Gbps'
    cell_hl_flow = sheet['C4']
    cell_hl_flow.value = the_data[2] + ' Gbps'
    cell_idc_flow = sheet['C5']
    cell_idc_flow.value = the_data[3] + ' Gbps'
    cell_total_flow = sheet['C6']
    cell_total_flow.value = the_data[4] + ' Gbps'
    cell_average_bandwidth = sheet['C7']
    cell_average_bandwidth.value = the_data[10] + ' kbps'
    cell_ck_per = sheet['D3']
    cell_ck_per.value = the_data[5] + ' %'
    cell_hl_per = sheet['D4']
    cell_hl_per.value = the_data[6] + ' %'
    cell_idc_per = sheet['D5']
    cell_idc_per.value = the_data[7] + ' %'
    cell_nwl_per = sheet['E7']
    cell_nwl_per.value = the_data[8] + ' %'
    cell_all_user = sheet['E6']
    cell_all_user.value = the_data[9] + ' 万'
    workbook.save(filename=the_excel[:-15] + the_data[0][:10].replace('/', '-') + '.xlsx')


if __name__ == '__main__':
    sor_all_file = os.listdir(os.getcwd())
    for sor_file in sor_all_file:
        if '每日监控' in sor_file:
            get_info = get_date()
            update_excel(sor_file, get_info)
