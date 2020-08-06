"""rest_framework_study2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from api import views

urlpatterns = [
    re_path(r'^(?P<version>[v1|v2]+)/users/$', views.UsersView.as_view(), name="uuu"),
    re_path(r'^(?P<version>[v1|v2]+)/parser/$', views.ParserView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/roles/$', views.RoleView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/user_info/$', views.UserInfoView.as_view()),
    re_path(r'^(?P<version>[v1|v2]+)/group/(?P<pk>\d+)/$', views.GroupView.as_view(), name='gp'),
    re_path(r'^(?P<version>[v1|v2]+)/user_group/$', views.UserGroupView.as_view(), name='gp'),
    re_path(r'^(?P<version>[v1|v2]+)/page1/$', views.Page1View.as_view(), name='gp'),
    re_path(r'^(?P<version>[v1|v2]+)/page2/$', views.Page2View.as_view(), name='gp'),
    re_path(r'^(?P<version>[v1|v2]+)/page3/$', views.Page3View.as_view(), name='gp'),
    re_path(r'^(?P<version>[v1|v2]+)/v1/$', views.View1View.as_view({'get': 'list'})),

    re_path(r'^(?P<version>[v1|v2]+)/v2/$', views.View2View.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^(?P<version>[v1|v2]+)/v2/(?P<pk>\d+)/$', views.View2View.as_view(
        {'get': 'retrieve', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'})),
]
