from django.urls import path, include
from rest_framework.routers import DefaultRouter

from main.views import ImageFrontView# , OfficeViews


app_name = 'api'

# router_v1 = DefaultRouter()
# router_v1.register("offices", OfficeViews, basename="offices")


urlpatterns = [
    path('v1/save_point', ImageFrontView.as_view(), name='save_point'),
    # path('v1/', include(router_v1.urls))
]
