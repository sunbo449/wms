from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from utils.login_auth import permission
from utils.info_verification import vehicle_info_validation
from business import models


@permission
def index(request):
    """首页显示"""
    return render(request, 'index.html')


@permission
def spectaculars(request):
    """看板页面信息显示"""
    return render(request, 'spectaculars.html')


@permission
def unfinished(request):
    """在场车辆页面显示"""
    return render(request, 'unfinished.html')


def vehicle_info(request):
    """ 车辆信息创建 """

    if vehicle_info_validation(request) is True:
        return JsonResponse({'status': True, "data": "车辆信息创建成功！"})
    return JsonResponse({'status': False, "data": vehicle_info_validation(request)})


def vehicle_status_edit(request):
    """ 车辆状态操作 """
    # 使用字符串分割，获取提交的  车牌号 和 班组 用来确定车辆信息
    service_team = str(request.GET.get('veh_num')).replace(" ", "")[0:4]
    veh_num = str(request.GET.get('veh_num')).replace(" ", "")[4:]
    veh_status = request.GET.get('veh_status').replace(" ", "")

    # 判断 数据库中是否存在对应的车辆信息和班组信息，如果存在那么获取车辆信息，进行状态更改
    if models.QuickServiceVehicle.objects.filter(vehicle_num=veh_num, quick_service_team=service_team).exists():
        veh_message = models.QuickServiceVehicle.objects.get(vehicle_num=veh_num)
        veh_message.quick_service_status = veh_status
        veh_message.save()

    if models.ServiceVehicle.objects.filter(vehicle_num=veh_num, service_team=service_team).exists():
        veh_message = models.ServiceVehicle.objects.get(vehicle_num=veh_num)
        veh_message.service_status = veh_status
        veh_message.save()

    return JsonResponse({'status': True})
