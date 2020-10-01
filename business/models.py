from django.db import models
from account.models import Team, UserProfile


# Create your models here.


class ServiceProject(models.Model):
    """维修项目"""
    caption = models.CharField(max_length=40, verbose_name="维修项目")

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = "维修项目表"
        verbose_name_plural = verbose_name


class VehicleInfo(models.Model):
    """车辆信息"""
    vehicle_num = models.CharField(max_length=20, verbose_name="车牌号码", db_index=True)
    wip = models.CharField(max_length=20, verbose_name="工单号码", null=True, blank=True, db_index=True)
    sa = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="服务顾问")
    register_date = models.DateField(auto_now_add=True, verbose_name="登记日期")
    register_time = models.TimeField(auto_now_add=True, verbose_name="登记时间")
    estimate_finish_date = models.DateField(auto_now_add=True, verbose_name="预计完成日期")
    estimate_finish_time = models.TimeField(auto_now_add=True, verbose_name="预计完成时间")
    actual_finish_date = models.DateField(auto_now=True, verbose_name="实际完成日期")
    actual_finish_time = models.TimeField(auto_now=True, verbose_name="实际完成时间")
    accident_work_order = models.CharField(max_length=10, verbose_name="事故维修工单")
    moto_work_order = models.CharField(max_length=10, verbose_name="摩托维修工单")
    oil_service = models.CharField(max_length=10, verbose_name="机油保养")
    over_registration = models.CharField(max_length=10, verbose_name="重复进场工单")
    quick_service_team = models.ForeignKey(Team, related_name="quick_service", db_column="快修班组",
                                           on_delete=models.CASCADE, verbose_name="快修班组", null=True, blank=True)
    quick_service_status = models.CharField(max_length=32, default="正在维修", verbose_name="快修维修状态")
    service_team = models.ForeignKey(Team, related_name="service_team", db_column="机电班组", on_delete=models.CASCADE,
                                     verbose_name="机电班组", null=True, blank=True)
    service_project = models.ForeignKey(ServiceProject, on_delete=models.CASCADE, verbose_name="维修项目", null=True,
                                        blank=True)
    service_status = models.CharField(max_length=32, default="正常维修", verbose_name="机电维修状态")

    def __str__(self):
        return self.vehicle_num

    class Meta:
        verbose_name = "车辆信息表"
        verbose_name_plural = verbose_name


class QuickServiceVehicle(models.Model):
    """快修车辆信息"""
    vehicle_num = models.CharField(max_length=32, verbose_name="车牌号码", db_index=True)
    wip = models.CharField(max_length=32, verbose_name="工单号", db_index=True)
    quick_service_team = models.CharField(max_length=32, verbose_name="快修班组", null=True, blank=True)
    oil_service = models.CharField(max_length=10, verbose_name="机油保养")
    quick_service_status = models.CharField(
        max_length=32, default="正常维修", verbose_name="维修状态", db_index=True)
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name="开始日期")
    finish_time = models.DateTimeField(
        auto_now=True, verbose_name="完工时间")

    def __str__(self):
        return self.vehicle_num

    class Meta:
        verbose_name = "快修车辆信息表"
        verbose_name_plural = verbose_name


class ServiceVehicle(models.Model):
    """机电车辆信息"""
    vehicle_num = models.CharField(max_length=32, verbose_name="车牌号码", db_index=True)
    wip = models.CharField(max_length=32, verbose_name="工单号", db_index=True)
    service_team = models.CharField(max_length=32, verbose_name="机电班组", null=True, blank=True)
    service_status = models.CharField(
        max_length=32, default="正常维修", verbose_name="维修状态", db_index=True)
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name="开始日期")
    finish_time = models.DateTimeField(
        auto_now=True, verbose_name="完工时间")

    def __str__(self):
        return self.vehicle_num

    class Meta:
        verbose_name = "机电车辆信息表"
        verbose_name_plural = verbose_name


class VehicleRoadTest(models.Model):
    """车辆路试信息"""
    driver = models.CharField(max_length=32, verbose_name='试车司机', null=True, blank=True)
    wip = models.CharField(max_length=32, verbose_name="工单号", null=True, blank=True)
    vehicle_num = models.CharField(max_length=32, verbose_name="车牌号码", db_index=True)
    service_team = models.CharField(max_length=32, verbose_name="维修班组", db_index=True)
    service_status = models.CharField(
        max_length=32, default="车辆路试", verbose_name="维修状态", db_index=True)
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name="开始时间")
    finish_time = models.DateTimeField(
        auto_now=True, verbose_name="结束时间")

    def __str__(self):
        return self.vehicle_num

    class Meta:
        verbose_name = "路试车辆信息表"
        verbose_name_plural = verbose_name


class FQC(models.Model):
    """车辆终检信息"""
    inspector = models.CharField(max_length=32, verbose_name="质检员", null=True, blank=True)
    wip = models.CharField(max_length=32, verbose_name="工单号", null=True, blank=True)
    vehicle_num = models.CharField(max_length=32, verbose_name="车牌号码", db_index=True)
    service_team = models.CharField(max_length=32, verbose_name="维修班组", db_index=True)
    service_status = models.CharField(
        max_length=32, default="车辆终检", verbose_name="维修状态", db_index=True)
    start_time = models.DateTimeField(
        auto_now_add=True, verbose_name="开始时间")
    finish_time = models.DateTimeField(
        auto_now=True, verbose_name="结束时间")
