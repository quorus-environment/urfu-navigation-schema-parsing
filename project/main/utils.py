import cv2
import numpy as np
import json
from typing import Dict, List

from main.models import (
    Floor,
    Office,
    Neighbor,
    Section,
    Hallway,
    Body
)


class DefinitionObjects:
    """Определние объектов c помшью cv2."""

    def __init__(self, image) -> None:
        image = np.asarray(bytearray(image), dtype="uint8")
        self.img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    def defind_sections(self) -> tuple:
        lower = np.array([37, 84, 234])
        upper = np.array([37, 84, 234])
        mask = cv2.inRange(self.img, lower, upper)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def defind_hellways(self) -> tuple:
        lower = np.array([218, 161, 99])
        upper = np.array([218, 161, 99])
        mask = cv2.inRange(self.img, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def defind_offices_one(self) -> tuple:
        lower = np.array([100, 230, 137])
        upper = np.array([104, 231, 138])
        mask = cv2.inRange(self.img, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def defind_offices_two(self) -> tuple:
        lower = np.array([58, 139, 79])
        upper = np.array([58, 139, 79])
        mask = cv2.inRange(self.img, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours


class ReturnData:
    def __init__(self) -> None:
        self.auditoriums = self.__auditoriums()
        self.graphs = self.__graphs()

    def __auditoriums(self) -> Dict:
        return {

        }

    def graphs(self, ) -> Dict:
        return {

        }

    def json(self):
        res = {
            "auditoriums": self.auditoriums,
            "graphs": self.graphs
        }
        return json.dumps(res)


class SaveImageData:
    """Сохранение найденных объектов в базу."""
    image_proccessing: DefinitionObjects

    def __init__(self, image, floor="0") -> None:
        self.image = image
        self.floor = floor
        self.__set_image_proccessing()

    def call(self) -> dict:
        self.__set_data()
        self.__save_data()
        return self.__result_hash(status=200)

    def __set_data(self) -> None:
        self.sections = self.image_proccessing.defind_sections()
        self.hallways = self.image_proccessing.defind_hellways()
        self.offices_one = self.image_proccessing.defind_offices_one()
        self.offices_two = self.image_proccessing.defind_offices_two()

    def __save_data(self) -> None:
        self.body = Body.objects.create(name="Test_body")
        self.floor = Floor.objects.create(name="TEst", body=self.body)
        list_s_data = []
        for section in self.sections:
            x, y, w, h = cv2.boundingRect(section)
            s_data = {
                "x": x,
                "y": y,
                "w": w,
                "h": h
            }
            self.__save_section()
            list_s_data.append([self.section, (x, y, w, h)])
            self.__data_inside_section(s_data)
        self.__set_neighbor(list_s_data)

    def __save_section(self) -> None:
        """Сохранение секции в бд и в переменную класса.

        Так как секций может быть несколько
        на след. итерации здесь будет другая секция.
        Через нее сохранение помещений c section=self.sections.
        """
        self.section = Section.objects.create(floor=self.floor, body=self.body)

    def __data_inside_section(self, s_data: Dict[str, int]) -> None:
        self.__save_hallways(s_data)

    def __save_hallways(self, s_data: Dict[str, int]) -> None:
        for hallway in self.hallways:
            x, y, w, h = cv2.boundingRect(hallway)
            obj = {
                "x": x,
                "y": y,
                "w": w,
                "h": h
            }
            if not self.__is_in_section(s_data, obj):
                continue
            Hallway.objects.create(
                section=self.section,
                x=obj["x"],
                y=obj["y"],
                w=obj["w"],
                h=obj["h"]
            )
            self.__save_offices((x, y, w, h))

    def __save_offices(self, rect2_hallway: List[int]) -> None:
        list_offices = [
            self.offices_one,
            self.offices_two
        ]
        for offices in list_offices:
            self.__save_one_type_office(
                offices,
                rect2_hallway
            )

    def __save_one_type_office(
            self, offices: tuple, rect2: List[int]) -> None:
        for office in offices:
            rect1 = cv2.boundingRect(office)
            if not self.__is_office_adjacent_to_hallway(rect1, rect2):
                continue
            Office.objects.create(
                section=self.section,
                name="Name",
                x=rect1[0],
                y=rect1[1],
                w=rect1[2],
                h=rect1[3]
            )

    def __is_in_section(
            self, s_data: Dict[str, int], obj: Dict[str, int]) -> bool:
        return bool(
            s_data["x"] <= obj["x"]
            and obj["x"] + obj["w"] <= s_data["x"] + s_data["w"]
            and s_data["y"] <= obj["y"]
            and obj["y"] + obj["h"] <= s_data["y"] + s_data["h"]
        )
    
    def __is_office_adjacent_to_hallway(
            self, rect1: List[int], rect2: List[int]) -> bool:
        rect1_top = rect1[1]
        rect1_bottom = rect1[1]+rect1[3]
        rect1_left = rect1[0]
        rect1_right = rect1[0]+rect1[2]
        rect2_top = rect2[1]
        rect2_bottom = rect2[1]+rect2[3]
        rect2_left = rect2[0]
        rect2_right = rect2[0]+rect2[2]
        if ((rect1_top == rect2_bottom or rect1_bottom == rect2_top) and
                rect1_left < rect2_right and rect1_right > rect2_left):
            return True
        elif ((rect1_left == rect2_right or rect1_right == rect2_left) and
                rect1_top < rect2_bottom and rect1_bottom > rect2_top):
            return True
        return False

    def __set_neighbor(self, data) -> None:
        for i in range(len(data) - 1):
            one = data[i]
            two = data[i + 1]
            if not self.__is_neighbor(one[1], two[1]):
                continue
            Neighbor.objects.create(section=one[0], neighbor_id=two[0].id)
            Neighbor.objects.create(section=two[0], neighbor_id=one[0].id)

    def __is_neighbor(self, rect1, rect2) -> bool:
        rect1_top = rect1[1]
        rect1_bottom = rect1[1] + rect1[3]
        rect1_left = rect1[0]
        rect1_right = rect1[0] + rect1[2]
        rect2_top = rect2[1]
        rect2_bottom = rect2[1] + rect2[3]
        rect2_left = rect2[0]
        rect2_right = rect2[0] + rect2[2]        
        if (rect1_left <= rect2_left <= rect1_right and 
                rect1_top <= rect2_top <= rect1_bottom and
                rect1_left <= rect2_right <= rect1_right and
                rect1_top <= rect2_bottom <= rect1_bottom and 
                self.__is_office_adjacent_to_hallway(rect1, rect2)):
            return True
        return False

    def __result_hash(self, status: int) -> dict:
        return {
            "status": status
        }

    def __set_image_proccessing(self) -> None:
        self.image_proccessing = DefinitionObjects(image=self.image)
