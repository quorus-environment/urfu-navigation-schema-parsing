from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from django.core import serializers
from django.http import JsonResponse

from main.models import (
    Body,
    Floor,
    Section,
    Neighbor,
    Hallway,
    Office
)
from main.utils import SaveImageData


class ImageFrontView(APIView):
    """Получение изображения с фронта.

    - Сохранение изображения ?
    - Запуск скрипта по изображению
    - Сохранение точек в бд
    - Отпарвка координат кабинета обратно ?
    - Или еще один эндпоинт get, который отдает все эти точки ?
    """

    def post(self, request):
        try:
            file = request.data['file'].read()
            SaveImageData(image=file).call()
            data = {
                "bodys": serializers.serialize("json", Body.objects.all()),
                "floors": serializers.serialize("json", Floor.objects.all()),
                "sections": serializers.serialize("json", Section.objects.all()),
                "neighbors": serializers.serialize("json", Neighbor.objects.all()),
                "hallways": serializers.serialize("json", Hallway.objects.all()),
                "offices": serializers.serialize("json", Office.objects.all())
            }
            return JsonResponse(data)
        except KeyError:
            return Response(
                "В запросе отсутвует изоброжение",
                status=status.HTTP_400_BAD_REQUEST
            )


# class OfficeViews(ListModelMixin):
#     """Вывод списка кабинетов.

#     Нужен для получения кабинетов университета.
#     Принмает в качетве параметра фильтр по университету.
#     Если нужно то и по секции.
#     """
#     pass
