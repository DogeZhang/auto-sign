import yaml
import os, sys

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

    print('+++++++++\033[33m生成用户配置文件、几点说明：\033[0m+++++++++')
    print('｜1. 请按\033[31m输入示例\033[0m输入，否则“登陆”可能不成功。')
    print('｜2. 本程序不检查输入，如出错请仔细查看example下的示例文件。')
    print('｜3. 如果填写错误，请运行ctrl+c 并"python3 generate_config.py" 重新填写一次。')
    print('｜4. \033[31m由于福大登入限制，手机登陆后，此处掉线，需运行 "python3 login.py" 重新登陆。\033[0m\n')

    print('请输入\033[31m学号\033[0m：')
    print('+++｜例：\033[33m190******\033[0m｜+++')
    username = input('\033[31m学号\033[0m：')
    if username == '':
        print('\033[31m输入为空，签到程序可能报错\033[0m\n')
    else:
        print('username: \033[32m' + username + '\033[0m\n')
    
    print('请输入\033[31m手机号\033[0m：')
    print('+++｜例：\033[33m131*******8\033[0m｜+++')
    tellphone = input('\033[31m手机号\033[0m：')
    if tellphone == '':
        print('|\033[31m输入为空，签到程序可能报错\033[0m' + '\n')
    else:
        print('|tellphone: \033[32m' + tellphone + '\033[0m\n')

    print('请输入\033[31m福大统一认证登陆账号\033[0m：（无需账号登陆可不填）')
    print('+++｜例：\033[33mN1903XXXXXS\033[0m｜+++')
    username_account = input('\033[31m登陆账号\033[0m: ')
    if username_account == '':
        print('|\033[31m输入为空\033[0m' + '\n')
    else:
        print('|username_account: \033[32m' + username_account + '\033[0m\n')
    
    print('请输入\033[31m密码\033[0m：（无需账号登陆可不填）')
    print('+++｜例：\033[33m*******\033[0m｜+++')
    password = input('\033[31m密码\033[0m：')
    if password == '':
        print('|\033[31m输入为空\033[0m' + '\n')
    else:
        print('|password: \033[32m' + password + '\033[0m\n')

    print('请输入\033[31m地址\033[0m：（留空直接敲回车\033[0m默认：中国福建省福州市闽侯县源江路\033[0m）')
    print('+++｜例：\033[33m中国**省**市**县**路\033[0m｜或留空\033[33m直接回车\033[0m｜+++')
    address = input('\033[31m地址\033[0m：')
    if address == '':
        print('|\033[31m输入为空\033[0m，默认 \033[33m中国福建省福州市闽侯县源江路\033[0m' + '\n')
        address = '中国福建省福州市闽侯县源江路'
    else:
        print('|address: ' + address + '\n')
    
    print('请输入\033[31m邮箱\033[0m：')
    print('+++｜例：\033[33m***@**.**\033[0m｜+++')
    email = input('\033[31m邮箱\033[0m：')
    if email == '':
        print('|\033[31m输入为空，签到程序可能报错\033[0m' + '\n')
    else:
        print('|email: \033[32m' + email + '\033[0m\n')
    
    print('请输入\033[31m学校\033[0m：（留空直接敲回车默认：\033[33m福州大学\033[0m）')
    print('+++｜例：\033[33m**大学\033[0m｜+++')
    school = input('\033[31m学校\033[0m：')
    if school == '':
        print('|\033[31m输入为空\033[0m，默认：\033[33m福州大学\033[0m' + '\n')
        school = '福州大学'
    else:
        print('|school: \033[32m' + school + '\033[0m\n')
    
    print('请输入\033[31m经度(六位小数)\033[0m：（请访问 https://lbs.amap.com/api/javascript-api/example/map/click-to-get-lnglat/ 获取经纬度）')
    print('+++｜例：\033[33m119.203149\033[0m｜+++')
    lon = input('\033[31m经度\033[0m：')
    if lon == '':
        print('|\033[31m输入为空，签到程序可能报错\033[0m' + '\n')
    else:
        print('|lon: \033[32m' + lon + '\033[0m\n')

    print('请输入\033[31m纬度(六位小数)\033[0m：（请访问 https://lbs.amap.com/api/javascript-api/example/map/click-to-get-lnglat/ 获取经纬度）')
    print('+++｜例：\033[33m26.062701\033[0m｜+++')
    lat = input('\033[31m纬度\033[0m：')
    if lat == '':
        print('|\033[31m输入为空，签到程序可能报错\033[0m' + '\n')
    else:
        print('|lat: \033[32m' + lat + '\033[0m\n')

    print('\n')
    print('+++|\033[31m配置邮箱通知服务\033[0m|+++')
    print('|1. 如果懒得配置，请输入 \033[31m1\033[0m，或者\033[31m直接回车\033[0m（别输别的！），使用原作者提供的邮箱服务（注意事项看readme）。')
    print('|2. 如果有 2 个邮箱（\033[31m是两个！不能和上一个邮箱相同！\033[0m），可使用自己邮箱\033[31m发送结果\033[0m。（需开启SMTP！自己百度！）')
    isAuthor = input('是否使用原作者邮箱服务？（直接回车 或 1:\033[31m是\033[0m｜0：否，\033[33m使用自己的邮箱发送结果通知\033[0m）')
    if isAuthor == '' or isAuthor == 1:
        print('懒得配置，使用原作者提供的邮箱服务。')
        isAuthor = 1
        mail_host = ''  
        mail_user = ''  
        mail_pass = ''   
        sender = '' 
    else:
        print('\033[32m使用自己的邮箱发送结果。\033[0m\n')
        print('请输入\033[31m邮箱服务器：\033[0m')
        print('+++｜例：\033[33msmtp.yeah.net\033[0m｜+++')
        mail_host = input('\033[31m邮箱服务器：\033[0m')
        if mail_host == '':
            print('|\033[31m输入为空，邮箱服务可能无法正常运行\033[0m' + '\n')
        else:
            print('|mail_host: \033[32m' + mail_host + '\033[0m\n')

        print('请输入\033[31m邮箱用户名\033[0m：')
        print('+++｜例：\033[33msdfdfesd\033[0m｜@前面那一段|+++')
        mail_user = input('\033[31m邮箱用户名：\033[0m')
        if mail_user == '':
            print('|\033[31m输入为空，邮箱服务可能无法正常运行\033[0m' + '\n')
        else:
            print('|mail_host: \033[32m' + mail_user + '\033[0m\n')

        print('请输入\033[31m密码(部分邮箱为授权码)\033[0m：')
        print('+++｜例：\033[33mGVARYOSKBONSBMFB\033[0m｜开通SMTP可见|+++')
        mail_pass = input('\033[31m密码\033[0m：')
        if mail_pass == '':
            print('|\033[31m输入为空，邮箱服务可能无法正常运行\033[0m' + '\n')
        else:
            print('|mail_pass: \033[32m' + mail_pass + '\033[0m\n')
        
        print('请输入用于发送结果信息的邮箱：')
        print('+++｜例：\033[33msdfdfesd@yeah.net\033[0m|+++')
        sender = input('\033[31m邮箱\033[0m：')
        if sender == '':
            print('|\033[31m输入为空，邮箱服务可能无法正常运行\033[0m' + '\n')
        else:
            print('|sender: \033[32m' + sender + '\033[0m\n')

    
    print('\033[32m输入完毕，正在生成配置文件。\033[0m')
    config = {
        'user': {
            'username': username,
            'tellphone': tellphone,
            'username_account': username_account,
            'password': password,
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
        yaml_file = os.path.join(sys.path[0], 'config', 'config_sign.yml')
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, sort_keys=False, allow_unicode = True)
    except IOError:
        print('\033[31mIO 出错，无法生成配置文件。\033[0m' + '\n')
        print(IOError)
    else:
        print('\033[32m生成配置文件成功！\033[0m' + '\n')
        yaml_file = os.path.join(sys.path[0], 'config', 'config_sign.yml')
        with open(yaml_file, 'r', encoding='utf-8') as f:
            file_data = f.read()
            # config_read = yaml.load(file_data, Loader=yaml.FullLoader)
            print(file_data)
        print('\n' + '+++｜\033[32m已按福大“默认签到表格”生成配置文件，请对照，如有出入在config/config_sign.yml中修改或重新运行改程序\033[0m｜+++' + '\n')
    
    

def main():
    """
    main function
    """
    generateConfig()
    
if __name__ == '__main__':
    main()
