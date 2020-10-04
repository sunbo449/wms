import random
from datetime import datetime
from business.models import VehicleInfo, QuickServiceVehicle, ServiceVehicle
from account import models
from business.models import VehicleInfo


def vehicle_info_validation(request):
    """车辆录入信息验证"""
    timer = datetime.now().strftime("%Y%m%d")
    vehicle_num = request.POST.get("vehicle_num").replace(" ", "").upper()
    wip = timer + str(request.POST.get("wip", "").replace(" ", ""))
    sa = request.POST.get("sa")
    estimate_finish_date = request.POST.get("estimate_finish_date")
    estimate_finish_time = request.POST.get("estimate_finish_time")
    accident_work_order = request.POST.get("accident_work_order")
    moto_work_order = request.POST.get("moto_work_order")
    oil_service = request.POST.get("oil_service")
    over_registration = request.POST.get("over_registration")
    quick_service_team = request.POST.get("quick_service_team")
    service_team = request.POST.get("service_team")
    service_project = request.POST.get("service_project")

    if len(vehicle_num) < 6 or len(vehicle_num) > 8:
        error_msg = "车牌号输入不正确"
        return error_msg

    # 如果输入发工单号重复了，那么不允许
    if VehicleInfo.objects.filter(wip=wip).exists():
        error_msg = '工单号重复了！'
        return error_msg

    # 如果没有输入工单号码，那么将会自动生成当前日期 + 随机四位数字的工单号，保证工单号的唯一性
    if wip == "":
        num = random.randint(11111, 99999)
        wip = timer + str(num)

    if sa == "":
        error_msg = "服务顾问不能为空"
        return error_msg

    if estimate_finish_date == "" or estimate_finish_time == "":
        error_msg = "交车时间不能为空"
        return error_msg

    VehicleInfo.objects.create(vehicle_num=vehicle_num, wip=wip, sa_id=sa, estimate_finish_date=estimate_finish_date,
                               estimate_finish_time=estimate_finish_time, actual_finish_date=estimate_finish_date,
                               actual_finish_time=estimate_finish_time, accident_work_order=accident_work_order,
                               moto_work_order=moto_work_order, oil_service=oil_service,
                               over_registration=over_registration, quick_service_team_id=quick_service_team,
                               service_team_id=service_team, service_project_id=service_project)

    # 当维修班组不为空的时候，说明有该班组的项目，那么就会同时创建该班组的维修信息
    if quick_service_team != "":
        """创建快修车辆信息"""
        quick_service_team = models.Team.objects.filter(id=quick_service_team).first().caption
        QuickServiceVehicle.objects.create(vehicle_num=vehicle_num, wip=wip, quick_service_team=quick_service_team,
                                           oil_service=oil_service)

    if service_team != "":
        """创建机电车辆信息"""
        service_team = models.Team.objects.filter(id=service_team).first().caption
        ServiceVehicle.objects.create(vehicle_num=vehicle_num, wip=wip, service_team=service_team)

    success = True
    return success


def vehicle_info_edit_validation(request):
    """车辆信息修改验证与操作"""
    veh_num = request.POST.get('veh_number')
