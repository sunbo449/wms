from django.contrib import admin
from business import models
# Register your models here.

@admin.register(models.ServiceProject)
class ServiceProjectAdmin(admin.ModelAdmin):
    list_display = ('id', "caption")


@admin.register(models.VehicleInfo)
class VehicleInfoAdmin(admin.ModelAdmin):
    list_display = ('id', "vehicle_num", "wip", "sa", "register_time", "estimate_finish_time", "actual_finish_time",
                    "accident_work_order", "moto_work_order", "oil_service", "over_registration", "quick_service_team",
                    "service_team", "service_project")

@admin.register(models.QuickServiceVehicle)
class QuickServiceVehicleInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_num', 'quick_service_status')
