import yaml
import os

username = ''
tellphone = ''
address = '中国福建省福州市闽侯县源江路'
email = ''
school = '福州大学'
lon = 119.203149
lat = 26.062701
abnormalReason = ''
photo = ''
#是否使用原作者提供的邮箱服务
isAuthor = 1
#邮箱服务器
mail_host = ''  
#163用户名
mail_user = ''  
#密码(部分邮箱为授权码) 
mail_pass = ''   
#邮件发送方邮箱地址
sender = '' 




def generateConfig():
    """
    生成验证信息，填错可ctrl+c并重新运行
    """

    print('+++++++++生成用户配置文件、几点说明：+++++++++')
    print('｜1. 请按输入示例输入，否则“登陆”可能不成功。')
    print('｜2. 本程序不检查输入，如出错请仔细查看example下的示例文件。')
    print('｜3. 如果填写错误，请运行ctrl+c 并"python3 generate_config.py" 重新填写一次。')
    print('｜4. 由于福大登入限制，手机登陆后，此处掉线，需运行 "python3 login.py" 重新登陆。\n')

    print('请输入学号：')
    print('+++｜例：190******｜+++')
    username = input('学号：')
    if username == '':
        print('输入为空，签到程序可能报错\n')
    else:
        print('username: ' + username + '\n')
    
    print('请输入手机号：')
    print('+++｜例：131*******8｜+++')
    tellphone = input('手机号：')
    if tellphone == '':
        print('|输入为空，签到程序可能报错' + '\n')
    else:
        print('|tellphone: ' + tellphone + '\n')

    print('请输入登陆账号：（无需账号登陆可不填）')
    print('+++｜例：N1903XXXXXS｜+++')
    username_account = input('登陆账号')
    if username_account == '':
        print('|输入为空' + '\n')
    else:
        print('|username_account: ' + username_account + '\n')
    
    print('请输入密码：（无需账号登陆可不填）')
    print('+++｜例：*******｜+++')
    password = input('密码：')
    if password == '':
        print('|输入为空' + '\n')
    else:
        print('|password: ' + password + '\n')

    print('请输入地址：（留空直接敲回车默认：中国福建省福州市闽侯县源江路）')
    print('+++｜例：中国**省**市**县**路｜或留空直接回车｜+++')
    address = input('地址：')
    if address == '':
        print('|输入为空，默认 中国福建省福州市闽侯县源江路' + '\n')
        address = '中国福建省福州市闽侯县源江路'
    else:
        print('|address: ' + address + '\n')
    
    print('请输入邮箱：')
    print('+++｜例：***@**.**｜+++')
    email = input('邮箱：')
    if email == '':
        print('|输入为空，签到程序可能报错' + '\n')
    else:
        print('|email: ' + email + '\n')
    
    print('请输入学校：（留空直接敲回车默认：福州大学）')
    print('+++｜例：**大学｜+++')
    school = input('学校：')
    if school == '':
        print('|输入为空，默认：福州大学' + '\n')
        school = '福州大学'
    else:
        print('|school: ' + school + '\n')
    
    print('请输入经度：（请访问 https://lbs.amap.com/api/javascript-api/example/map/click-to-get-lnglat/ 获取经纬度）')
    print('+++｜例：119.203149｜+++')
    lon = input('经度：')
    if lon == '':
        print('|输入为空，签到程序可能报错' + '\n')
    else:
        print('|lon: ' + lon + '\n')

    print('请输入纬度：（请访问 https://lbs.amap.com/api/javascript-api/example/map/click-to-get-lnglat/ 获取经纬度）')
    print('+++｜例：26.062701｜+++')
    lat = input('纬度：')
    if lat == '':
        print('|输入为空，签到程序可能报错' + '\n')
    else:
        print('|lat: ' + lat + '\n')

    print('\n')
    print('+++|配置邮箱通知服务|+++')
    print('|1. 如果懒得配置，请输入 1，或者直接回车（别输别的！），使用原作者提供的邮箱服务（注意事项看readme）。')
    print('|2. 如果有 2 个邮箱（是两个！不能和上一个邮箱相同！），可使用自己邮箱发送结果。（需开启SMTP！自己百度！）')
    isAuthor = input('是否使用原作者邮箱服务？（直接回车 或 1:是｜0：否）')
    if isAuthor == '' or isAuthor == 1:
        print('懒得配置，使用原作者提供的邮箱服务。')
        isAuthor = 1
        mail_host = ''  
        mail_user = ''  
        mail_pass = ''   
        sender = '' 
    else:
        print('使用自己的邮箱发送结果。\n')
        print('请输入邮箱服务器：')
        print('+++｜例：smtp.yeah.net｜+++')
        mail_host = input('邮箱服务器：')
        if mail_host == '':
            print('|输入为空，邮箱服务可能无法正常运行' + '\n')
        else:
            print('|mail_host: ' + mail_host + '\n')

        print('请输入邮箱用户名：')
        print('+++｜例：sdfdfesd｜@前面那一段|+++')
        mail_user = input('邮箱用户名：')
        if mail_user == '':
            print('|输入为空，邮箱服务可能无法正常运行' + '\n')
        else:
            print('|mail_host: ' + mail_user + '\n')

        print('请输入密码(部分邮箱为授权码)：')
        print('+++｜例：GVARYOSKBONSBMFB｜开通SMTP可见|+++')
        mail_pass = input('密码：')
        if mail_pass == '':
            print('|输入为空，邮箱服务可能无法正常运行' + '\n')
        else:
            print('|mail_pass: ' + mail_pass + '\n')
        
        print('请输入用于发送结果信息的邮箱：')
        print('+++｜例：sdfdfesd@yeah.net|+++')
        sender = input('邮箱：')
        if sender == '':
            print('|输入为空，邮箱服务可能无法正常运行' + '\n')
        else:
            print('|sender: ' + sender + '\n')

    
    print('输入完毕，正在生成配置文件。')
    config = {
        'user': {
            'username': username,
            'tellphone': tellphone,
            'username_account': username_account,
            'password': password
            'address': address, 
            'email': email, 
            'school': school, 
            'lon': str(lon), 
            'lat': str(lat), 
            'abnormalReason': None,
            'photo:': None
        }, 
        'cpdaily': {
            'defaults': [
                {
                    'default': {
                        'title': '午检体温 (必填)',
                        'value': '小于37.3度'
                    }
                },
                {
                    'default': {
                        'title': '是否有发热、咳嗽、乏力、呼吸困难等疑似症状(必填)',
                        'value': '否'
                    }
                }
            ]
        },
        'email': {
            'isAuthor': isAuthor,
            'mail_host': mail_host,
            'mail_user': mail_user,
            'mail_pass': mail_pass,
            'sender': sender
        }
    }
    try:
        with open('config/config.yml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f, sort_keys=False, allow_unicode = True)
    except IOError:
        print('IO 出错，无法生成配置文件。' + '\n')
        print(IOError)
    else:
        print('生成配置文件成功！' + '\n')
        with open('config/config.yml', 'r', encoding='utf-8') as f:
            file_data = f.read()
            # config_read = yaml.load(file_data, Loader=yaml.FullLoader)
            print(file_data)
        print('\n' + '+++｜已按福大“默认签到表格”生成配置文件，请对照，如有出入在config/config.yml中修改或重新运行改程序｜+++' + '\n')
    
    

def main():
    """
    main function
    """
    generateConfig()
    
if __name__ == '__main__':
    main()
