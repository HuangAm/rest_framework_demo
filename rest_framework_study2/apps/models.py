from django.db import models


# Create your models here.
class UserGroup(models.Model):
    """用户组表"""
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    """用户表"""
    user_type_choices = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP'),
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)  # 组外键
    roles = models.ManyToManyField("Role")


class UserToken(models.Model):
    """Token 表"""
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Role(models.Model):
    """角色表"""
    title = models.CharField(max_length=32)
