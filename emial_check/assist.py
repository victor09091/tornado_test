# coding:utf-8
import hashlib, random, string


def get_token(name, email, model=None):
    """
    使用由name, time 组成的明文生成相应密文
    :param name:
    :param email:
    :return:
    """
    data = "%s%s%s" % (name, email, model)
    hash_md5 = hashlib.md5(data)
    return hash_md5.hexdigest()


def get_authcode(length=5):
    """
    生成长度为 length 的随机字符串作为验证码
    :param length:
    :return:
    """
    char_set = list(string.digits + string.ascii_letters)
    random.shuffle(char_set)
    return "".join(char_set[:length])