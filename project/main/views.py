import json

from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from main.utils import SaveImageData, ReturnData


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
            status = SaveImageData(image=file).call()
            if not status["status"] == 200:
                return Response(
                    "Что-то пошло не так",
                    status=status.HTTP_400_BAD_REQUEST
                )
            res = ReturnData()
            data = res.t_sections()
            return JsonResponse(data, safe=False)
        except KeyError:
            return Response(
                "В запросе отсутвует изоброжение",
                status=status.HTTP_400_BAD_REQUEST
            )
