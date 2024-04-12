from django.db import models
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField
import uuid

from apps.user.models import User
from apps.products.models import Product

# Create your models here.


class Billing(models.Model):
    class BillingReceiptTypeChoices(models.TextChoices):
        PICKUP = 'Самовывоз', _('Самовывоз')
        DELIVERY = 'Доставка', _('Доставка')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="billing_user",
        verbose_name="Пользователь",
        blank=True, null=True
    )
    first_name = models.CharField(
        max_length=255, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=255, verbose_name="Фамилия"
    )
    phone = models.CharField(
        max_length=255, verbose_name="Телефонный номер"
    )
    billing_receipt_type = models.CharField(
        max_length=100, choices=BillingReceiptTypeChoices.choices,
        default=BillingReceiptTypeChoices.DELIVERY,
        verbose_name=_('Вид получения товара')
    )
    payment_code = models.CharField(
        max_length=20, unique=True,
        verbose_name="Код оплаты биллинга",
        blank=True, null=True
    )
    status = models.BooleanField(
        default=False, verbose_name="Статус заказа"
    )
    country = models.CharField(
        max_length=255, 
        verbose_name="Страна"
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
        verbose_name="Улица"
    )
    note = models.TextField(
        verbose_name="Примечание",
        blank=True, null=True
    )
    total_price = models.PositiveIntegerField(
        verbose_name="Итоговая сумма",
        blank=True, null=True
    )
    delivery_price = models.PositiveIntegerField(
        verbose_name="Стоимость доставки",
        blank=True, null=True
    )
    discount_price = models.IntegerField(
        verbose_name="Скидка",
        blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания биллинга"
    )

    def __str__(self):
        return f"{self.billing_receipt_type} {self.payment_code}"
    
    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = str(uuid.uuid4().int)[:10]  # Генерируем UUID и оставляем только первые 10 цифр
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Биллинг"
        verbose_name_plural = "Биллинги"

class BillingProduct(models.Model):
    billing = models.ForeignKey(
        Billing, on_delete=models.CASCADE, 
        related_name='billing_products', verbose_name="Биллинг"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='products_billings', verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество товаров"
    )
    configurator = ArrayField(
        models.CharField(max_length=255, blank=True),
        verbose_name="Значения атрибута конфигуратора товара",
        blank=True, null=True,
        default=list
    )
    price = models.PositiveBigIntegerField(
        verbose_name="Итоговая цена товара", default=0
    )
    status = models.BooleanField(
        verbose_name="Статус", default=False
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.billing} - {self.product} ({self.quantity} шт.)"
    
    class Meta:
        verbose_name = "Продукт биллинга"
        verbose_name_plural = "Продукты биллингов"
        
class SaleSummary(Billing):
    class Meta:
        proxy = True
        verbose_name = 'Отчет продажа товар'
        verbose_name_plural = 'Отчеты продажи товаров'