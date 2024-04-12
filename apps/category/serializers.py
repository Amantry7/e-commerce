from rest_framework import serializers

from apps.category.models import Category
from apps.products.serializers import ProductSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'banner', 'icon',)

    def get_name(self, obj):
        language = self.context.get('request').query_params.get('language', 'ru')
        name = getattr(obj, f'name_{language}', None)
        return name if name else obj.name
    
class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'banner', 'icon', 'subcategories')

    

class CategoryDetailSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    category_products = ProductSerializer(read_only=True, many=True)
    name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'banner', 'icon', 'subcategories', 'category_products')  # Добавляем в поля
        ref_name = 'CategoryDetail'

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True, context=self.context).data
        return []

    def get_category_products(self, obj):
        return ProductSerializer(obj.category_products.all(), many=True, context=self.context).data

    def get_name(self, obj):
        language = self.context.get('request').query_params.get('language', 'ru')
        name = getattr(obj, f'name_{language}', None)
        return name if name else obj.name
    
class CategorySubcategoryDetailSerializer(serializers.ModelSerializer):
    # Now you can safely refer to CategoryDetailSerializer
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'banner', 'icon', 'parent', 'subcategories')
        ref_name = 'CategorySubcategoryDetail'

    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            # Recursive call to the same serializer
            return CategorySubcategoryDetailSerializer(obj.subcategories.all(), many=True).data
        return []