from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django.shortcuts import get_list_or_404

from apps.products.models import Product
from apps.products.serializers import ProductSerializer, ProductDetailSerializer
from apps.products.filters import ProductFilter

# Create your views here.
class ProductAPIViews(GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin,
                      ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (SearchFilter, )
    search_fields = ('title', 'description', 'price')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  
        instance.save(update_fields=['views'])  
        serializer = self.get_serializer(instance)
        return Response(serializer.data)