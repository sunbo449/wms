from django.db import models


# 用户表
class UserProfile(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name='密码')
    mobile_phone = models.CharField(max_length=32, verbose_name='手机号', unique=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, verbose_name='角色')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, verbose_name='组别')

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name


# 班组表
class Team(models.Model):
    caption = models.CharField(max_length=32, verbose_name='班组')

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "班组表"
        verbose_name_plural = verbose_name


# 角色表
class Role(models.Model):
    caption = models.CharField(max_length=32, verbose_name='角色')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    last_time = models.DateTimeField(auto_now_add=True, verbose_name='最后修改时间')
 
    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


# 菜单表（URL）
class Menu(models.Model):
    title = models.CharField(max_length=32, verbose_name='菜单名')
    url = models.CharField(max_length=60, verbose_name='URL')

    def __str__(self):
        return "%s - %s" % (self.title, self.url)

    class Meta:
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name


# 权限表(角色绑定菜单URL)
class Permission(models.Model):
    role = models.ForeignKey('Role', on_delete=models.CASCADE, verbose_name='角色')
    menu_title = models.ForeignKey('Menu', on_delete=models.CASCADE, verbose_name='菜单')

    def __str__(self):
        return "%s - %s" % (self.role, self.menu_title)

    class Meta:
        verbose_name = "权限表"
        verbose_name_plural = verbose_name
