from django.urls import path
from main.views import (
    ImageFrontView
)


app_name = 'api'

urlpatterns = [
    path('v1/save_point', ImageFrontView.as_view(), name='save_point')
]
