"""Модель цитаты."""

import re
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from backend.constants import NORMALIZED_TEXT_MAX_LENGTH, SHOW_TEXT_LENGTH

User = get_user_model()


def normalize_text(text):
    """Нормализация текста."""
    # переводим в нижний регистр
    text = text.lower()
    # убираем пробелы, кавычки, апострофы и все небуквенно-цифровые символы
    text = re.sub(r'[\s"\'«»“”‘’„,.!?;:()\[\]{}…\-–—]', "", text)
    return text


class Quote(models.Model):
    """Модель цитаты."""

    text = models.TextField(verbose_name="Текст цитаты")
    normalized_text = models.CharField(
        max_length=NORMALIZED_TEXT_MAX_LENGTH,
        unique=True,
        editable=False,
        verbose_name="Нормализованный текст",
    )
    source = models.ForeignKey(
        "Source", on_delete=models.CASCADE, verbose_name="Источник"
    )
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ],
        verbose_name="Вес (от 0 до 1)"
    )
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотры")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время добавления"
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь (добавил)",
    )

    class Meta:
        unique_together = ("text", "source")  # дополнительная защита от дубликатов

    def __str__(self):
        return f"{self.text[:SHOW_TEXT_LENGTH]} - {self.source}"

    def clean(self):
        # При редактировании не считаем эту же цитату
        existing_quotes = Quote.objects.filter(source=self.source)
        if self.pk:
            existing_quotes = existing_quotes.exclude(pk=self.pk)
        if existing_quotes.count() >= 3:
            raise ValidationError(
                "У этого источника уже три цитаты — добавить ещё нельзя."
            )
        normalized = normalize_text(self.text)
        qs = Quote.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.filter(normalized_text=normalized).exists():
            raise ValidationError(
                "Такая цитата уже существует (с учётом нормализации)."
            )
        self.normalized_text = normalized

    def save(self, *args, **kwargs):
        self.full_clean()  # Чтобы clean сработал и в save()
        super().save(*args, **kwargs)
