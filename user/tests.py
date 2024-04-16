from django.test import TestCase

# Create your tests here.
import time
import jwt # 需要安装pyjwt  pip isntall pyjwt

secret_key = 'secret'  # 密钥

# 生成token
data = {'a': 1, 'b': 2}
data['exp'] = int(time.time()) + 60 *5  # 过期时间设置为 当前时间加5分钟

token = jwt.encode(data, secret_key, algorithm='HS256')
print(token)
# # 验证token
#
data1 =  jwt.decode(token, secret_key, algorithms=['HS256'])  # 注意解码时，算法参数为algorithms，多一个s
print(data1)
# # 如果token不合法，解码时会抛出jwt.PyJWTError异常
# exp = data1.pop('exp') # 得到超时时间
# assert exp >= time.time()  # 验证未过期
# assert data1 == data  # 验证还原的数据与原数据相同
