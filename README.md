# 福州大学 auto-sign

# 禁止任何人使用此项目提供付费的代挂服务

> ## **感谢[ZimoLoveShuang](https://github.com/ZimoLoveShuang/auto-sign)的开发，添加了新功能以及返回消息优化，有条件请支持原作者[ZimoLoveShuang](https://github.com/ZimoLoveShuang)。**

## 本项目适配 **福州大学** 今日校园签到服务，推荐有**服务器**的伙伴使用，当然由于ZimoLoveShuang模拟了登陆服务对所有学校均支持，云函数可参考原作微调使用。


# 新特性

1. ~~一键部署~~ 懒，过几天再写，其实挺简单的，感兴趣的自己研究下代码
2. 自动登陆配置，无需修改代码
3. **支持福州大学学号、密码登陆**
4. 添加邮件模块，可使用自己邮箱发送结果（也可选择原作者提供的邮箱服务）
5. ~~自动注册定时计划~~ 同一键部署代码
6. ~~邮件回复验证码~~
7. 能够自动识别`验证码图片`，但是*巧妙*避开了登陆密码需要验证码验证的情况 ：) 所以用不到。

# 说明
1. 仅学习交流~如有不妥请联系本人删除！
2. 本项目对福州大学签到服务进行了适配
3. 由于登陆限制，手机端登陆，服务器端会掉线，需重新登陆
> 这里说明一下：   
关于添加福州大学账号密码登陆的原因。
进出校门都要扫码，就导致了每次都要重新登陆！这个和每日签到就没区别了。  
由于福大的认证严格，每次登陆会消除上一登陆设备认证，就想到用`账号密码`登陆代替`手机验证码`。但是实现了账号密码登陆后，今日校园会对每一台`未认证设备`进行手机验证，白虾。。。  

> 偶然发现：使用目前登陆设备的`CpdailyInfo`作为参数，使用`账号密码`进行登陆是**可以跳过认证的！**`但是需要抓包，以后可以解决这个问题`  
或者使用手机自带的一键登陆功能  
目前来说，进一步实现的成本大于收益，日后可能实现邮件收发验证码，仅此而已  
项目完全开源，~~有想法~~想学习的同学可以查看代码
4. 如使用自己邮箱发送，需开启邮箱[SMTP服务](https://www.baidu.com/s?wd=%E9%82%AE%E7%AE%B1%E5%BC%80%E5%90%AFsmtp%E6%9C%8D%E5%8A%A1)
5. 虽然从每日4次改为1次，但是要重视签到
6. 有很大发挥余地，请**充满想象**

# 技术思路、环境
本项目使用python3 3 3 3 3 3 3  你只需要安装python3  
环境见requirements.txt  
福大登陆使用了加密，闲麻烦从网站提取了加密方法。  
福大账号密码与今日校园使用`ticket`认证，即DES加密登陆成功返回的跳转链接里的`mobile_token`  
福大账号密码登陆需要`六次request`  
1. 获取`extension`、`pwdDefaultEncryptSalt`、`lt`
2. 验证是否需要验证码（附加一个v与随机数即可避免。。。）
3. 将`password`、`pwdDefaultEncryptSalt`使用DES混淆加密
4. 登陆成功会返回`callback`链接，需要`禁止转发`才可获得
4. 返回来的结果中`+`会转码成`&#43;` 在加密前需解码
5. 使用门票`tecket`与今日校园认证  

邮件服务器使用`smtplib`、`email`实现，难度低，方便。
定时任务使用Linux系统标配：`crontab`

今日校园账号密码登陆的`手机验证码`使用了不同的链接，很细节。 

### 这么**细节**了恳请右上角`star` 点一下吧！救救孩子=）



# 使用

1. **下载项目**
```bash
# 下拉项目代码
git clone https://github.com/DogeZhang/auto-sign.git
cd auto-sign
```
2. **安装必备环境 （仅运行一次）** 

```bash
# 仅有python3 (直接用下面pip3的就好了)
pip install -r requirements.txt -t . -i https://mirrors.aliyun.com/pypi/simple
# 建议使用pip3安装
pip3 install -r requirements.txt -t . -i https://mirrors.aliyun.com/pypi/simple

```

3. **登陆**
```bash
python3 login.py
# 按照提示填入信息，相信你会的
```

4. **签到**
```bash
# 每日签到、健康检测-午签到 均适配
python3 login_sign.py
# 健康信息报表
python3 login_submit.py
```

5. **没了 总结一下技术要领（四行指令，一句签到）**
```bash
git clone https://github.com/DogeZhang/auto-sign.git && cd auto-sign
pip3 install -r requirements.txt -t . -i https://mirrors.aliyun.com/pypi/simple
python3 login.py
python3 login_sign.py
```
