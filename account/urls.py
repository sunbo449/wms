from os import name
from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
    path("login", views.login, name='login'),  # 用户登录
    path('logout', views.logout, name='logout'),  # 用户退出
    path("del_user", views.del_user, name="del_user"),  # 用户删除
    path("edit_user/<user_id>", views.edit_user, name="edit_user"),   # 用户修改
    path("error_404", views.error_404, name="error_404"),   # 错误页面
    path("", views.account, name='account'),  # 后台管理之用户注册
]
