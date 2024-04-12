
from django.db import models

from apps.products.models import Product, ProductColor
from apps.user.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name="user_carts", 
        verbose_name="Пользователь"
    )
    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )
    
    def __str__(self):
        return f"{self.user}"
    
    class Meta: 
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='cart_items', 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, 
        related_name='cart_items', verbose_name="Товар"
    )
    colors = models.ManyToManyField(
        ProductColor, related_name='cart_items', 
        verbose_name="Цвета", blank=True
    )
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество товара"
    )
    is_selected = models.BooleanField(default=False, verbose_name="Выбрано")

    def __str__(self):
        return f"{self.cart}"
    
    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
