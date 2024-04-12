from rest_framework import serializers

from apps.products.models import Product, ProductImage, ProductAttribute, ProductColor


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['key', 'value']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', )

class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ('id', 'product', 'color')

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 
                  'category', 'image', 'views',
                  'price',)

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return obj.description
            
class ProductDetailSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    product_attributes = ProductAttributeSerializer(many=True, read_only=True)
    product_colors = ProductColorSerializer(many=True, read_only=True)

    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 
                  'category', 'image', 'views',
                  'price', 'product_images', 
                  'product_attributes', 'product_colors')
        
    