"""Модуль обработки изоброжения с фронта.

Переводит изоброжение в массив, проходит по массиву изоброжения и
сиохраняет координаты координаты в БД.
"""
from typing import Tuple, Dict

from django.db import models
import cv2
import numpy as np


class ImageProcessing:
    """Класс обработки изображений."""

    # TODO - сделать изображение с этими цветами для теста
    ALL_COLORS: Tuple[Dict[Tuple[int, int, int], int]] = (
        {(255, 255, 255): "white"},
        {(255, 0, 0): "red"},
        {(0, 255, 0): "green"},
        {(255, 255, 0): "yellow"}
    )

    def __init__(self, image) -> None:
        image = np.asarray(bytearray(image), dtype=np.uint8)
        # self.array - тут изображение в массиве numpy
        self.array = cv2.imdecode(image, cv2.IMREAD_COLOR)

    def call(self) -> bool:
        """Основной метод.

        Хз может нужно разделить, но можно оставить как один
        """
        self.__start_defind_office()
        print(len(self.array))
        print(len(self.result))
        return False

    def __start_defind_office(self) -> None:
        for line in self.array:
            self.__line_search(line)
        return False

    def __line_search(self, line) -> None:
        self.result = []
        for element in line:
            color = self.__defind_color(element)
            if color == "white":
                continue
            elif color == "":
                self.result.append(self.__defind_color(element))

    def __defind_color(self, array: np.ndarray) -> None:
        set_color = tuple(array)
        result = None
        for i in range(len(self.ALL_COLORS)):
            try:
                result = self.ALL_COLORS[i][set_color]
            except Exception:
                continue
        if not result:
            return "unknown"
        return result

    def __get_or_create_university(self) -> models.Model:
        return 0
