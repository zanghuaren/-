import gxk_data
import time
import os
import pandas as pd
import json
import requests
from tabulate import tabulate


with open("Cookie.json", "r", encoding="utf-8") as file:
    cookies = json.load(file)  # 将 JSON 数据加载为 Python 字典

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'http://jwgl.jiaowu.dlufl.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/comeInBxxk',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {
    'sEcho': '1',
    'iColumns': '9',
    'sColumns': '',
    'iDisplayStart': '0',
    'iDisplayLength': '5000',
    'mDataProp_0': 'kch',
    'mDataProp_1': 'kcmc',
    'mDataProp_2': 'xf',
    'mDataProp_3': 'skls',
    'mDataProp_4': 'sksj',
    'mDataProp_5': 'skdd',
    'mDataProp_6': 'xqmc',
    'mDataProp_7': 'ctsm',
    'mDataProp_8': 'czOper',
}


def Add_Id(id):
    # 文件路径
    file_path = "ID.txt"

    # 读取当前文件中的 ID
    try:
        with open(file_path, "r") as f:
            choose_list = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        choose_list = []

    # 检查 ID 长度是否为 16
    if len(id) == 16:
        if id[0] == '+':
            # 以 '+' 开头，添加到列表（去重）
            id_to_add = id[1:]
            if id_to_add not in choose_list:
                choose_list.append(id_to_add)
                print("添加成功！当前ID池：")
            else:
                print("ID 已经存在，无法重复添加！")

        elif id[0] == '-':
            # 以 '-' 开头，移除列表中的 ID
            id_to_remove = id[1:]
            if id_to_remove in choose_list:
                choose_list.remove(id_to_remove)
                print("移除成功！当前ID池：")
            else:
                print("ID 不在列表中，无法移除！")

        else:
            print("ID 格式错误：必须以 '+' 或 '-' 开头！")
    else:
        print("ID 无效：长度必须为 16 位！")

    # 更新文件中的 ID 列表（去重）
    with open(file_path, "w") as f:
        for id in set(choose_list):  # 使用 set 去重
            f.write(id + "\n")

    # 打印当前 ID 池
    print("当前 ID 池：")
    for i in set(choose_list):  # 使用 set 去重
        print(i)
# 添加ID到选课池


def Pre_Load():
    params = {
        'jx0502zbid': '57CC78AC27EE439C98DE2A3121D0AE3D',
    }
    response = requests.get(
        'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxk/xsxk_index',
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    response.close()
# 预加载函数，即使cookie正确，也必须先访问这个url才能开始选课。


def Print_Course(courses):
    i = 0
    for course in courses:
        class_name = course.get('class_name', '未知课程')
        class_id = course.get('class_id', '未知ID')
        class_time = course.get('class_time', '未知课程')
        class_teacher = course.get('class_teacher', '未知课程')
        i += 1
        # print(
        #     f"{i}，{class_teacher.ljust(3, '　')} {class_name}\nid:{class_id}\n时间:{class_time}\n")

    return i
# 打印列表函数调试时使用，主要功能已废弃


def Ls_Course(url):
    response = requests.post(
        url,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    content = json.loads(response.text)['aaData']
    courses = []

    for each_class in content:
        # print(each_class)
        if each_class['skls']:
            class_name = each_class['kcmc']
            class_id = each_class['jx0404id']
            class_time = each_class['sksj'].replace('<br>', '')
            class_teacher = each_class['skls']
            # 添加到课程列表
            courses.append({'class_name': class_name, 'class_id': class_id,
                           'class_time': class_time, 'class_teacher': class_teacher})

    return courses
# 课程列表，适用于选修和必修


def Find_Course(file, *keywords):
    """
    根据用户输入的关键字筛选 CSV 文件中的数据。

    :param file: str, CSV 文件路径
    :param keywords: str，可变参数，用户输入的关键字
    :return: str, 筛选后的数据或"无"
    """
    # 加载 CSV 文件
    df = pd.read_csv(file)

    # 合并所有列为字符串进行模糊匹配
    df["combined"] = df.apply(lambda row: " ".join(map(str, row)), axis=1)

    # 对每个关键字进行筛选
    for keyword in keywords:
        df = df[df["combined"].str.contains(keyword, na=False, case=False)]

    # 删除辅助列
    df = df.drop(columns=["combined"])

    # 检测是否有结果
    if df.empty:
        return "无"

    # 使用 tabulate 格式化输出
    return tabulate(df, headers="keys", tablefmt="simple", showindex=False)
# 查找公选课


def BX_Course(url1, url2):
    course_list = Ls_Course(url1)
    # Print_Course(course_list)
    len = Print_Course(course_list)
    print(f"当前课程共有{len}节课可选————")
    for i in range(0, len):
        class_teacher = course_list[i]['class_teacher']
        class_name = course_list[i]['class_name']
        class_id = course_list[i]['class_id']
        class_time = course_list[i]['class_time']

        print(
            f'\n{class_teacher.ljust(4, '　')}{class_name}\n{class_id}\n{class_time}')
        params = {
            'jx0404id': class_id,
        }
        resp = response = requests.get(
            url2,
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
        )
        resp.close()
        if resp.json()['success']:
            print('选课成功！')
        else:
            print(resp.json()['message'])
        print('----------------------------------')
# 必修程选择


def XX_Course(url1, url2):
    course_list = Ls_Course(url1)
    len_courses = len(course_list)  # 获取课程数量
    Print_Course(course_list)
    print(f"当前课程共有{len_courses}节课可选————")

    # 创建一个字典，映射序号到课程信息
    course_dict = {}

    # 打印课程列表并填充字典
    for i in range(len_courses):
        class_teacher = course_list[i]['class_teacher']
        class_name = course_list[i]['class_name']
        class_id = course_list[i]['class_id']
        class_time = course_list[i]['class_time']
        print(
            f'\n{i + 1}. {class_teacher.ljust(4, "　")}{class_name}\n{class_id}\n{class_time}')
        course_dict[i + 1] = class_id  # 序号从 1 开始

    # 获取用户输入的序号，逗号分隔
    selected_indexes = input("\n请输入课程序号，用英文逗号分隔：").split(",")

    # 遍历用户输入的序号
    for index in selected_indexes:
        index = int(index.strip())  # 转换为整数
        if index in course_dict:
            class_id = course_dict[index]  # 获取课程ID
            params = {
                'jx0404id': class_id,
            }
            # 请求选课
            resp = requests.get(
                url2,
                params=params,
                cookies=cookies,
                headers=headers,
                verify=False,
            )
            resp.close()
            if resp.json()['success']:
                print(f'选课成功！课程ID: {class_id}')
            else:
                print(f"选课失败！{resp.json()['message']}")
        else:
            print(f"无效的序号：{index}")
# 选修课选课


def Public_Course(url, id):
    params = {
        'jx0404id': id,
        'xkzy': '',
        'trjf': '',
    }
    resp = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    resp.close()
    if resp.json()['success']:
        print('选课成功！')
        return True
    else:
        print(resp.json()['message'])
        return False
    print('----------------------------------')
# 公选课选择


def Cancel_Course(url, id):
    params = {
        'jx0404id': id,
    }

    resp = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    resp.close()
    if resp.json()['success']:
        print('退课成功！')
        return True
    else:
        # print(resp.json()['message'])
        # 如果没选上面会打印非本学期课程表不能退选，实际上是没有选择。
        print('该课程还未选择！')
        return False
    print('----------------------------------')


def main():
    Pre_Load()

    # 分别为：必修选课请求网页，选修选课请求网页，选择公选课操作的请求地址。选择选修和必修操作的请求地址。退课请求地址。
    url1 = 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/xsxkBxxk'
    url2 = 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/xsxkXxxk'
    url3 = 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/ggxxkxkOper'
    url4 = 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkkc/bxxkOper'
    url5 = 'http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxkjg/xstkOper'
    while (True):
        print("=============================")
        print(" 输入1进入必修选课")
        print(" 输入2进入选修选课")
        print(" 输入3进入循环选课模式")
        print(" 输入4查找或选择公共选修课")
        print(" 输入5加载选修课数据")
        print(" 输入6进入退课模式")
        print("=============================")
        i = input("Please Enter:")
        if int(i) == 0:
            break
        try:
            if int(i) == 1:
                os.system('cls')
                BX_Course(url1, url4)
                print("所有必修课选择成功！")
                os.system('pause')
                os.system('cls')
            else:
                os.system('cls')
            if int(i) == 2:
                os.system('cls')
                XX_Course(url2, url4)
                os.system('pause')
                os.system('cls')
            else:
                os.system('cls')
            if int(i) == 3:
                while (True):
                    os.system('cls')
                    print("本模式适用于指定课程已没有名额，但有人退课的情况下可以及时选到，选课池内容永久保存。")
                    print("=============================")
                    print("输入0退出")
                    print("输入1设置选课池")
                    print("输入2在选课池中开始选课")
                    print("=============================")
                    words = input("请输入：")
                    if words == '0':
                        break
                    if words == '1':
                        print("说明：如输入+ID标明添加，-ID表明移除：")
                        print("输入0退出")
                        while (True):
                            # 获取用户输入的 ID
                            id = input("Please Enter Course ID:")
                            if id == '0':
                                break
                            Add_Id(id)
                    if words == '2':
                        sum = 0
                        while (True):
                            with open("ID.txt", "r") as f:
                                ids = [line.strip()
                                       for line in f.readlines()]
                            sum += 1
                            print(f"\n第{sum}次尝试：")
                            for id in ids:
                                print(id)
                                if Public_Course(url3, id):
                                    break
                            time.sleep(1.5)
            else:
                os.system('cls')
            if int(i) == 4:
                os.system('cls')
                print("输入课程名称则搜索，输入课程ID则选课，输入0退出。")
                print("说明：例如最后一列3/30表示课程容量30人，已选3人。搜索支持星期几、老师、课程类型等。")
                while (True):
                    words = input("\n请输入：").replace('，', ',')
                    if words == '0':
                        break
                    elif len(words) == 15:
                        os.system('cls')
                        Public_Course(url3, words)
                        os.system('pause')
                    else:
                        words = words.split(",")
                        results = Find_Course("data.csv", *words)
                        print(results)
            else:
                os.system('cls')
            if int(i) == 5:
                gxk_data.get_data()
                os.system('cls')
                print("提取完成！")
            else:
                os.system('cls')
            if int(i) == 6:
                words = input("请输入退课ID：")
                Cancel_Course(url5, words)
                os.system('pause')
                os.system('cls')
            else:
                os.system('cls')
        except:
            os.system('cls')
            # cookie有效期内的第一次使用必须访问下面的地址。
            # Pre_Load()


if __name__ == '__main__':
    main()
