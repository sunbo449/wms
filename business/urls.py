from os import name
from django.urls import path
from business.views import process_control, dp

app_name = 'business'

urlpatterns = [
    path("vehicle_info", process_control.vehicle_info, name="vehicle_info"),  # 信息录入
    path('spectaculars', process_control.spectaculars, name="spectaculars"),  # 动态看板
    path("vehicle_status_edit", process_control.vehicle_status_edit, name="vehicle_status_edit"),  # 车辆状态操作
    path("vehicle_road_status_edit", process_control.vehicle_road_status_edit, name="vehicle_road_status_edit"),  # 路试
    path("vehicle_care_of", process_control.vehicle_care_of, name="vehicle_care_of"),   # 车辆转接操作
    path('unfinished', process_control.unfinished, name='unfinished'),   # 未完成在场车辆
    path('data_report', dp.data_report, name="data_report"),  # 数据报表
    path("", process_control.index, name='index'),   # 首页
]
