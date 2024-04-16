# @Author : Kql
# @Time : 2023/6/17 15:41
import datetime
import hashlib
import base64
import json

import requests  # http/https请求


class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self, accountSid, accountToken, appId, templateId):
        self.accountSid = accountSid  # 账户ID
        self.acccountToken = accountToken  # 授权令牌
        self.appId = appId  # 应用id
        self.templateId = templateId  # 模版id

    def get_request_url(self, sig):
        # /2013-12-26/Accounts/{accountSid}/SMS/{funcdes}?sig={SigParameter}
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s' % (self.accountSid, sig)
        return self.url

    def get_timestamp(self):
        # 生成时间戳
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self, timestamp):
        # 生成业务url中的sig
        s = self.accountSid + self.acccountToken + timestamp
        m = hashlib.md5()
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_request_header(self, timestamp):
        s = self.accountSid + ':' + timestamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': auth
        }

    def get_request_body(self, phone, code):
        return {
            "to": phone,
            "appId": self.appId,
            "templateId": self.templateId,
            'datas': [code, "3"]
        }

    def request_api(self, url, header, body):
        res = requests.post(url, headers=header, data=body)
        return res.text

    def run(self, phone, code):
        # 获取时间戳
        timestamp = self.get_timestamp()
        # 生成签名
        sig = self.get_sig(timestamp)
        # 生成业务url
        url = self.get_request_url(sig)
        # print(url)
        header = self.get_request_header(timestamp)
        print(header)
        # 生成请求体
        body = self.get_request_body(phone, code)
        # 发送请求
        data = self.request_api(url, header, json.dumps(body))
        return data


if __name__ == '__main__':
    # accountSid, accountToken, appId, templateId
    config = {
        "accountSid": "2c94811c88bf35030188c823b9b902cc",
        "accountToken": "bd81141c557842d19334168b303eec6f",
        "appId": "2c94811c88bf35030188c823bafb02d3",
        "templateId": "1"
    }
    obj = YunTongXin(**config)
    res = obj.run("17753639501", '9810')
    print(res)
