from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from wms import consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path("spectaculars/<group_id>", consumers.SpectacularsConsumers)
    ])
})
