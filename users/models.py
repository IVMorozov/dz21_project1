from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя, наследуемая от AbstractUser.
    Получит все поля и методы AbstractUser, но с возможностью их переопределения и добавления новых полей.
    """

    avatar = models.ImageField(
        upload_to="avatars/",
        default="avatars/default_avatar.png",  # Убедитесь, что у вас есть это изображение в папке media/avatars/
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    
    vk_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="VK ID",
        unique=True,
        help_text="Уникальный идентификатор пользователя в VK",
    )
    telegram_id = models.CharField(    
        blank=True,
        null=True,
        verbose_name="Telegram ID",
        unique=True,
        help_text="Уникальный идентификатор пользователя в Telegram",
    )
    github_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="GitHub ID",
        unique=True,
        help_text="Уникальный идентификатор пользователя в GitHub",
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения",
        help_text="Дата рождения пользователя",
    )

