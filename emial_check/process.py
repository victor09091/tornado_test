# coding:utf-8
import requests, json, datetime

# 调用 SendCloud 的 WEBAPI 所需参数
API_USER = 'victor_yux_test_HbStZY'
API_KEY = '5GfjAG4pvbL6ustL'
import requests, json

url = "http://api.sendcloud.net/apiv2/mail/send"


def send_email(name, authcode, email):
    """
    给指定邮箱发送验证信息
    :param name:
    :param email:
    :return:
    """
    # database = DataBase(host, user, pwd, base)
    # database.set_table(table)
    # 使用 email 和 name 查询数据库
    # 数据库查询返回的记录是一个 tuple
    # 分别获取 name, email, token, authcode 信息

    # record = DataBase.query_by_email(name, email)
    # database.close()
    # name = record[1]
    # email = record[2]
    # token = record[3]
    # authcode = record[5]

    # 构造完整的邮箱认证链接
    # link = base_link + 'token=%s&authcode=%s' % (token, authcode)

    # "to"：指定目标邮箱
    # "sub"：指定替换变量
    # 将模板中定义的变量 %name% 和 %url% 分别进行替换成真实值
    sub_vars = {
        'to': [email],
        'sub': {
            '%name%': [name],
            '%authcode%': [authcode],
        }
    }

    # 您需要登录SendCloud创建API_USER，使用API_USER和API_KEY才可以进行邮件的发送。
    str = "尊敬的{}你好，<p>欢迎注册爱发信, 这是您的验证码:{}</p>".format(name, authcode)
    params = {"apiUser": API_USER,
              "apiKey": API_KEY,
              "from": "service@sendcloud.im",
              "fromName": "测试公司邮件",
              "to": [email],
              "subject": "test公司验证码邮件！",
              "html": str,
              }
    r = requests.post(url, files={}, data=params)
    print r.text

    # 获取请求返回的状态
    # 200 说明请求成功，否则失败
    if r.status_code == 200:
        return True
    else:
        return False
