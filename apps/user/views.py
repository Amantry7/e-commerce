from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from  apps.user.models import User
from apps.user.serializers import UserRegisterSerializers, UserSerializer
# Create your views here.

class UserViewsSet(GenericViewSet,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == 'create':
             return UserRegisterSerializers
        return UserSerializer

# Create your views here.
