from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time


# VISIT_RECORD = {}
#
#
# class VisitThrottle(BaseThrottle):
#     """60s访问三次"""
#
#     def __init__(self):
#         self.history = None
#
#     def allow_request(self, request, view):
#         # 获取用户 IP
#         # remote_addr = request.META.get('REMOTE_ADDR')
#         remote_addr = self.get_ident(request)
#         print(remote_addr)
#         ctime = time.time()
#         if remote_addr not in VISIT_RECORD:
#             VISIT_RECORD[remote_addr] = [ctime, ]
#             return True
#         history = VISIT_RECORD.get(remote_addr)
#         self.history = history
#         while history and history[-1] < ctime - 60:
#             history.pop()
#
#         if len(history) < 3:
#             history.insert(0, ctime)
#             return True
#
#         return False
#
#     def wait(self):
#         ctime = time.time()
#         return 60 - (ctime - self.history[-1])


class VisitThrottle(SimpleRateThrottle):
    """对普通用户做限制"""
    scope = "anonymity"

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    scope = "login_user"

    def get_cache_key(self, request, view):
        return request.user.username
