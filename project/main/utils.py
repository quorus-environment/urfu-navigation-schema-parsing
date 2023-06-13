import cv2
import numpy as np
import math
from typing import Dict, List
import datetime
import json

from main.models import (
    Floor,
    Office,
    Neighbor,
    Section,
    Hallway,
    Body,
    EntryPoint
)


class DefinitionObjects:
    """Определние объектов c помшью cv2."""
    RGB_OBJ = {
        "entry_point": [[0, 120, 255], [2, 125, 255]],
        "sections": [[35, 80, 230], [40, 90, 240]],
        "hellway": [[215, 155, 95], [222, 165, 105]],
        "office_one": [[100, 225, 135], [104, 231, 140]],
        "office_two": [[54, 135, 75], [60, 145, 85]]
    }

    def __init__(self, image) -> None:
        image = np.asarray(bytearray(image), dtype="uint8")
        self.img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    def defind_entry_point(self) -> tuple:
        """Определение точки входа в секцию"""
        lower = np.array(self.RGB_OBJ["entry_point"][0])
        upper = np.array(self.RGB_OBJ["entry_point"][1])
        mask = cv2.inRange(self.img, lower, upper)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def defind_sections(self) -> tuple:
        """Определение секции"""
        lower = np.array(self.RGB_OBJ["sections"][0])
        upper = np.array(self.RGB_OBJ["sections"][1])
        mask = cv2.inRange(self.img, lower, upper)
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        return contours

    def defind_angel_section(self, contours: tuple) -> int:
        rect = cv2.minAreaRect(contours)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        edge1 = np.int0((box[1][0] - box[0][0], box[1][1] - box[0][1]))
        edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))

        usedEdge = edge1
        if cv2.norm(edge2) > cv2.norm(edge1):
            usedEdge = edge2
        reference = (1, 0)

        angle = 180.0 / math.pi * math.acos(
            (reference[0] * usedEdge[0] + reference[1] * usedEdge[1])
            / (cv2.norm(reference) * cv2.norm(usedEdge))
        )
        return angle

    def defind_hellways(self) -> tuple:
        """Определние коридора."""
        lower = np.array(self.RGB_OBJ["hellway"][0])
        upper = np.array(self.RGB_OBJ["hellway"][1])
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
        """Определние офисов."""
        lower = np.array(self.RGB_OBJ["office_one"][0])
        upper = np.array(self.RGB_OBJ["office_one"][1])
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
        """Определние офисов."""
        lower = np.array(self.RGB_OBJ["office_two"][0])
        upper = np.array(self.RGB_OBJ["office_two"][1])
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
    def t_sections(self) -> Dict:
        res = []
        for obj in Section.objects.all():
            res.append({
                "id": obj.pk,
                "auds": self.__auds_section(obj),
                "corridor": self.__vectors_obj(obj.hallway),
                "position": obj.position,
                "floor": obj.floor.name,
                "entry_points": self.__enty_points(obj),
                "neighbors": list(obj.neighbors.all().values())
            })
        return json.dumps(res, default=self.__default)

    def __default(self, o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    def __auds_section(self, section: Section) -> List[Dict]:
        res = []
        for obj in section.offices.all():
            res.append(
                {
                    "id": obj.pk,
                    "vectors": self.__vectors_obj(obj),
                    "startPoint": {"x": obj.x, "y": obj.y},
                    "section": obj.section.pk
                }
            )
        return res

    def __enty_points(self, section: Section) -> List[Dict]:
        """Точки входа в секции."""
        res = []
        for obj in section.entry_points.all():
            res.append(
                {
                    "id": obj.pk,
                    "vectors": self.__vectors_obj(obj),
                    "section": obj.section.pk
                }
            )
        return res

    def __vectors_obj(self, obj) -> List[Dict]:
        x, y, w, h = int(obj.x), int(obj.y), int(obj.w), int(obj.h)
        return [
            [
                {
                    "x": x,
                    "y": y
                },
                {
                    "x": x,
                    "y": y + h
                },
            ],
            [
                {
                    "x": x,
                    "y": y + h
                },
                {
                    "x": x + w,
                    "y": y + h
                },
            ],
            [
                {
                    "x": x + w,
                    "y": y + h
                },
                {
                    "x": x + w,
                    "y": y
                },
            ],
            [
                {
                    "x": x + w,
                    "y": y
                },
                {
                    "x": x,
                    "y": y
                },
            ]
        ]


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
        self.entry_points = self.image_proccessing.defind_entry_point()
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
            angel = self.image_proccessing.defind_angel_section(section)
            type_position = self.__type_position_section(angel)
            s_data = {
                "x": x,
                "y": y,
                "w": w,
                "h": h
            }
            self.__save_section(type_position)
            list_s_data.append([self.section, (x, y, w, h)])
            self.__data_inside_section(s_data)
        self.__set_neighbor(list_s_data)

    def __type_position_section(self, angel: float) -> str:
        angel = int(angel)
        if angel >= 45 and angel < 135:
            return Section.VERTICALLY
        return Section.HORIZONTALLY

    def __save_section(self, type_position: str) -> None:
        """Сохранение секции в бд и в переменную класса.

        Так как секций может быть несколько
        на след. итерации здесь будет другая секция.
        Через нее сохранение помещений c section=self.sections.
        """
        self.section = Section.objects.create(
            floor=self.floor,
            body=self.body,
            position=type_position
        )

    def __data_inside_section(self, s_data: Dict[str, int]) -> None:
        """Сохраняем данные внутри секции"""
        self.__save_entry_points(s_data)
        self.__save_hallways(s_data)

    def __save_entry_points(self, s_data: Dict[str, int]) -> None:
        """Сохранение данных точки входа в секцию"""
        for entry_point in self.entry_points:
            x, y, w, h = cv2.boundingRect(entry_point)
            obj = {
                "x": x,
                "y": y,
                "w": w,
                "h": h
            }
            if not self.__is_in_section(s_data, obj):
                continue
            EntryPoint.objects.create(
                section=self.section,
                x=obj["x"],
                y=obj["y"],
                w=obj["w"],
                h=obj["h"]
            )

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
        rect1_bottom = rect1[1] + rect1[3]
        rect1_left = rect1[0]
        rect1_right = rect1[0] + rect1[2]
        rect2_top = rect2[1]
        rect2_bottom = rect2[1] + rect2[3]
        rect2_left = rect2[0]
        rect2_right = rect2[0] + rect2[2]
        if ((rect1_top == rect2_bottom or rect1_bottom == rect2_top)
                and rect1_left < rect2_right and rect1_right > rect2_left):
            return True
        elif ((rect1_left == rect2_right or rect1_right == rect2_left)
                and rect1_top < rect2_bottom and rect1_bottom > rect2_top):
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
        if self.__is_office_adjacent_to_hallway(rect1, rect2):
            return True
        rect1_tl = (rect1[0], rect1[1])
        rect1_tr = (rect1[0] + rect1[2], rect1[1])
        rect1_bl = (rect1[0], rect1[1] + rect1[3])
        # rect1_br = (rect1[0] + rect1[2], rect1[1] + rect1[3])
        rect2_tl = (rect2[0], rect2[1])
        rect2_tr = (rect2[0] + rect2[2], rect2[1])
        rect2_bl = (rect2[0], rect2[1] + rect2[3])
        # rect2_br = (rect2[0] + rect2[2], rect2[1] + rect2[3])
        if (rect1_tl[0] <= rect2_tl[0] <= rect1_tr[0] or rect1_tl[0] <= rect2_tr[0] <= rect1_tr[0]) and (rect1_tl[1] <= rect2_tl[1] <= rect1_bl[1] or rect1_tl[1] <= rect2_bl[1] <= rect1_bl[1]):
            return True
        elif (rect2_tl[0] <= rect1_tl[0] <= rect2_tr[0] or rect2_tl[0] <= rect1_tr[0] <= rect2_tr[0]) and (rect2_tl[1] <= rect1_tl[1] <= rect2_bl[1] or rect2_tl[1] <= rect1_bl[1] <= rect2_bl[1]):
            return True
        return False

    def __result_hash(self, status: int) -> dict:
        return {
            "status": status
        }

    def __set_image_proccessing(self) -> None:
        self.image_proccessing = DefinitionObjects(image=self.image)
