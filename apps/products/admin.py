from django.contrib import admin

from apps.products.models import Product, ProductImage, ProductAttribute, ProductColor
# Register your models here.

class ProductImageTabularInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAttributeTabularInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductColorTabularInline(admin.TabularInline):
    model = ProductColor
    extra = 1

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description','price')
    search_fields = ('title', 'description', 'price')
    inlines = (ProductImageTabularInline, ProductAttributeTabularInline, ProductColorTabularInline)
    readonly_fields = ('views', 'id')
    exclude = ('views', )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ()  
@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')