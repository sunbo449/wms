from django import template
from account.models import UserProfile, Team
from business.models import ServiceProject
register = template.Library()
# ***  模板文件： 用于将服务顾问 维修班组 维修项目等信息传递给前端页面 ****


@register.simple_tag
def sa_team():
    """服务顾问"""
    sa_list = []
    sa_obj = UserProfile.objects.filter(role__caption="服务顾问")
    for sa in sa_obj:
        sa_list.append(sa)
    return sa_list


@register.simple_tag
def quick_service_team():
    """快修班组"""
    team_list = []
    team_obj = Team.objects.filter(caption__regex="快修")
    for team in team_obj:
        team_list.append(team)
    return team_list


@register.simple_tag
def service_team():
    """机电班组"""
    team_list = []
    team_obj = Team.objects.filter(caption__regex="机电")
    for team in team_obj:
        team_list.append(team)
    return team_list


@register.simple_tag
def service_project():
    """维修项目"""
    project_list = []
    project_obj = ServiceProject.objects.all()
    for project in project_obj:
        project_list.append(project)
    return project_list
