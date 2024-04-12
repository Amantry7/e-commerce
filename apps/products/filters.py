import django_filters
from django import forms
from .models import Product, Category

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        to_field_name='name',
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-control'})  
    )

    class Meta:
        model = Product
        fields = ['category']
