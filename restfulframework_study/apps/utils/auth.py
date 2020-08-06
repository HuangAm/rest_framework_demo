"""
这里面的认证类都是全局的，我们都将他们加载了配置文件中的 REST_FRAMEWORK 中
"""
from apps import models
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class Authentication(BaseAuthentication):
    # 认证类必须有authenticate、authenticate_header这两个方法，不然会报错
    def authenticate(self, request):
        token = request._request.GET.get("token")
        token_obj = models.UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        # 在 rest_framework 内部会将两个字段以元组的方式赋值给request, 以供后续操作使用
        # request.user = token_obj.user request.auth = token_obj
        # 源码在 rest_framework\request.py 的 380 行
        return token_obj.user, token_obj

    def authenticate_header(self, request):
        pass
