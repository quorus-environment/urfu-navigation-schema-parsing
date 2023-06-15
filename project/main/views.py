from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from main.utils import SaveImageData, ReturnData


class ImageFrontView(APIView):
    """Получение изображения с фронта.

    - Запуск скрипта по изображению
    - Сохранение координат в бд
    - Отпарвка координат по всему данных из фотографии
    """

    def post(self, request):
        """Получение и сохранение данных по фотографии."""
        try:
            file = request.data['file'].read()
            status = SaveImageData(image=file).call()
            if not status["status"] == 200:
                return Response(
                    "Что-то пошло не так",
                    status=422
                )
            res = ReturnData()
            data = res.t_sections()
            return JsonResponse(data, safe=False)
        except KeyError:
            return Response(
                "В запросе отсутвует изоброжение",
                status=404
            )
