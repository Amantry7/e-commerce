from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import ValidationError
import asyncio

from apps.billing.models import Billing, BillingProduct
from apps.billing.serializars import BillingSerializer
from apps.cart.models import Cart

# Create your views here.
class BillingAPIView(GenericViewSet, CreateModelMixin):
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()

        if not cart:
            raise ValidationError("Корзина пользователя пуста.")

        billing = serializer.save(user=user)

        # Получаем список продуктов из корзины пользователя и подсчитываем итоговую сумму
        products_info = []
        total_price = 0
        for item in cart.cart_items.all():
            product = item.product
            quantity = item.quantity
            price = product.price
            product_detail = f"{product.title} ({price} KGS) - {quantity} шт - {price * quantity} KGS"
            total_price += price * quantity
            products_info.append(product_detail)
            BillingProduct.objects.create(billing=billing, product=product, quantity=quantity, price=price)


        products = "\n".join(products_info)

        payment_code = billing.payment_code
        city = billing.city
        street = billing.street
        phone = billing.phone
        delivery_price = billing.delivery_price
        billing_receipt_type = billing.billing_receipt_type
        first_name = billing.first_name
        last_name = billing.last_name

        # Обновляем итоговую сумму в биллинге
        billing.total_price = total_price
        billing.save()

        # Запускаем асинхронную функцию в синхронном коде
        # asyncio.run(send_post_billing(
        #     id=billing.id,
        #     products=products,
        #     payment_code=payment_code,
        #     city=city,
        #     street=street,
        #     phone=phone,
        #     delivery_price=delivery_price,
        #     total_price=total_price,
        #     billing_receipt_type=billing_receipt_type,
        #     first_name=first_name,
        #     last_name=last_name,
        #     type_order=type_order
        # ))

        # Удаляем корзину пользователя после успешного создания биллинга
        cart.delete()