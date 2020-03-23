# XueXiTongAtuoSignIn

## 使用方法：

1. 环境：python3.x

2. 需要使用requests库

3. 需要准备的参数：
  - cookie（必须）
  - uid（必须）
  - 邮箱（可选）
  
4. 获取cookie和uid的方法（必须）：
  - 登录`http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1`
  - 按F12，在network中找到cookie，其中包含了uid
  - ![cookie](https://github.com/johnsun123/XueXiTongAtuoSignIn/blob/master/cookies.png "cookie.png")
  - 将这两个参数填入`sign.py`中即可
  
5. 准备邮件提醒的方法（可选）：
  - my_sender：发件人账户
  - my_pass:发件人smtp密码
  - my_user:收件人
  - smtp:(eg:smtp.126.com)
  - 登录到邮箱账号，在设置中开启POP3/SMTP，得到对应的smtp密码，填入`sign.py`中即可
  
  
感谢原作者：给我一碗炒饭
