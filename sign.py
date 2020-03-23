import requests, json, time, logging
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 填入Cookie

headers = {
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
}
# 填入uid
uid = ""
coursedata = []
activeList = []
course_index = 0
speed = 10
status = 0
status2 = 0
activates = []


def backclazzdata():
    global coursedata
    url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"
    res = requests.get(url, headers=headers)
    cdata = json.loads(res.text)
    if (cdata['result'] != 1):
        print("课程列表获取失败")
        return 0
    for item in cdata['channelList']:
        if ("course" not in item['content']):
            continue
        pushdata = {}
        pushdata['courseid'] = item['content']['course']['data'][0]['id']
        pushdata['name'] = item['content']['course']['data'][0]['name']
        pushdata['imageurl'] = item['content']['course']['data'][0]['imageurl']
        pushdata['classid'] = item['content']['id']
        coursedata.append(pushdata)
    print("获取成功")
    # print(coursedata)
    printdata()


def printdata():
    global course_index, speed
    index = 1
    for item in coursedata:
        print(str(index) + ".课程名称:" + item['name'])
        index += 1
    course_index = int(input("请输入序号以设定监控课程")) - 1
    print("监控课程设定完成")
    speed = int(input("请输入监控频率"))
    print("监控频率设置完毕")
    startsign()


def taskactivelist(courseId, classId):
    global activeList
    url = "https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId=" + str(courseId) + "&classId=" + str(
        classId) + "&uid=" + uid
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    activeList = data['activeList']
    # print(activeList)
    for item in activeList:
        if ("nameTwo" not in item):
            continue
        if (item['activeType'] == 2 and item['status'] == 1):
            signurl = item['url']
            aid = getvar(signurl)
            if (aid not in activates):
                print("【签到】查询到待签到活动 活动名称:%s 活动状态:%s 活动时间:%s aid:%s" % (
                    item['nameOne'], item['nameTwo'], item['nameFour'], aid))
                sign(aid, uid)


def getvar(url):
    var1 = url.split("&")
    for var in var1:
        var2 = var.split("=")
        if (var2[0] == "activePrimaryId"):
            return var2[1]
    return "ccc"


def sign(aid, uid):
    global status, activates
    url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId=" + aid + "&uid=" + uid + "&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
    res = requests.get(url, headers=headers)
    if (res.text == "success"):
        print("用户:" + uid + " 签到成功！")
        mail("用户:" + uid + " 签到成功！")
        activates.append(aid)
        status = 2
    else:
        print("签到失败")
        mail("签到失败")
        activates.append(aid)


def startsign():
    global status, status2
    status = 1
    status2 = 1
    ind = 1
    print("监控启动 监控课程为:%s 监控频率为:%s" % (coursedata[course_index]['name'], str(speed)))
    while (status != 0 and status2 != 0):
        ind += 1
        taskactivelist(coursedata[course_index]['courseid'], coursedata[course_index]['classid'])
        time.sleep(speed)
        if (status == 1):
            print(str(ind) + " [签到]监控运行中，未查询到签到活动")
        elif (status == 2):
            print(str(ind) + " [新签到]监控运行中，未查询到签到活动")
    print("任务结束")
    printdata()


# 这里使用邮件的方式进行签到状态提醒，通过465端口发送。需填入
#    my_sender：发件人账户
#    my_pass:发件人smtp密码
#    my_user:收件人
#    smtp:(eg:smtp.126.com)
# 如不使用，可删除，并删掉sign中对应的mail
def mail(body):
    my_sender = ''  # 发件人
    my_pass = ''
    smtp=""

    my_user = ""
    ret = True
    try:

        Body = body
        msg = MIMEText(Body, 'html', 'utf-8')
        msg['From'] = formataddr(["我是发件人", my_sender])  
        msg['To'] = formataddr(["我是收件人", my_user])  
        msg['Subject'] = "签到"  

        server = smtplib.SMTP_SSL(smtp, 465) 
        server.login(my_sender, my_pass) 
        server.sendmail(my_sender, [my_user, ], msg.as_string())  
        server.quit() 
    except Exception as e:  
        print(e.with_traceback())
        ret = False
    return ret




backclazzdata()
