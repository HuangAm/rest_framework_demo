from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "必须是 SVIP 才能访问"

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class VIPPermission(BasePermission):
    message = "只有 VIP、SVIP 才能访问"

    def has_permission(self, request, view):
        if request.user.user_type > 1:
            return False
        return True
