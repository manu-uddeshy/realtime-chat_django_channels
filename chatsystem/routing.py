from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import path
from channels.auth import AuthMiddleware , AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

from chat.consmers import ChatConsumer 
application = ProtocolTypeRouter({
    # (http->django views is added by default) 
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    #path("users/", NewUserConsumer),
                    #url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer),
                    path("messages/<username>/", ChatConsumer),
                    
                ]
            )
        )
    )
})

#  ws://ourdomain/<username>