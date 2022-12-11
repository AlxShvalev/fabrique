from django.urls import include, path
from rest_framework import routers

from . import views

router_v1 = routers.DefaultRouter()
router_v1.register('clients', views.ClientViewSet, basename='clients')
router_v1.register('mailings', views.MailingViewSet, basename='mailings')
router_v1.register('messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
