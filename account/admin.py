from django.contrib import admin
from account import models
# Register your models here.

@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'mobile_phone', 'role', 'team')


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'create_time', 'last_time')

    

@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption')

@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')


@admin.register(models.Permission)
class Permissiondmin(admin.ModelAdmin):
    list_display = ('id', 'role', 'menu_title')

