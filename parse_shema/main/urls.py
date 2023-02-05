from django.urls import path
# from rest_framework.routers import DefaultRouter

from main.views import ImageFrontView


app_name = 'api'


urlpatterns = [
    path('v1/save_point', ImageFrontView.as_view(), name='save_point')
]
