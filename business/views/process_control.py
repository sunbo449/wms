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


def vehicle_care_of(request):
    """车辆转接操作"""
    pass_on_to_team = request.GET.get("pass_on_to_team").replace(" ", "").strip()  # 转接目的班组
    care_of_team = request.GET.get("care_of_team").replace(" ", "")[:4]  # 转接班组
    vehicle_num = request.GET.get("care_of_team").replace(" ", "")[4:]  # 转接车牌号

    if "快修" in care_of_team:  # 如果转接的班组信息中包含快修，那么肯定是快修班组，否则不处理
        quick_service_vehicle_wip = models.QuickServiceVehicle.objects.filter(
            quick_service_team=care_of_team, vehicle_num=vehicle_num).exclude(
            quick_service_status='完工交车').first().wip

        # 获取机电班组是否存在对应车辆信息
        service_vehicle_info = models.ServiceVehicle.objects.filter(wip=quick_service_vehicle_wip)
        if service_vehicle_info.exists():
            return JsonResponse({'status': False, "errors": '该车辆信息，在被转工序存在，故不能转车，可修改车辆信息'})
        else:
            # 2. 查询目的班组是否存在这个车辆信息，根据wip查询，如果存在那么不允许转接，否则根据信息创建目的班组的车辆信息
            # 3. 转接班组的转接车辆的默认状态更改为完工交车状态
            # 更改转接班组的车辆状态为完工交车， 创建目的班组的信息
            quick_service_vehicle = models.QuickServiceVehicle.objects.get(wip=quick_service_vehicle_wip)
            quick_service_vehicle.quick_service_status = "完工交车"
            quick_service_vehicle.save()
            models.ServiceVehicle.objects.create(service_team=pass_on_to_team, wip=quick_service_vehicle_wip,
                                                 vehicle_num=vehicle_num)

    elif "机电" in care_of_team:
        service_vehicle_wip = models.ServiceVehicle.objects.filter(
            service_team=care_of_team, vehicle_num=vehicle_num).exclude(
            service_status='完工交车').first().wip
        quick_service_vehicle_info = models.QuickServiceVehicle.objects.filter(wip=service_vehicle_wip)
        if quick_service_vehicle_info.exists():
            return JsonResponse({'status': False, "errors": '该车辆信息，在被转工序存在，故不能转车，可修改车辆信息'})
        else:
            service_vehicle = models.ServiceVehicle.objects.get(wip=service_vehicle_wip)
            service_vehicle.service_status = "完工交车"
            service_vehicle.save()
            models.QuickServiceVehicle.objects.create(quick_service_team=pass_on_to_team, wip=service_vehicle_wip,
                                                      vehicle_num=vehicle_num)
    else:
        return JsonResponse({'status': False, "errors": '只有机电快修工序，才能互转车辆！其他工序不可！'})
    return JsonResponse({'status': True})
