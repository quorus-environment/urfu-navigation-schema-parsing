"""Основные модели.

Университеты, секции, кабинеты.
"""
from django.db import models


class University(models.Model):
    """Сущность университета"""

    name = models.CharField(
        'Название',
        max_length=100
    )

    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)


class Section(models.Model):
    """Сущность секций"""

    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='sections'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)


class Office(models.Model):
    """Сущность кабинетов"""

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='offices'
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
