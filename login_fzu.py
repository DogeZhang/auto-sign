import requests
import execjs
import re
import random
from bs4 import BeautifulSoup



def login():
    headers = {
        'Host': 'id.fzu.edu.cn',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; VOG-AL00 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': "application/x-www-form-urlencoded",
        'Referer': 'http://id.fzu.edu.cn/authserver/login?service=http%3A%2F%2Fid.fzu.edu.cn%2Fauthserver%2Fmobile%2Fcallback%3FappId%3D673223559&login_type=mobileLogin'
    }
    session = requests.Session()
    with open('encrypt.js', 'r') as f:
        content = f.read()
        encrypt = execjs.compile(content)
    pwdDefaultEncryptSalt = ''
    username = ''
    password = ''
    url = 'http://id.fzu.edu.cn/authserver/login?service=http%3A%2F%2Fid.fzu.edu.cn%2Fauthserver%2Fmobile%2Fcallback%3FappId%3D673223559&login_type=mobileLogin'
    r = session.get(url=url, headers=headers, allow_redirects=False)
    soup = BeautifulSoup(r.content, 'html5lib')
    lt = soup.find('input', attrs={'name': 'lt'})['value']
    execution = soup.find('input', attrs={'name': 'execution'})['value']
    pwdDefaultEncryptSalt = re.search(r'pwdDefaultEncryptSalt = "(.*)"', r.text).group(1)
    math = str(random.random()).replace('.', '')
    hasCode = session.get("http://id.fzu.edu.cn/authserver/needCaptcha.html?username={0}&pwdEncrypt2=pwdEncryptSalt&v={1}".format(username, math), headers=headers)
    print(hasCode.text)
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
    print(requests.utils.dict_from_cookiejar(session.cookies))
    r = session.get(url=r.headers['Location'], headers=headers, allow_redirects=False)
    

if __name__ == "__main__":
    login()