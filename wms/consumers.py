from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
import json
from django.db.models import Q
from asgiref.sync import async_to_sync
from business import models


class SpectacularsConsumers(WebsocketConsumer):
    def websocket_connect(self, message):
        """服务端接收连接"""
        group_id = self.scope['url_route']['kwargs'].get('group_id')
        self.accept()
        async_to_sync(self.channel_layer.group_add)(group_id, self.channel_name)

    def websocket_receive(self, message):
        """客户端浏览器向服务端发送消息，此方法触发"""
        veh_obj_dict = {}
        group_id = self.scope['url_route']['kwargs'].get('group_id')
        # 获取快修班组车辆数据
        quick_service_veh_obj = models.QuickServiceVehicle.objects.exclude(
            Q(quick_service_status='完工交车') | Q(quick_service_status='暂停等件') | Q(quick_service_status='车辆终检'))
        service_veh_obj = models.ServiceVehicle.objects.exclude(
            Q(service_status='完工交车') | Q(service_status='暂停等件') | Q(service_status='车辆终检'))
        vehicle_road_test_obj = models.VehicleRoadTest.objects.exclude(service_status='结束路试')
        fqc_vehicle_obj = models.FQC.objects.exclude(service_status='完工交车')

        quick_1_list = []
        quick_2_list = []
        quick_1_status_list = []
        quick_2_status_list = []
        for veh_obj in quick_service_veh_obj:
            if veh_obj.quick_service_team == "快修一组":
                quick_1_list.append(veh_obj.vehicle_num)
                quick_1_status_list.append(veh_obj.quick_service_status)
            elif veh_obj.quick_service_team == "快修二组":
                quick_2_list.append(veh_obj.vehicle_num)
                quick_2_status_list.append(veh_obj.quick_service_status)
        quick_lis_1 = dict(zip(quick_1_list, quick_1_status_list))
        quick_lis_2 = dict(zip(quick_2_list, quick_2_status_list))
        veh_obj_dict['快修一组'] = quick_lis_1
        veh_obj_dict['快修二组'] = quick_lis_2
        service_1_list = []
        service_2_list = []
        service_3_list = []
        service_4_list = []
        service_5_list = []
        service_6_list = []
        service_1_status_list = []
        service_2_status_list = []
        service_3_status_list = []
        service_4_status_list = []
        service_5_status_list = []
        service_6_status_list = []
        for service_obj in service_veh_obj:
            if service_obj.service_team == "机电一组":
                service_1_list.append(service_obj.vehicle_num)
                service_1_status_list.append(service_obj.service_status)

            if service_obj.service_team == "机电二组":
                service_2_list.append(service_obj.vehicle_num)
                service_2_status_list.append(service_obj.service_status)

            if service_obj.service_team == "机电三组":
                service_3_list.append(service_obj.vehicle_num)
                service_3_status_list.append(service_obj.service_status)

            if service_obj.service_team == "机电四组":
                service_4_list.append(service_obj.vehicle_num)
                service_4_status_list.append(service_obj.service_status)

            if service_obj.service_team == "机电五组":
                service_5_list.append(service_obj.vehicle_num)
                service_5_status_list.append(service_obj.service_status)

            if service_obj.service_team == "机电六组":
                service_6_list.append(service_obj.vehicle_num)
                service_6_status_list.append(service_obj.service_status)

        service_1_veh_list = dict(zip(service_1_list, service_1_status_list))
        service_2_veh_list = dict(zip(service_2_list, service_2_status_list))
        service_3_veh_list = dict(zip(service_3_list, service_3_status_list))
        service_4_veh_list = dict(zip(service_4_list, service_4_status_list))
        service_5_veh_list = dict(zip(service_5_list, service_5_status_list))
        service_6_veh_list = dict(zip(service_6_list, service_6_status_list))

        veh_obj_dict['机电一组'] = service_1_veh_list
        veh_obj_dict['机电二组'] = service_2_veh_list
        veh_obj_dict['机电三组'] = service_3_veh_list
        veh_obj_dict['机电四组'] = service_4_veh_list
        veh_obj_dict['机电五组'] = service_5_veh_list
        veh_obj_dict['机电六组'] = service_6_veh_list

        road_obj_list = []
        road_status_list = []
        for road_test_obj in vehicle_road_test_obj:
            road_obj_list.append(road_test_obj.vehicle_num)
            road_status_list.append(road_test_obj.service_status)
        road_test_status_list = dict(zip(road_obj_list, road_status_list))
        veh_obj_dict['车辆路试'] = road_test_status_list

        fqc_vehicle_obj_list = []
        fqc_vehicle_obj_status_list = []
        for fqc_obj in fqc_vehicle_obj:
            fqc_vehicle_obj_list.append(fqc_obj.vehicle_num)
            fqc_vehicle_obj_status_list.append(fqc_obj.service_status)
        fqc_obj_list = dict(zip(fqc_vehicle_obj_list, fqc_vehicle_obj_status_list))
        veh_obj_dict['车辆终检'] = fqc_obj_list

        async_to_sync(self.channel_layer.group_send)(group_id, {'type': 'my.send',
                                                                'message': {'code': 'init', 'data': veh_obj_dict}})

    def my_send(self, event):
        message = event['message']
        self.send(json.dumps(message))

    def websocket_disconnect(self, message):
        """客户端主动断开连接，服务端抛出一个停止连接的异常"""
        group_id = self.scope['url_route']['kwargs'].get('group_id')
        async_to_sync(self.channel_layer.group_discard)(group_id, self.channel_name)
        raise StopConsumer()
