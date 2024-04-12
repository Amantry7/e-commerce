from django.db import models
from django_resized.forms import ResizedImageField
# Create your models here.

class Category(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название категории'
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='subcategories', 
        verbose_name="Родительская категория", 
        blank=True, null=True,
        # limit_choices_to={'parent__isnull': True},  # Только категории без родителя
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='subcategories', 
        verbose_name="Родительская категория", 
        blank=True, null=True,
    )
    banner = ResizedImageField(
        force_format="WEBP", default='no_image.jpg',
        quality=100, upload_to='category_banners/',
        verbose_name="Баннер категории",
        blank=True, null=True
    )
    icon = ResizedImageField(
        force_format="WEBP", default='no_image.jpg',
        quality=100, upload_to='category_icons/',
        verbose_name="Иконка категории",
        blank=True, null=True
    )
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'