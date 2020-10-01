from django.shortcuts import render, redirect
from django.http import JsonResponse
from utils.login_auth import permission
from utils.info_verification import vehicle_info_validation
from utils import vehicle_status_utils
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
    # 1.使用字符串分割，获取提交的  车牌号 和 班组 用来确定车辆信息
    service_team = str(request.GET.get('veh_num')).replace(" ", "")[0:4]  # 班组名
    veh_num = str(request.GET.get('veh_num')).replace(" ", "")[4:]  # 车牌号
    veh_status = request.GET.get('veh_status').replace(" ", "").strip()  # 车辆状态
    # 2.将信息传递给封装的车辆状态处理类，去进行车辆状态处理
    vehicle_status_utils.ServiceStatusEdit(request, service_team, veh_num, veh_status)

    return JsonResponse({'status': True})


def vehicle_road_status_edit(request):
    """结束路试操作"""
    road_status = request.GET.get("road_status").replace(" ", "").strip()  # 路试状态
    road_veh_num = request.GET.get("road_veh_num").replace(" ", "")[4:]  # 路试车辆信息
    driver = str(request.wms[0])

    try:
        road_test_obj = models.VehicleRoadTest.objects.filter(vehicle_num=road_veh_num).exclude(
            service_status='结束路试').first()
        road_test_obj.service_status = road_status
        road_test_obj.driver = driver
        road_test_obj.save()
        # 同时查询快修和机电班组是否有符合条件的车辆，并且将其维修状态修改为正常维修状态
        exists = models.ServiceVehicle.objects.filter(vehicle_num=road_veh_num,
                                                      service_team=road_test_obj.service_team).exclude(
            service_status='完工交车')
        quick_service_exists = models.QuickServiceVehicle.objects.filter(
            vehicle_num=road_veh_num, quick_service_team=road_test_obj.service_team).exclude(
            quick_service_status='完工交车')

        if exists.exists():
            veh_obj = models.ServiceVehicle.objects.get(id=exists.first().id)
            veh_obj.service_status = "正常维修"
            veh_obj.save()

        if quick_service_exists.exists():
            veh_obj = models.QuickServiceVehicle.objects.get(id=quick_service_exists.first().id)
            veh_obj.quick_service_status = "正常维修"
            veh_obj.save()

    except Exception as e:
        return JsonResponse({'status': False, 'data': '试车结束问题'})

    return JsonResponse({'status': True})
