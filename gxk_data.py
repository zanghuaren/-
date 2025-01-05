import requests
import csv
import os
from wcwidth import wcswidth
import time
import json

# 方便后期输出，ljust对中英文计算不同.
# 结合125-131行可以使得数据打印整齐，但在主文件中还是会乱，已停用。


def ljust_wcwidth(text, width, fillchar=' '):
    current_width = wcswidth(text)
    return text + fillchar * (width - current_width)


def get_data():
    csv_file_path = "data.csv"
    os.system(f"type nul > {csv_file_path}")
    for i in range(0, 31):
        with open("Cookie.json", "r", encoding="utf-8") as file:
            cookies = json.load(file)  # 将 JSON 数据加载为 Python 字典
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'http://jwgl.jiaowu.dlufl.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/comeInGgxxkxk',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = {
            'kcxx': '',
            'skls': '',
            'skxq': '',
            'skjc': '',
            'sfym': 'false',
            'sfct': 'false',
            'szjylb': '',
        }

        data = {
            'sEcho': '2',
            'iColumns': '12',
            'sColumns': '',
            'iDisplayStart': f'{15 * i}',
            'iDisplayLength': '15',
            'mDataProp_0': 'kch',
            'mDataProp_1': 'kcmc',
            'mDataProp_2': 'xf',
            'mDataProp_3': 'skls',
            'mDataProp_4': 'sksj',
            'mDataProp_5': 'skdd',
            'mDataProp_6': 'xqmc',
            'mDataProp_7': 'xkrs',
            'mDataProp_8': 'syrs',
            'mDataProp_9': 'ctsm',
            'mDataProp_10': 'szkcflmc',
            'mDataProp_11': 'czOper',
        }

        response = requests.post(
            'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/xsxkGgxxkxk',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            verify=False,
        )
        response.close()
        # if i == 6:
        #     break
        print("\n正在提取page:", i + 1)
        for each_class in response.json()['aaData']:
            # print(each_class)
            if each_class['kcmc'] == '体育':
                class_name = each_class['fzmc']
                class_id = each_class['jx0404id']
                class_time = each_class['sksj'].replace('<br>', '')
                class_teacher = each_class['skls']
                class_group = each_class['szkcflmc']
                # print(type(each_class['xkrs']), type(each_class['pkrs']))
                class_condition = str(
                    each_class['xkrs']) + '/' + str(each_class['pkrs'])
                if each_class['ctsm']:
                    class_ct = "冲突　"
                else:
                    class_ct = "不冲突"
                class_ct = class_ct
            else:

                class_name = each_class['kcmc'].split("-")[-1]
                class_id = each_class['jx0404id']
                class_time = '时间任选'
                class_teacher = '无　'
                if each_class['szkcflmc']:
                    class_group = each_class['szkcflmc']
                else:

                    class_group = '未知分类'
                # class_condition = '∞'
                class_condition = str(
                    each_class['xkrs']) + '/' + str(each_class['pkrs'])
                if each_class['ctsm']:
                    class_ct = "冲突　"
                else:
                    class_ct = "不冲突"
                if len(class_name.strip("　")) > 8:
                    class_name = (class_name[0:6] + '....')
                # print(each_class)
            # if len(class_teacher) == 2:
            #     class_teacher = class_teacher + '　'
            # class_group = ljust_wcwidth(class_group, 12, ' ')
            # class_name = ljust_wcwidth(class_name, 9, ' ')
            # class_teacher = ljust_wcwidth(class_teacher, 6, ' ')
            # class_id = ljust_wcwidth(class_id, 22, ' ')
            # class_time = ljust_wcwidth(class_time, 42, ' ')
            # class_ct = ljust_wcwidth(class_ct, 10, ' ')
            # class_condition = ljust_wcwidth(class_condition, 10, ' ')

            # print(class_group, class_name, class_teacher,
            # class_id, class_time, class_ct, class_condition)

            csv_file_path = "data.csv"
            # CSV 文件路径（当前文件夹下）
            with open(csv_file_path, mode="a", encoding="utf-8", newline="") as file:
                # 写为csv文件，避免重复获取
                writer = csv.writer(file)
                # 如果是第一次写入文件，添加表头
                if file.tell() == 0:  # 检查文件是否为空
                    writer.writerow(["class_group", "class_teacher", "class_name",
                                    "class_id", "class_time", "class_ct", "class_condition"])

                # 写入数据
                writer.writerow([class_group, class_teacher, class_name,
                                class_id, class_time, class_ct, class_condition])

            # print(f"数据已成功写入 {csv_file_path}")
