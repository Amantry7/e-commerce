from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    balance = models.DecimalField(
        max_digits=10,  verbose_name="Баланс пользователя",
        decimal_places=2, default=0.00
    )
    phone = models.CharField(
        max_length=255, verbose_name="Номер телефона",
        blank=True, null=True
    )
    country = models.CharField(
        max_length=255, 
        verbose_name="Страна",
        blank=True, null=True
    )
    region = models.CharField(
        max_length=255,
        verbose_name="Регион",
        blank=True, null=True
    )
    city = models.CharField(
        max_length=255, 
        verbose_name="Город",
        blank=True, null=True
    )
    street = models.CharField(
        max_length=255, 
        verbose_name="Улица",
        blank=True, null=True
    )
    def __str__(self):
        return self.username
    class Meta:
        verbose_name ='Пользаватель'
        verbose_name_plural ='Пользаватели'