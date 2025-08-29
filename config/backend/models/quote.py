"""Модель цитаты."""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from backend.models import Source

User = get_user_model()


class Quote(models.Model):
    """Модель цитаты."""

    text = models.TextField(verbose_name='Текст цитаты')
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, verbose_name='Источник'
    )
    weight = models.FloatField(
        default=1.0,
        verbose_name='Вес',
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    likes = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Дизлайки')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время добавления'
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Пользователь (добавил)'
    )

    def __str__(self):
        return self.text[:100]
    
    def clean(self):
        # При редактировании не считаем эту же цитату
        existing_quotes = Quote.objects.filter(source=self.source)
        if self.pk:
            existing_quotes = existing_quotes.exclude(pk=self.pk)
        if existing_quotes.count() >= 3:
            raise ValidationError('У этого источника уже три цитаты — добавить ещё нельзя.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Чтобы clean сработал и в save()
        super().save(*args, **kwargs)
