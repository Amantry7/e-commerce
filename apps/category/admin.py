from django.contrib import admin
from django.db.models import Count

from apps.category.models import Category
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'banner', 'icon', 'products_count')
    search_fields = ('name', )
    readonly_fields = ('id', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request).annotate(
            _products_count=Count('category_products')
        )
        return queryset

    def products_count(self, obj):
        return obj._products_count
    products_count.admin_order_field = '_products_count'  
    products_count.short_description = 'Количество продуктов'  