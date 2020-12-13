# -*- coding: utf-8 -*-
# @Author  : LuoXian
# @Date    : 2020/2/13 15:44
# Software : PyCharm
# version： Python 3.8
# @File    : qq_mail.py
# 简单邮件传输协议
import smtplib
import requests
import email
import time
import json
import sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


city = sys.argv[1]
user = sys.argv[2]
pwd = sys.argv[3]
url = f'https://free-api.heweather.net/s6/weather/forecast?location={city}&key=30e62ce83dcd466aa8da1e2450fdf250'


# 请求天气api
def get_weather():
    res = requests.get(url)
    res.encoding = 'utf-8'
    res = json.loads(res.text)
    result = res['HeWeather6'][0]['daily_forecast']
    location = res['HeWeather6'][0]['basic']
    city = location['parent_city'] + location['admin_area']
    names = ['城市', '时间', '天气状况', '最高温', '最低温', '日出', '日落']
    for data in result:
        date = data['date']
        cond = data['cond_txt_d']
        max = data['tmp_max']
        min = data['tmp_min']
        sr = data['sr']
        ss = data['ss']
        weather = [city, date, cond, max, min, sr, ss]
        today = ''
        for i in zip(names, weather):
            today += f'{i[0]:^9}{i[1]:^18}\n'
        yield today


msg = get_weather()
msg = '\t\t\t\t<这是今日份的天气>\n' + next(msg) + '=' * 40 + '\n\t\t\t\t<还有明日份的天气>\n' + next(msg) + '=' * 40
#print(msg)

# 设置邮箱的域名
HOST = 'smtp.qq.com'
# 设置邮件标题
SUBJECT = '今日份天气预报到了哟，主子'
# 设置发件人邮箱
FROM = user
# 设置收件人邮箱
TO = user  # 可以填写多个邮箱，用逗号分隔，后面会用split做逗号分割, xxx@163.com,
message = MIMEMultipart('related')
# --------------------------------------发送文本-----------------
# 发送邮件正文到对方的邮箱中
message_html = MIMEText(f"主子你的邮件到了~~\n\n{msg}", 'plain', 'utf-8')  # \n为换行
message.attach(message_html)

# -------------------------------------添加文件---------------------
# 要确定当前目录有test.csv这个文件
# message_xlsx = MIMEText(open('test.json', 'rb').read(), 'base64', 'utf-8')
# 设置文件在附件当中的名字
# message_xlsx['Content-Disposition'] = 'attachment;filename="test01.csv"'
# message.attach(message_xlsx)

# 设置邮件发件人
message['From'] = FROM
# 设置邮件收件人
message['To'] = TO
# 设置邮件标题
message['Subject'] = SUBJECT

# 获取简单邮件传输协议的证书
email_client = smtplib.SMTP_SSL(HOST)
# 设置发件人邮箱的域名和端口，端口为465
email_client.connect(HOST, '465')
# ---------------------------邮箱授权码------------------------------
result = email_client.login(FROM, pwd)
#print('登录结果', result)
email_client.sendmail(from_addr=FROM, to_addrs=TO.split(','), msg=message.as_string())
# 关闭邮件发送客户端
email_client.close()
