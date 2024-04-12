from rest_framework import serializers

from apps.billing.models import Billing, BillingProduct

class BillingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingProduct
        fields = ('product', 'quantity',
                  'price', 'configurator', 'created')
        
class BillingSerializer(serializers.ModelSerializer):
    # billing_products = BillingProductSerializer(many=True)
    class Meta:
        model = Billing
        fields = ('first_name', 'last_name', 'phone', 
                  'billing_receipt_type', 'region', 
                  'city', 'street', 'note')
    
    # def create(self, validated_data):
    #     billing_products_data = validated_data.pop('billing_products')
    #     billing = Billing.objects.create(**validated_data)
    #     for product_data in billing_products_data:
    #         BillingProduct.objects.create(billing=billing, **product_data)
    #     return billing