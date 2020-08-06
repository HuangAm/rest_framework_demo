from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from apps import models
import json
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.parsers import JSONParser, FormParser


#################################### 版本 ##################################
class UsersView(APIView):
    """
    版本示例
    """

    def get(self, request, *args, **kwargs):
        print(request.version)
        print(request.versioning_scheme)
        u1_url = request.versioning_scheme.reverse(viewname='uuu', request=request, )
        print(u1_url)
        u2_url = reverse(viewname='uuu', kwargs={'version': request.version})
        print(u2_url)
        return HttpResponse('用户列表')


#################################### 解析器 ##################################
class ParserView(APIView):
    """
    解析器示例
    JSONParser 只能解析 content-type:application/json 的头
    """

    def post(self, request, *args, **kwargs):
        print(request.data, "xxx")
        print(type(request.data))
        return HttpResponse("ParserView")


#################################### 序列化 ##################################
class RolesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class RoleView(APIView):
    """
    序列化示例
    """

    def get(self, request, *args, **kwargs):
        # 原生序列化方式
        # roles = models.Role.objects.all().values('id', 'title')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)

        # rest_framework 提供的序列化方式
        # 多条数据
        # roles = models.Role.objects.all()
        # ser = RolesSerializer(instance=roles, many=True)  # many=True 表示有多条数据
        # ret = json.dumps(ser.data, ensure_ascii=False)
        # 单条数据
        role = models.Role.objects.all().first()
        ser = RolesSerializer(instance=role, many=False)  # many=False 表示单条数据
        # ser.data 已经是转换完成的结果
        # ret = json.dumps(ser.data, ensure_ascii=False)
        # return HttpResponse(ret)
        return Response(ser.data)


# class UserInfoSerializer(serializers.Serializer):
#     # source 解决的是 choice 类的数据，如：models.UserInfo 的 user_type 字段
#     user_type_id = serializers.IntegerField(source="user_type")  # 只能拿到数字
#     user_type_title = serializers.CharField(source="get_user_type_display")  # row.get_user_type_display
#     username = serializers.CharField()
#     password = serializers.CharField()
#     gp = serializers.CharField(source="group.id")
#     # rls = serializers.CharField(source="roles.all")  # 返回的是 QuerySet 对象
#     rls = serializers.SerializerMethodField()  # 自定义显示，必须配合 'get_%s'%'rls' 方法用
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id': item.id, 'title': item.title})
#         return ret


# class UserInfoSerializer(serializers.ModelSerializer):
#     user_type_title = serializers.CharField(source="get_user_type_display")
#     rls = serializers.SerializerMethodField()
#
#     def get_rls(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id': item.id, 'title': item.title})
#         return ret
#
#     class Meta:
#         model = models.UserInfo
#         # fields = "__all__"
#         fields = ['id', 'username', 'password', 'user_type_title', 'rls']

class UserInfoSerializer(serializers.ModelSerializer):
    # lookup_url_kwarg 参数对应路由中的 pk 关键字，如果 url 中的 pk 做修改后，这里也对应修改
    group = serializers.HyperlinkedIdentityField(view_name='gp', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
        # 下面的这个操作可以实现自动序列化连表
        # depth = 1  # 指的是层数，最好不要超过3层，官方要求不能大于 10
        depth = 0


class UserInfoView(APIView):
    """
    序列化示例
    """

    def get(self, request, *args, **kwargs):
        users = models.UserInfo.objects.all()
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        print(ret)
        return HttpResponse(ret)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserGroup
        fields = '__all__'


class GroupView(APIView):
    """
    不像上面序列化一下返回 group 中的数据，而是返回一个 url
    """

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = models.UserGroup.objects.filter(pk=pk).first()
        ser = GroupSerializer(instance=obj, many=False, context={'request': request})
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


#################################### 数据验证 ##################################
############### 不利用钩子函数的方式 #########################
# class XXValidator(object):
#     def __init__(self, base):
#         self.base = base
#
#     def __call__(self, value):
#         if not value.startswith(self.base):
#             message = '标题必须为 %s 开头' % self.base
#             raise serializers.ValidationError(message)
#
#
# class UserGroupSerializer(serializers.Serializer):
#     title = serializers.CharField(error_messages={'required': '标题不能为空'}, validators=[XXValidator('亲爱的')])
#
#
# class UserGroupView(APIView):
#     def post(self, request, *args, **kwargs):
#         ser = UserGroupSerializer(data=request.data)
#         if ser.is_valid():
#             return JsonResponse(ser.validated_data)
#         else:
#             return JsonResponse(ser.errors)

############### 利用钩子函数的方式 #########################
# 钩子函数是 'validate_' 开头
class UserGroupSerializer(serializers.Serializer):
    title = serializers.CharField(error_messages={'required': '标题不能为空'})

    def validate_title(self, value):
        from rest_framework import exceptions
        if not value.startswith("亲爱的"):
            raise exceptions.ValidationError("必须以 亲爱的 开头")
        return value


class UserGroupView(APIView):
    def post(self, request, *args, **kwargs):
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            return JsonResponse(ser.validated_data)
        else:
            return JsonResponse(ser.errors)


#################################### 分页 ##################################
########### a ##############
from api.utils.serializers.pager import PageSerialiser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class MyPageNumberPagination(PageNumberPagination):
    page_size = 2  # 每页默认展示 2 条
    max_page_size = 5  # 每页最多展示 5 条
    page_size_query_param = 'size'  # 通过 ?size=3 设置每页展示 3 条
    page_query_param = 'page'  # 通过 ?page=1 请求第 1 页数据


class Page1View(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
        # ser = PageSerialiser(instance=roles, many=True)
        # print(ser.data)
        # 创建分页对象
        # 原生对象
        # pg = PageNumberPagination()
        # 自定制对象
        pg = MyPageNumberPagination()
        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(pager_roles)
        # 对数据进行序列化
        ser = PageSerialiser(instance=pager_roles, many=True)
        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)


########### b ##############
from rest_framework.pagination import LimitOffsetPagination


class Page2View(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
        # 创建分页对象
        # 原生对象
        pg = LimitOffsetPagination()
        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(pager_roles)
        # 对数据进行序列化
        ser = PageSerialiser(instance=pager_roles, many=True)
        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)


########### c ##############
from rest_framework.pagination import CursorPagination


class MyCursorPagination(CursorPagination):
    cursor_query_param = 'cursor'
    ordering = '-id'
    template = 'rest_framework/pagination/previous_and_next.html'

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None

    # Set to an integer to limit the maximum page size the client may request.
    # Only relevant if 'page_size_query_param' has also been set.
    max_page_size = None


class Page3View(APIView):
    def get(self, request, *args, **kwargs):
        # 获取所有数据
        roles = models.Role.objects.all()
        # 创建分页对象
        # 原生对象
        pg = MyCursorPagination()
        # 在数据库中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        print(pager_roles)
        # 对数据进行序列化
        ser = PageSerialiser(instance=pager_roles, many=True)
        # return Response(ser.data)
        return pg.get_paginated_response(ser.data)


#################################### 视图 ##################################
########## GenericViewSet ###############
from rest_framework.viewsets import GenericViewSet


class View1View(GenericViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PageSerialiser
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        # 获取数据
        roles = self.get_queryset()  # models.Role.objects.all()
        # 分页
        pager_roles = self.paginate_queryset(roles)
        # 序列化
        ser = self.get_serializer(instance=pager_roles, many=True)
        return Response(ser.data)


########## ModelViewSet ###############
from rest_framework.viewsets import ModelViewSet
from api.utils.serializers.pager import PageSerialiser
from rest_framework.renderers import JSONOpenAPIRenderer, BrowsableAPIRenderer


class View2View(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = PageSerialiser
    pagination_class = PageNumberPagination
