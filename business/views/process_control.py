from django.shortcuts import render
from django.http import JsonResponse
from utils.login_auth import permission, admin_permission
from utils.info_verification import vehicle_info_validation
from utils import vehicle_status_utils
from business import models


# --------------------------------------------
#   该视图文件功能：
#   1-车辆信息录入页面操作 ： 车辆信息录入功能
#   2-动态看板页面操作 : 车辆状态操作、各种派工操作
# --------------------------------------------


@permission
def index(request):
    """首页显示"""
    return render(request, 'index.html')

# ----- Start 看板页面信息处理 ----------


@permission
def spectaculars(request):
    """看板页面信息显示"""
    return render(request, 'spectaculars.html')


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

    except Exception:
        return JsonResponse({'status': False, 'data': '试车结束问题'})

    return JsonResponse({'status': True})


def vehicle_care_of(request):
    """车辆转接操作"""
    pass_on_to_team = request.GET.get("pass_on_to_team").replace(" ", "").strip()  # 转接目的班组
    care_of_team = request.GET.get("care_of_team").replace(" ", "")[:4]  # 转接班组
    vehicle_num = request.GET.get("care_of_team").replace(" ", "")[4:]  # 转接车牌号

    if "快修" in care_of_team:  # 如果转接的班组信息中包含快修，那么肯定是快修班组，否则不处理
        # 快修完工转机电
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
        # 机电完工转快修
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
            oil_service = models.VehicleInfo.objects.get(wip=service_vehicle_wip).oil_service
            models.QuickServiceVehicle.objects.create(quick_service_team=pass_on_to_team, wip=service_vehicle_wip,
                                                      vehicle_num=vehicle_num, oil_service=oil_service)
    else:
        return JsonResponse({'status': False, "errors": '只有机电快修工序，才能互转车辆！其他工序不可！'})
    return JsonResponse({'status': True})


def add_dispatch_team(request):
    """增加项目派工操作"""
    dispatch_team = request.GET.get("dispatch_team").replace(" ", "").strip()  # 派工班组信息
    service_team = str(request.GET.get('veh_num')).replace(" ", "")[0:4]  # 提交班组名
    veh_num = str(request.GET.get('veh_num')).replace(" ", "")[4:]  # 车牌号
    oil_service = str(request.GET.get("oil_service")).replace(" ", "").strip()  # 获取机油保养信息
    # 1.根据信息，查询对应工序是否已经存在该信息，如果存在，则不允许派工（快修和机修）
    # 2.如果不存在，那么在对应的表中创建该车辆信息
    # 快修专机电，先在快修表获取车辆wip，然后去机电表查询是否存在

    if "机电" in dispatch_team and '机电' not in service_team:
        # 快修增项转机电
        quick_service_vehicle_wip = models.QuickServiceVehicle.objects.filter(
            quick_service_team=service_team, vehicle_num=veh_num).exclude(
            quick_service_status='完工交车').first().wip
        service_vehicle_info = models.ServiceVehicle.objects.filter(wip=quick_service_vehicle_wip)
        if service_vehicle_info.exists():
            return JsonResponse({'status': False, "errors": '该车辆信息，在被转工序存在，故不能转车，可修改车辆信息'})
        else:
            models.ServiceVehicle.objects.create(service_team=dispatch_team, wip=quick_service_vehicle_wip,
                                                 vehicle_num=veh_num)

    elif "快修" in dispatch_team and '快修' not in service_team:
        # 机电增项转快修
        service_vehicle_wip = models.ServiceVehicle.objects.filter(service_team=service_team,
                                                                   vehicle_num=veh_num).exclude(
            service_status='完工交车').first().wip
        quick_service_vehicle_info = models.QuickServiceVehicle.objects.filter(wip=service_vehicle_wip)
        if quick_service_vehicle_info.exists():
            return JsonResponse({'status': False, "errors": '该车辆信息，在被转工序存在，故不能转车，可修改车辆信息'})
        else:
            models.QuickServiceVehicle.objects.create(quick_service_team=dispatch_team, wip=service_vehicle_wip,
                                                      vehicle_num=veh_num, oil_service=oil_service)
    else:
        return JsonResponse({'status': False, "errors": '该车辆信息，在被转工序存在，故不能转车，可修改车辆信息'})
    return JsonResponse({'status': True})


def team_vehicle_info_view(request):
    """班组车辆信息查看功能"""
    team = request.GET.get('team').replace(" ", "").strip()
    data = {}
    if '快修' in team:
        team_vehicle_info = models.QuickServiceVehicle.objects.exclude(quick_service_status='完工交车').filter(
            quick_service_team=team)
        for veh_obj in team_vehicle_info:
            data[veh_obj.vehicle_num] = veh_obj.quick_service_status
    elif '机电' in team:
        team_vehicle_info = models.ServiceVehicle.objects.exclude(service_status='完工交车').filter(service_team=team)
        for veh_obj in team_vehicle_info:
            data[veh_obj.vehicle_num] = veh_obj.service_status
    else:
        data['该组别'] = "无车辆信息可以查看！"
    return JsonResponse({'status': True, 'data': data})

# ------  End 看板页面信息处理  ------------

# ------- Start 在场车辆信息处理 --------


@admin_permission
def unfinished(request):
    """在场车辆页面显示"""
    return render(request, 'unfinished.html')


def vehicle_info_edit(request):
    """车辆信息修改"""
    pass
