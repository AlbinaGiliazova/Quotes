"""Модель кастомного пользователя."""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Модель пользователя."""
