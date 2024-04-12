from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.category.models import Category
from apps.category.serializers import CategorySerializer, CategoryDetailSerializer, CategoryListSerializer

# Create your views here.
class CategoryAPIView(GenericViewSet,
                      ListModelMixin,
                      RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer   
        elif self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            # Возвращаем только категории без родителей для списка
            return Category.objects.filter(parent__isnull=True) #Функция нужна для отображения родительских категорий сперва
        # Для детального просмотра возвращаем все категории
        return super().get_queryset()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response(serializer.data)