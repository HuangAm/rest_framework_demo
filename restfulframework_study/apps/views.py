from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from apps import models
from apps.utils.permission import SVIPPermission
from apps.utils.throttle import VisitThrottle

ORDER_DICT = {
    1: {
        "name": "媳妇",
        "age": 19,
        "gender": "男",
        "content": "..."
    },
    2: {
        "name": "老狗",
        "age": 19,
        "gender": "男",
        "content": "..."
    }
}


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding="utf-8"))
    m.update(bytes(ctime, encoding="utf-8"))
    return m.hexdigest()


class AuthView(APIView):
    """
    用户登录认证
    """
    authentication_classes = []  # 阻止认证
    permission_classes = []  # 阻止权限
    throttle_classes = [VisitThrottle, ]  # 局部节流控制

    def post(self, request, *args, **kwargs):
        ret = {"code": 1000, "msg": None}
        try:
            user = request.POST.get("username")
            pwd = request.POST.get("password")
            obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret["code"] = 1001
                ret["msg"] = "用户名或密码错误"
            # 为登陆用户创建新 token
            token = md5(user)
            # 存在就更新，不存在就创建
            models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
            # 给用户返回新的 token
            ret["token"] = token
        except Exception as e:
            ret["code"] = 1002
            ret["msg"] = "请求异常"
        return JsonResponse(ret)


class OrderView(APIView):
    """
    订单相关业务（SVIP）
    """
    permission_classes = [SVIPPermission, ]  # 局部权限认证

    def get(self, request, *args, **kwargs):
        ret = {"code": 1000, "msg": None}
        try:
            ret["data"] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """
    用户信息（SVIP、VIP）
    """

    def get(self, request, *args, **kwargs):
        return HttpResponse("用户信息")
