from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status

from apps.cart.models import Cart, CartItem
from apps.cart.serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer

class CartAPI(GenericViewSet,
              mixins.ListModelMixin,
              mixins.CreateModelMixin,
              mixins.UpdateModelMixin,
              mixins.DestroyModelMixin,
              mixins.RetrieveModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filterset_fields = ['user', ]

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def destroy(self, request, *args, **kwargs):
        try:
            cart = self.get_object()
            CartItem.objects.filter(cart=cart).delete()  
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CartItemAPI(GenericViewSet,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.action == "create":
            return CartItemCreateSerializer
        return CartItemSerializer

    def create(self, request, *args, **kwargs):
        cart_id = request.data.get('cart')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if not all([cart_id, product_id]):
            return Response({"detail": "Missing cart or product"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Используем filter вместо get_or_create для поиска существующих записей
            cart_items = CartItem.objects.filter(cart_id=cart_id, product_id=product_id)
            if cart_items.exists():
                # Если товары найдены, обновляем количество первой записи
                cart_item = cart_items.first()
                cart_item.quantity += int(quantity)
                cart_item.save()
                created = False
            else:
                # Если товар не найден, создаем новый
                cart_item = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
                created = True
                serializer = self.get_serializer(cart_item)
                return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

        except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)