# 福州大学 auto-sign

# 禁止任何人使用此项目提供付费的代挂服务

> ## **本项目fork自[ZimoLoveShuang](https://github.com/ZimoLoveShuang/auto-sign)，感谢ZimoLoveShuang的开发，核心代码逻辑没有改动，仅添加了些许新功能以及返回消息优化，有条件请支持原作者[ZimoLoveShuang](https://github.com/ZimoLoveShuang)。**

## 本项目适配 **福州大学** 今日校园签到服务，推荐有**服务器**的伙伴使用，当然由于ZimoLoveShuang模拟了登陆服务对所有学校均支持，云函数可参考原作微调使用。


# 新特性

1. 一键部署
2. 自动登陆配置，无需修改代码
3. 添加邮件模块，可使用自己邮箱发送结果（也可选择原作者提供的邮箱服务）
4. 自动注册定时计划

# 说明
1. 如有不妥请联系本人删除
2. 本项目对福州大学签到服务进行了适配
3. 由于登陆限制，手机端登陆，服务器端会掉线，需重新登陆
4. 如使用自己邮箱发送，需开启邮箱[SMTP服务](https://www.baidu.com/s?wd=%E9%82%AE%E7%AE%B1%E5%BC%80%E5%90%AFsmtp%E6%9C%8D%E5%8A%A1&rsv_spt=1&rsv_iqid=0x9b8af0e0001310be&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=20&rsv_sug1=17&rsv_sug7=100&rsv_t=dd93VNICKFdGlO1kYyK0aV%2BvLo1wn5UC3mYu86pc7e5ScYud0dAyJQyOWU5O3%2BxTHHeq&sug=%25E9%2582%25AE%25E7%25AE%25B1%25E5%25BC%2580%25E5%2590%25AFsmtp%25E6%259C%258D%25E5%258A%25A1&rsv_n=1)
5. 虽然从每日4次改为1次，但是要重视签到

# 使用

## 请参考[auto-submit项目](https://github.com/ZimoLoveShuang/auto-submit)

#### 如果你不会配置表单组默认选项配置，请先配置好user信息之后本地执行generate.py然后将分割线下的内容复制到配置文件中对应位置

#### 如遇到依赖问题，请去[`auto-sumit`](https://github.com/ZimoLoveShuang/auto-submit)项目下载`dependency.zip`，然后参考`auto-submit`项目的说明将函数依赖层添加到腾讯云函数

#### 如果不知道怎么配置经纬度信息，可以访问[这里](http://zuobiao.ay800.com/s/27/index.php)，将经纬度四舍五入保留六位小数之后的放入配置文件对应位置即可

#### 如果一天签到多次，除了问题不一样之外，其他都一样，你又不想配置多个云函数的话，配置文件设置不检查就行了

# 其他

1. 项目依赖于我的开源项目[模拟登陆 金智教务统一登陆系统 的API](https://github.com/ZimoLoveShuang/wisedu-unified-login-api)
2. `Cpdaily-Extension`本质上就是对一个json对象进行了des加密，然后编码为了Base64字符串，加密解密实现可以参考[Java版](https://github.com/ZimoLoveShuang/yibinu-score-crawler/blob/master/src/main/java/wiki/zimo/scorecrawler/helper/DESHelper.java) [python版](https://github.com/ZimoLoveShuang/auto-submit/blob/master/currency/encrypt.py)
3. 也欢迎其他学校学子在此提交适用于自己学校的配置，命名规则为`config_xxxx.yml`，`xxxx`为学校英文简称