from django.contrib.auth import views
from django.urls import path, re_path


from .views import ThreadView, OnlineUsers
#from django.contrib.auth import  views as auth_views

app_name = 'chat'

urlpatterns = [
    path("", OnlineUsers, name="online"),
    #re_path(r"^(?P<username>[\w.@+-]+)", ThreadView.as_view(),name='second'),
    path("<username>/", ThreadView.as_view(),name='second'),
]
