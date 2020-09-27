from django.utils.deprecation import MiddlewareMixin
from account import models


class AuthMiddleware(MiddlewareMixin):
    """自定义验证用户登录的中间件"""
    def process_request(self, request):
        user_id = request.session.get('user_id', 0)
        user_obj = models.UserProfile.objects.filter(id=user_id)
        request.wms = user_obj


class PermissionMiddleware(MiddlewareMixin):
    """用户权限中间件"""
    def process_request(self, request):
        user_id = request.session.get('user_id', 0)
        # 登录的时候有 team 退出的时候，没有team这个属性，就会报错IndexError，那么处理一下
        try:
            user_team = models.UserProfile.objects.filter(id=user_id)[0].team
            request.team = str(user_team)
        except IndexError as e:
            user_team = models.UserProfile.objects.filter(id=user_id).first()
            request.team = user_team
