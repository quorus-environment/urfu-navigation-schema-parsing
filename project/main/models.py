"""Основные модели.

Университеты, секции, кабинеты.
"""
from django.db import models


class Body(models.Model):
    """Сущность корпуса"""

    name = models.CharField(
        "Название",
        max_length=100
    )

    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Floor(models.Model):
    """Сущность этажа"""
    body = models.ForeignKey(
        Body,
        on_delete=models.CASCADE,
        related_name="floors"
    )

    name = models.CharField(
        "Название",
        max_length=100
    )

    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Section(models.Model):
    """Сущность секций"""
    floor = models.ForeignKey(
        Floor,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    body = models.ForeignKey(
        Body,
        on_delete=models.CASCADE,
        related_name="sections"
    )
    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Neighbor(models.Model):
    """Соседи для секций"""
    neighbor_id = models.IntegerField()
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="neighbors",
    )
    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Hallway(models.Model):
    """Коридор"""

    section = models.OneToOneField(
        Section,
        on_delete=models.CASCADE,
        primary_key=True
    )
    x = models.CharField(
        "X",
        max_length=20
    )
    y = models.CharField(
        "Y",
        max_length=20
    )
    w = models.CharField(
        "W",
        max_length=20
    )
    h = models.CharField(
        "H",
        max_length=20
    )

    x_end = models.CharField(
        "X_end",
        max_length=20
    )

    y_end = models.CharField(
        "Y_end",
        max_length=20
    )

    height = models.CharField(
        "height",
        max_length=20
    )

    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)


class Office(models.Model):
    """Сущность кабинетов"""
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="offices"
    )
    name = models.CharField(
        "Название",
        max_length=50
    )
    x = models.CharField(
        "X",
        max_length=20
    )
    y = models.CharField(
        "Y",
        max_length=20
    )
    w = models.CharField(
        "W",
        max_length=20
    )
    h = models.CharField(
        "H",
        max_length=20
    )
    pub_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)
