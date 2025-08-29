"""Модель источника цитаты."""

from django.db import models
from django.core.validators import MaxValueValidator

from backend.constants import (
    SOURCE_NAME_MAX_LENGTH,
    SOURCE_TYPE_MAX_LENGTH,
    SOURCE_AUTHOR_MAX_LENGTH,
    MAX_SOURCE_YEAR,
)


class Source(models.Model):
    """Модель источника цитаты."""

    TYPE_CHOICES = [
        ("book", "Книга"),
        ("movie", "Фильм"),
        ("tv", "Сериал"),
        ("game", "Игра"),
        ("speech", "Выступление"),
        ("other", "Другое"),
    ]

    name = models.CharField(
        max_length=SOURCE_NAME_MAX_LENGTH,
        verbose_name="Название",
        unique=True,
    )
    source_type = models.CharField(
        max_length=SOURCE_TYPE_MAX_LENGTH,
        choices=TYPE_CHOICES,
        verbose_name="Тип источника",
    )
    author = models.CharField(
        max_length=SOURCE_AUTHOR_MAX_LENGTH,
        blank=True,
        verbose_name="Автор/создатель",
    )
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Год",
        validators=[MaxValueValidator(MAX_SOURCE_YEAR)],
    )
    details = models.TextField(blank=True, verbose_name="Дополнительные сведения")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время добавления"
    )

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"
