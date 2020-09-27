from django import template
from business.models import VehicleInfo
register = template.Library()

@register.simple_tag
def unfinished_messages():
    unfinished_messages_list = []
    unfinished_messages_dict = VehicleInfo.objects.exclude(service_status="完工交付")
    for msg in unfinished_messages_dict:
        unfinished_messages_list.append(msg)
    return unfinished_messages_list
