# -*- coding: utf-8 -*-
import requests


class YunPian(object):
    """
    单条短信发送, 智能匹配短信模板
    * @ param apikey成功注册后登录云片官网, 进入后台可查看
    * @ param text需要使用已审核通过的模板或者默认模板
    * @ param mobile接收的手机号, 仅支持单号码发送
    * @ return json格式字符串
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "http://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【奇洛米特】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        import json
        re_dict = json.loads(response.text)  # 解析出来字符
        return re_dict

if __name__ == "__main__":
    api_key = 'c62d03985384b6554b7461b3339e6c67'

    yun_pian = YunPian('c62d03985384b6554b7461b3339e6c67')
    yun_pian.send_sms("2017", '13801268603')
