from django.shortcuts import redirect
from account.models import UserProfile


# 自定义登录验证组件（后期改为权限验证组件）
def permission(func):
    def inner(request, *args, **kwargs):
        user_id = request.session.get('user_id')   # 判断用户是否登陆，没有跳转回登录页面
        if not user_id:
            return redirect("account:login")
        return func(request, *args, **kwargs)
    return inner


# 自定义登录验证组件（后期改为权限验证组件）
def admin_permission(func):
    def inner(request, *args, **kwargs):
        user_id = request.session.get('user_id')   # 判断用户是否登陆，没有跳转回登录页面
        if not user_id:
            return redirect("account:login")
        user_role = str(UserProfile.objects.filter(id=user_id).first().role)
        if user_role != "管理员":
            return redirect("account:error_404")
        return func(request, *args, **kwargs)
    return inner
