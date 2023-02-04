from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
