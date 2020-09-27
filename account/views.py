from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms.account_forms import RegisterForm
from account.models import UserProfile
from utils.md5 import encrypt
from utils.login_auth import admin_permission  # 自定义登录认证组件


@admin_permission
def account(request):
    """
    用户管理界面之用户注册处理
    """
    context = {}
    if request.method == "GET":
        form = RegisterForm()
        user_lis = UserProfile.objects.all()
        context['user_lis'] = user_lis
        context['form'] = form
        return render(request, 'account.html', context)

    form = RegisterForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/index'})  # 返回给前端json数据
    return JsonResponse({'status': False, 'errors': form.errors})  # 验证失败返回给失败的信息


def login(request):
    """
    用户登录处理
    """
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        mobile_phone = request.POST.get('mobile_phone', '')
        pwd = encrypt(request.POST.get('password', ''))
        if mobile_phone == "" or pwd == "":
            return JsonResponse({'status': False, 'errors': "手机号或密码不能为空"})

        user_obj = UserProfile.objects.filter(mobile_phone=mobile_phone, password=pwd).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 7)  # 设置存储的过期时间7天
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False, 'errors': "用户名或者密码错误"})


def logout(request):
    """
    退出登录
    """
    request.session.flush()
    return redirect('account:login')


@admin_permission
def del_user(request):
    """用户删除"""
    user_name = request.GET.get('user_name')
    UserProfile.objects.filter(username=user_name).delete()
    return JsonResponse({'status': True})


@admin_permission
def edit_user(request, user_id):
    """用户修改"""
    user_obj = UserProfile.objects.filter(id=user_id).first()
    if request.method == "GET":
        form = RegisterForm(instance=user_obj)
        return render(request, 'edit_user.html', {'form': form})

    form = RegisterForm(data=request.POST, instance=user_obj)
    if form.is_valid():
        form.save()
        return redirect("account:account")
    else:
        return render(request, 'edit_user.html', {"form": form})   # 验证失败返回给失败的信息


def error_404(request):
    """错误页面"""
    return render(request, 'admin_404.html')
