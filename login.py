# -*- coding: utf-8 -*-
import sys, os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import json
import uuid
import base64
from pyDes import des, CBC, PAD_PKCS5
from datetime import datetime, timedelta, timezone
import yaml
import time
import execjs
import re
import random
import sendEmail



# 获取当前utc时间，并格式化为北京时间
def getTimeStr():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")


# 输出调试信息，并及时刷新缓冲区
def log(content):
    print(getTimeStr() + ' ' + str(content))
    sys.stdout.flush()


# 获取今日校园api
def getCpdailyApis(user, debug=False):
    apis = {}
    schools = requests.get(url='https://www.cpdaily.com/v6/config/guest/tenant/list', verify=not debug).json()['data']
    flag = True
    for one in schools:
        if one['name'] == user['school']:
            if one['joinType'] == 'NONE':
                log(user['school'] + ' 未加入今日校园')
                exit(-1)
            flag = False
            params = {
                'ids': one['id']
            }
            apis['tenantId'] = one['id']
            res = requests.get(url='https://www.cpdaily.com/v6/config/guest/tenant/info', params=params,
                               verify=not debug)
            data = res.json()['data'][0]
            joinType = data['joinType']
            idsUrl = data['idsUrl']
            ampUrl = data['ampUrl']
            ampUrl2 = data['ampUrl2']
            if 'campusphere' in ampUrl or 'cpdaily' in ampUrl:
                parse = urlparse(ampUrl)
                host = parse.netloc
                apis[
                    'login-url'] = idsUrl + '/login?service=' + parse.scheme + r"%3A%2F%2F" + host + r'%2Fportal%2Flogin'
                apis['host'] = host
            if 'campusphere' in ampUrl2 or 'cpdaily' in ampUrl2:
                parse = urlparse(ampUrl2)
                host = parse.netloc
                apis[
                    'login-url'] = idsUrl + '/login?service=' + parse.scheme + r"%3A%2F%2F" + host + r'%2Fportal%2Flogin'
                apis['host'] = host
            if joinType == 'NOTCLOUD':
                res = requests.get(url=apis['login-url'], verify=not debug)
                if urlparse(apis['login-url']).netloc != urlparse(res.url):
                    apis['login-url'] = res.url
            break
    if user['school'] == '云南财经大学':
        apis[
            'login-url'] = 'http://idas.ynufe.edu.cn/authserver/login?service=https%3A%2F%2Fynufe.cpdaily.com%2Fportal%2Flogin'
    if flag:
        log(user['school'] + ' 未找到该院校信息，请检查是否是学校全称错误')
        exit(-1)
    log(apis)
    return apis


# 读取yml配置
def getYmlConfig(yaml_file='config/config_sign.yml'):
    yaml_file = os.path.join(sys.path[0], 'config', 'config_sign.yml')
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)


# DES加密
def DESEncrypt(s, key='XCE927=='):
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(s)
    return base64.b64encode(encrypt_str).decode()


# DES解密
def DESDecrypt(s, key='XCE927=='):
    s = base64.b64decode(s)
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    return k.decrypt(s)


# 全局配置
config = getYmlConfig()
session = requests.session()
user = config['user']
email_yml = config['email']
# Cpdaily-Extension
extension = {
    "lon": user['lon'],
    "model": "PCRT00",
    "appVersion": "8.0.8",
    "systemVersion": "4.4.4",
    "userId": user['username'],
    "systemName": "android",
    "lat": user['lat'],
    "deviceId": str(uuid.uuid1())
}
CpdailyInfo = DESEncrypt(json.dumps(extension))
apis = getCpdailyApis(user)
host = apis['host']


# 获取验证码
def getMessageCode():
    log('正在获取验证码。。。')
    headers = {
        'SessionToken': 'szFn6zAbjjU=',
        'clientType': 'cpdaily_student',
        'tenantId': apis['tenantId'],
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    params = {
        'mobile': DESEncrypt(str(user['tellphone']))
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/mobile/messageCode'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('获取验证码成功。。。')


# 手机号登陆
def mobileLogin(code):
    log('正在验证验证码。。。')
    headers = {
        'SessionToken': 'szFn6zAbjjU=',
        'clientType': 'cpdaily_student',
        'tenantId': apis['tenantId'],
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    params = {
        'loginToken': str(code),
        'loginId': str(user['tellphone'])
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/mobileLogin'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('验证码验证成功。。。')
    return res.json()['data']


# 验证登陆信息
def validation(data):
    log('正在验证登陆信息。。。')
    sessionToken = data['sessionToken']
    tgc = data['tgc']
    headers = {
        'SessionToken': DESEncrypt(sessionToken),
        'clientType': 'cpdaily_student',
        'tenantId': apis['tenantId'],
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'sessionToken=' + sessionToken
    }
    params = {
        'tgc': DESEncrypt(tgc)
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/validation'
    res = session.post(url=url, headers=headers, data=json.dumps(params))
    errMsg = res.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('验证登陆信息成功。。。')
    return res.json()['data']


# 更新acw_tc
def updateACwTc(data):
    log('正在更新acw_tc。。。')
    sessionToken = data['sessionToken']
    tgc = data['tgc']
    amp = {
        'AMP1': [{
            'value': sessionToken,
            'name': 'sessionToken'
        }],
        'AMP2': [{
            'value': sessionToken,
            'name': 'sessionToken'
        }]
    }
    headers = {
        'TGC': DESEncrypt(tgc),
        'AmpCookies': DESEncrypt(json.dumps(amp)),
        'SessionToken': DESEncrypt(sessionToken),
        'clientType': 'cpdaily_student',
        'tenantId': apis['tenantId'],
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Host': host,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    url = 'https://{host}/wec-portal-mobile/client/userStoreAppList'.format(host=host)
    # 清除cookies
    # session.cookies.clear()
    session.get(url=url, headers=headers, allow_redirects=False)
    log('更新acw_tc成功。。。')


# 获取MOD_AUTH_CAS
def getModAuthCas(data):
    log('正在获取MOD_AUTH_CAS。。。')
    sessionToken = data['sessionToken']
    headers = {
        'Host': host,
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 cpdaily/8.0.8 wisedu/8.0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'X-Requested-With': 'com.wisedu.cpdaily'
    }
    url = 'https://{host}/wec-counselor-sign-apps/stu/mobile/index.html?timestamp='.format(host=host) + str(
        int(round(time.time() * 1000)))
    res = session.get(url=url, headers=headers, allow_redirects=False)
    location = res.headers['location']
    # print(location)
    headers2 = {
        'Host': 'www.cpdaily.com',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 cpdaily/8.0.8 wisedu/8.0.8',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8',
        'Cookie': 'clientType=cpdaily_student; tenantId=' + apis['tenantId'] + '; sessionToken=' + sessionToken,
    }
    res = session.get(url=location, headers=headers2, allow_redirects=False)
    if hasattr(res.headers, 'location'): 
        print('验证成功。')
    else:
        print("验证失败，请重新登陆。")
        sendMessage('验证失败，请重新登陆！！', user['email'])
    location = res.headers['location']
    # print(location)
    session.get(url=location, headers=headers)
    cookies = requests.utils.dict_from_cookiejar(session.cookies)
    if 'MOD_AUTH_CAS' not in cookies:
        log('获取MOD_AUTH_CAS失败。。。')
        exit(-1)
    log('获取MOD_AUTH_CAS成功。。。')

# 福州大学登陆
def login_fzu():
    headers = {
        'Host': 'id.fzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; VOG-AL00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': 'http://id.fzu.edu.cn/authserver/login?service=http%3A%2F%2Fid.fzu.edu.cn%2Fauthserver%2Fmobile%2Fcallback%3FappId%3D673223559&login_type=mobileLogin'
    }
    with open('encrypt.js', 'r') as f:
        content = f.read()
        encrypt = execjs.compile(content)
    pwdDefaultEncryptSalt = ''
    username = ''
    password = ''
    session.cookies.set('CASTGC', '')
    url = 'http://id.fzu.edu.cn/authserver/login?service=http%3A%2F%2Fid.fzu.edu.cn%2Fauthserver%2Fmobile%2Fcallback%3FappId%3D673223559&login_type=mobileLogin'
    r = session.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    lt = soup.find('input', attrs={'name': 'lt'})['value']
    execution = soup.find('input', attrs={'name': 'execution'})['value']
    pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(.*)"', r.text).group(1)
    math = str(random.random()).replace('.', '')
    hasCode = session.get("http://id.fzu.edu.cn/authserver/needCaptcha.html?username={0}&pwdEncrypt2=pwdEncryptSalt&v={1}".format(username, math), headers=headers)
    data = {
            'username': "{0}".format(username),
            'dllt': 'userNamePasswordLogin',
            'captchaResponse': '',
            'password': encrypt.call('encryptAES', password, pwdDefaultEncryptSalt),
            'lt': lt,
            'execution': execution,
            "_eventId": "submit",
            'rmShown': "1"
        }
    r = session.post(url=url, headers=headers, data=data, allow_redirects=False)
    r = session.get(url=r.headers['Location'], headers=headers, allow_redirects=False)
    ticket = re.search(r'mobile_token=(.*)"', r.text).group(1)
    ticket = ticket.replace('&#43;', '+')
    ticket = DESEncrypt(ticket)
    data = {
        'tenantId': 'fzu',
        'ticket': str(ticket)
    }
    headers = {
        'SessionToken': 'szFn6zAbjjU=',
        'clientType': 'cpdaily_student',
        'tenantId':  '',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; PCRT00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.8.1',
        'deviceType': '1',
        'CpdailyStandAlone': '0',
        'CpdailyInfo': CpdailyInfo,
        'RetrofitHeader': '8.0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '184',
        'Host': 'www.cpdaily.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
    }
    url = 'https://www.cpdaily.com/v6/auth/authentication/notcloud/login'
    r = session.post(url=url, headers=headers, data=json.dumps(data))
    errMsg = r.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    result = r.json()
    tenantId = result['data']['tenantId']
    deviceExceptionMsg = result['data']['deviceExceptionMsg']
    mobile = result['data']['mobile']
    if deviceExceptionMsg != '':
        url = 'https://www.cpdaily.com/v6/auth/deviceChange/mobile/messageCode'
        data = {
            'mobile': 'Sbda8j60L+IXRBHH7yCaXA=='
        }
        headers['Content-Length'] = ''
        r = session.post(url=url, headers=headers, data=json.dumps(data))
        url = 'https://www.cpdaily.com/v6/auth/deviceChange/validateMessageCode'
        messageCode = input('massageCode')
        data = {
            'messageCode': messageCode,
            'ticket': ticket,
            'mobile': mobile
        }
        r = session.post(url=url, headers=headers, data=json.dumps(data))
    errMsg = r.json()['errMsg']
    if errMsg != None:
        log(errMsg)
        exit(-1)
    log('验证登陆信息成功。。。')
    sendEmail("登陆成功。", user['email'])
    return r.json()['data']

# 发送邮件通知
def sendMessage(msg, email):
    send = email
    isAuthor = email_yml['isAuthor']
    if send != '':
        #使用原作者邮箱服务
        if int(isAuthor) == 1:
            log('正在发送邮件通知。。。')
            res = requests.post(url='http://www.zimo.wiki:8080/mail-sender/sendMail',
                                data={'title': '今日校园自动签到结果通知', 'content': msg, 'to': send})
            code = res.json()['code']
            if code == 0:
                log('发送邮件通知成功。。。')
            else:
                log('发送邮件通知失败。。。')
                log(res.json())
        else: #使用自己邮箱发送结果
            log('正在发送邮件通知。。。')
            code = sendEmail.sendEmail(msg, send)
            if code == 0:
                log('发送邮件通知成功。。。')
            else:
                log('发送邮件通知失败。。。')
                log(code)

# 通过手机号和验证码进行登陆
def login():
    # 1. 获取验证码
    getMessageCode()
    code = input("请输入验证码：")
    # 2. 手机号登陆
    data = mobileLogin(code)
    # data = login_fzu()
    # 3. 验证登陆信息
    data = validation(data)
    # 4. 更新acw_tc
    updateACwTc(data)
    # 5. 获取mod_auth_cas
    getModAuthCas(data)
    print('==============sessionToken==============')
    sessionToken = data['sessionToken']
    print(sessionToken)
    print('==============CpdailyInfo==============')
    print(CpdailyInfo)
    print('==============Cookies-acw_tc==============')
    loginCookies = requests.utils.dict_from_cookiejar(session.cookies)
    print(loginCookies["acw_tc"])
    print('==============Cookies-MOD_AUTH_CAS==============')
    print(loginCookies["MOD_AUTH_CAS"])
    loginSession = {
    "sessionToken": sessionToken,
    "CpdailyInfo": CpdailyInfo,
    "sessionCookies": {
        "acw_tc": loginCookies["acw_tc"],
        "MOD_AUTH_CAS": loginCookies["MOD_AUTH_CAS"]
        }
    }
    with open('config/loginSession.yml', 'w', encoding='utf-8') as f:
        yaml.dump(loginSession, f, sort_keys=False)
    print('登陆信息已保存')
    


if __name__ == '__main__':
    login()
