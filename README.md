# 大外选课脚本

基于python的选课程序。

# 介绍

之前在GitHub搜索大外的选课脚本没有找到，于是决定让大外出现在GitHub上。

# 主要功能

- 必修选课，默认全选。
- 选修选课，列出当前课程，输入序号选择。
- 公选课查找，查找符合条件的公选课，支持输入多个关键词。
- 公选课选课，在查找页面直接输入课程ID就可以选择。
- 循环选课，提前把想选的课程添加到选课池，运行后会不断尝试选课，直到有一门课程被选中为止。适用于体育课。



# 使用说明

选课前登陆学校的[教学一体化平台](http://jwgl.jiaowu.dlufl.edu.cn/jxjsxsd/xsxk/xklc_list),浏览器抓包获得自己的cookie。也可以右键复制curl然后到[这个](https://curlconverter.com/)网站转换后一键复制。然后把复制的cookie保存到cookie.json。注意复制的是单引号要改为双引号。

json样例：

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

# 其他说明

ID池是在操作当前文件夹下生成的ID.txt，你也可以手动编辑该文件。

# 待完善功能
输入账号密码，模拟登陆获取cookie。暂时缺乏相关能力，找不到请求的url和加密方式。

# 声明
本仓库发布的脚本及其中涉及的任何功能，仅用于测试和学习研究爬虫相关技术，禁止用于违法用途。