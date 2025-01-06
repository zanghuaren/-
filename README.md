## 大外选课脚本

基于python的选课程序。

## 介绍

之前在GitHub搜索大外的选课脚本没有找到，于是决定让大外出现在GitHub上。

## 主要功能

- 必修选课，默认全选。
- 选修选课，列出当前课程，输入序号选择。
- 公选课查找，查找符合条件的公选课，支持输入多个关键词。
- 公选课选课，在查找页面直接输入课程ID就可以选择。
- 循环选课，提前把想选的课程添加到选课池，运行后会不断尝试选课，直到有一门课程被选中为止。适用于体育课。



## 使用说明

选课前登陆学校的[教学一体化平台](http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxk/xklc_list),F12刷新页面浏览器抓包，
![image](https://github.com/user-attachments/assets/c6280001-88d2-4d5f-b736-20048ca23a55)
然后去[https://curlconverter.com/](https://curlconverter.com/)粘贴转换为python用的格式，找到cookie，把cookie后面的大括号内容复制保存到cookie.json。
注意复制的是单引号要改为双引号。
最终json样例：

```
{
    "uid": "123456",
    "JSESSIONID": "654321",
    "SERVERID": "app6",
}
```

安装python环境：

```
scoop install python
```

然后下载引用的库：

```
pip install tabulate requests pandas wcwidth

```

## 其他说明

ID池是在操作当前文件夹下生成的ID.txt，你也可以手动编辑该文件。

## 主要功能运行截图
<img width="1045" alt="Snipaste_2025-01-06_11-11-15" src="https://github.com/user-attachments/assets/002739c7-9695-41ea-826b-ea3b62f61b93" />
<img width="813" alt="Snipaste_2025-01-06_11-09-13" src="https://github.com/user-attachments/assets/4c275587-5781-4ec7-9db5-888f32a8e972" />
<img width="813" alt="Snipaste_2025-01-06_11-10-11" src="https://github.com/user-attachments/assets/be0e85ec-eed8-4e76-bb1f-c3ad47b0d0ce" />
<img width="807" alt="Snipaste_2025-01-06_11-28-51" src="https://github.com/user-attachments/assets/ca668c57-eba5-40f0-afd8-a93d7dec219c" />



## 待完善功能
输入账号密码，模拟登陆获取cookie。暂时缺乏相关能力，找不到请求的url和加密方式。

## 声明
本仓库发布的脚本及其中涉及的任何功能，仅用于测试和学习研究爬虫相关技术，禁止用于违法用途。
