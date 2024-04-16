# @Author : Kql
# @Time : 2023/6/14 17:08

import jwt
from user.models import UserProfile
from django.http import JsonResponse
from django.conf import settings
import json

# jwt 校验登录和校验权限
def logging_check(func):
    def wrap(request, *args, **kwargs):
        # 获取token，request.META.get('HTTP_AUTHORIZATION)
        # 校验token
        # 失败，403 errorPlease login
        token = json.loads(request.META.get('HTTP_AUTHORIZATION'))
        if not token:
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)
        # 校验jwt
        try:
            res = token
            # res = jwt.decode(token, settings.JWT_TOKEN_KET, algorithms=settings.JWT_ALGORITHM)
        except Exception as e:
            print('jwt decode error is %s' % (e))
            result = {'code': 403, 'error': 'Please login'}
            return JsonResponse(result)
        # 获取登录用户 将获取的用户的用户名通过ORM进行一次查询，之后可以使用request进行使用该用户下的所有信息。
        # print(res)
        username = res['username']
        user = UserProfile.objects.get(username=username)
        request.myuser = user
        return func(request, *args, **kwargs)

    return wrap


# 使用token校验访问者
def get_user_by_request(request):
    k = request.META.get('HTTP_AUTHORIZATION')
    if not k:
        return None
    token = json.loads(k)
    print(token)
    try:
        res = token
        # res = jwt.decode(token, settings.JWT_TOKEN_KET, algorithms=settings.JWT_ALGORITHM)
    except Exception as e:
        return None
    if(res!=None):
        username = res['username']
        user = UserProfile.objects.get(username=username)
        return user
    else:
        return None
