from rest_framework import serializers

from apps.products.models import Product, ProductColor
from apps.cart.models import Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'category', 'image', 'views', 'price')


class CartProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id', 'color')

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    colors = CartProductColorSerializer(many=True, read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'colors', 'quantity')
        
class CartItemCreateSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.IntegerField())
    colors = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = CartItem
        fields = ('cart', 'products', 'colors', 'quantity')
        
class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    products = serializers.ListField(child=serializers.IntegerField(), allow_empty=True, required=False)

    def get_total_price(self, obj):
        total_price = sum(item.product.price * item.quantity for item in obj.cart_items.all())
        return total_price

    def create(self, validated_data):
        products = validated_data.pop('products', [])
        user = self.context['request'].user

        # Проверяем, есть ли у пользователя уже корзина
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            cart = Cart.objects.create(user=user)

        for product_id in products:
            product = Product.objects.get(pk=product_id)
            CartItem.objects.create(cart=cart, product=product, quantity=1)
        return cart

    class Meta:
        model = Cart
        fields = ('id', 'cart_items', 'total_price', 'products')

class CartCreateSerializer(serializers.ModelSerializer):
    products = serializers.ListField(child=serializers.DictField(), allow_empty=True, required=False)

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user)

        for product_data in products_data:
            product_id = product_data.get('id')
            quantity = product_data.get('quantity', 1)
            color_ids = product_data.get('colors', [])  # Обновлено здесь

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id)

            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()

            if color_ids:
                colors = ProductColor.objects.filter(id__in=color_ids)
                cart_item.colors.set(colors)  # Используйте set для установки отношений many-to-many

        return cart

    class Meta:
        model = Cart
        fields = ('id', 'products')