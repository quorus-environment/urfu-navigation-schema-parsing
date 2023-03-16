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
        self.result = [([100], "start")]
        self.res = []

    def call(self) -> bool:
        """Основной метод.

        Хз может нужно разделить, но можно оставить как один
        """
        self.__start_defind_office()
        print(len(self.array))
        print(len(self.result))
        with open('your_file.txt', 'w') as f:
            for line in self.result:
                f.write(f"{line}\n")
        print(self.res)
        return False

    def __start_defind_office(self) -> None:
        for line in self.array:
            tuple_result_in_line = self.__line_search(line)
            if (len(tuple_result_in_line[0]) != 0
                    or len(tuple_result_in_line[1]) != 0):
                self.__factory_office(tuple_result_in_line)

    def __line_search(self, line) -> None:
        red = []
        green = []
        for element in line:
            color = self.__defind_color(element)
            if color == "white":
                continue
            if color == "red":
                red.append(self.__defind_color(element))
            if color == "green":
                green.append(self.__defind_color(element))
        return (red, green)

    def __defind_color(self, array: np.ndarray) -> None:
        set_color = tuple(array)
        result = [(100, "start")]
        for i in range(len(self.ALL_COLORS)):
            try:
                result = self.ALL_COLORS[i][set_color]
                if result:
                    return result
            except Exception:
                continue
        return "unknown"

    def __factory_office(self, office_from_line) -> None:
        # TODO
        print(len(office_from_line))
        print("office_from_line", office_from_line)
        for office in office_from_line:
            if len(office) != 0 and office[1] != self.result[-1][1]:
                self.__save_office(office[0])

    def __get_or_create_university(self) -> models.Model:
        return 0

    def __save_office(self, office) -> None:
        self.res.append({"x": len(office), "y": len(office[0])})
