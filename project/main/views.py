from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.mixins import ListModelMixin

from main.utils import ImageProcessing


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
            ImageProcessing(file).call()
            return Response(
                "Координаты созданы успешно",
                status=status.HTTP_201_CREATED
            )
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
