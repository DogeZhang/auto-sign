import smtplib
from email.mime.text import MIMEText
from typing import IO
import yaml
#设置服务器所需信息
#163邮箱服务器地址
# mail_host = 'smtp.yeah.net'  
# #163用户名
# mail_user = 'asdfaser'  
# #密码(部分邮箱为授权码) 
# mail_pass = 'GVARYHTKBKNNBMFB'   
# #邮件发送方邮箱地址
# sender = 'asdfaser@yeah.net'  
 

#设置email信息


def sendEmail(msg, receiver):
    email = {}
    try:
        with open('config/config_sign.yml', 'r', encoding='utf-8') as f:
            file_data = f.read()
            config = yaml.load(file_data, Loader=yaml.FullLoader)
            config = dict(config)
            email = config['email']
    except IOError:
        print('IO 出错，无法读取配置文件。' + '\n')
        print(IOError)
    print(email)
    sender = email['sender']
    mail_host = email['mail_host']
    mail_user = email['mail_user']
    mail_pass = email['mail_pass']
    #邮件内容设置
    message = MIMEText('content','plain','utf-8')
    #邮件主题       
    message['Subject'] = msg 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    receivers = receiver 
    message['To'] = receiver  
    try:
        # smtpObj = smtplib.SMTP() 
        # #连接到服务器
        # smtpObj.connect(mail_host,25)
        smtpObj = smtplib.SMTP_SSL(mail_host)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        # print('success')
        return 0
    except smtplib.SMTPException as e:
        # print('error',e) #打印错误
        return e

# test
# msg = 'testEamil'
# email = '$$@qq.com'
# sendEmail(msg, email)
