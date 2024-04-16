# @Author : Kql
# @Time : 2023/6/19 18:57

# 发送短信
from tools.sms import YunTongXin
from dadablog.celery import app


@app.task
def send_sms_c(phone, code):
    config = {
        "accountSid": "2c94811c88bf35030188c823b9b902cc",
        "accountToken": "bd81141c557842d19334168b303eec6f",
        "appId": "2c94811c88bf35030188c823bafb02d3",
        "templateId": "1"
    }
    yun = YunTongXin(**config)
    res = yun.run(phone, code)
    return res
