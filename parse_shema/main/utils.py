"""Модуль обработки изоброжения с фронта.

Переводит изоброжение в массив, проходит по массиву изоброжения и
сиохраняет координаты координаты в БД.
"""
import cv2
import numpy as np


class ImageProcessing:
    """Класс обработки изображений."""
    def __init__(self, image) -> None:
        image = np.asarray(bytearray(image), dtype=np.uint8)
        # self.array - тут изображение в массиве numpy
        self.array = cv2.imdecode(image, cv2.IMREAD_COLOR)

    def call(self) -> bool:
        return False
