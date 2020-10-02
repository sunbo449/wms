"""
本文件： 处理车辆状态函数，由于车辆状态处理较为繁琐，统一集中在这个文件中进行处理
    # 1.如果提交的数据是转工序，那么获取到的是状态是被转的班组的名称
    # 2.如果获取的是班组名称，那么判断该班组内是否有这台车，如果有直接返回Js数据，告知已经存在，如果没有那么创建信息，并且返回Js数据
    # 3.同时车辆维修状态也要改成正常维修的状态
"""
from business import models
from django.http import JsonResponse

class ServiceStatusEdit:
    """封装操作车辆维修状态"""

    def __init__(self, request, service_team, veh_num, veh_status):
        self.request = request
        self.service_team = service_team
        self.veh_num = veh_num
        self.veh_status = veh_status
        self.service_status_edit()
        self.vehicle_finish()

    # 车辆状态修改，进行数据匹配，检查快修和机电班组符合条件的车辆，然后将状态更改为用户提交的状态
    def service_status_edit(self):
        try:
            quick_service_status = models.QuickServiceVehicle.objects.filter(vehicle_num=self.veh_num,
                                                                             quick_service_team=self.service_team).exclude(
                quick_service_status='完工交车')
            if quick_service_status.exists():
                quick_service_wip = quick_service_status.first().wip
                veh_message = models.QuickServiceVehicle.objects.get(wip=quick_service_wip)
                veh_message.quick_service_status = self.veh_status
                veh_message.save()
                self.vehicle_road_test(quick_service_wip)
                self.vehicle_fqc(quick_service_wip)

            service_status = models.ServiceVehicle.objects.filter(vehicle_num=self.veh_num,
                                                                  service_team=self.service_team).exclude(
                service_status='完工交车')
            if service_status.exists():
                service_wip = service_status.first().wip
                print(service_wip)
                veh_message = models.ServiceVehicle.objects.get(wip=service_wip)
                veh_message.service_status = self.veh_status
                veh_message.save()
                self.vehicle_road_test(service_wip)
                self.vehicle_fqc(service_wip)
        except Exception as e:
            print('错误')

    def vehicle_road_test(self, wip):
        """车辆路试状态操作"""
        # 1. 维修技师每次点击选择车辆路试的状态的时候，都会在路试模型中创建一条路试信息
        if self.veh_status == "车辆路试":
            models.VehicleRoadTest.objects.create(vehicle_num=self.veh_num, driver=self.request.wms[0],
                                                  service_team=self.service_team, wip=wip)

    def vehicle_fqc(self, wip):
        """车辆终检操作"""
        if self.veh_status == "车辆终检":
            models.FQC.objects.create(vehicle_num=self.veh_num, inspector=self.request.wms[0],
                                      service_team=self.service_team, wip=wip)

    def vehicle_finish(self):
        """终检环节"""
        fqc_vehicle = models.FQC.objects.filter(vehicle_num=self.veh_num).exclude(service_status='完工交车')
        if fqc_vehicle.exists():
            if self.veh_status == "完工交车":
                fqc_wip = fqc_vehicle.first().wip
                fqc_vehicle_status = models.FQC.objects.get(wip=fqc_wip)
                fqc_vehicle_status.service_status = self.veh_status
                fqc_vehicle_status.save()

                quick_service_fqc_vehicle = models.QuickServiceVehicle.objects.filter(wip=fqc_wip,
                                                                                      quick_service_status='车辆终检')
                print(quick_service_fqc_vehicle)
                if quick_service_fqc_vehicle.exists():
                    print(quick_service_fqc_vehicle.exists())
                    q_wip = quick_service_fqc_vehicle.first().wip
                    veh_message = models.QuickServiceVehicle.objects.get(wip=q_wip)
                    veh_message.quick_service_status = self.veh_status
                    veh_message.save()

                service_fqc_vehicle = models.ServiceVehicle.objects.filter(wip=fqc_wip, service_status='车辆终检')
                if service_fqc_vehicle.exists():
                    s_wip = service_fqc_vehicle.first().wip
                    veh_message = models.ServiceVehicle.objects.get(wip=s_wip)
                    veh_message._service_status = self.veh_status
                    veh_message.save()

