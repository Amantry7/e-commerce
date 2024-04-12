from django.db import models
from django_resized.forms import ResizedImageField
from django.utils import timezone

from apps.category.models import Category
# Create your models here.
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category_products',
        verbose_name='Category'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True, null=True
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, default='no_image.jpg',
        upload_to='product_images/',
        verbose_name="Основная фотография",
        blank = True, null = True
    )
    views = models.PositiveIntegerField(
        verbose_name='Просмотры',
        default=0, blank=True, null=True
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name="Товар"
    )
    image = ResizedImageField(
        force_format="WEBP", 
        quality=100, 
        upload_to='product_images/',
        verbose_name="Фотография",
        blank = True, null = True
    )

    def __str__(self):
        return f"{self.product} {self.image}"
    
    class Meta:
        verbose_name = "Фотография товара"
        verbose_name_plural = "Фотографии товаров"
    
class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from django.forms import CharField, TextInput
        kwargs['widget'] = TextInput(attrs={'type': 'color'})
        return super().formfield(**kwargs)

class ProductColor(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_colors"
    )
    color = ColorField(verbose_name='Цвет')

    def __str__(self):
        return f"ID: {self.id}, color: {self.color}"

    class Meta:
        verbose_name = "Цвет товара"
        verbose_name_plural = "Цвета товаров"

class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_attributes',
        verbose_name="Товар"
    )
    key = models.CharField(
        max_length=255,
        verbose_name="Название (Ключ) атрибута"
    )
    value = models.CharField(
        max_length=255,
        verbose_name="Значение атрибута"
    )

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = "Атрибут товара"
        verbose_name_plural = "Атрибуты товаров"