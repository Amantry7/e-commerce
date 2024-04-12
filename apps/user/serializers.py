from rest_framework import serializers

from apps.user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'last_login', 'username', 
                  'first_name', 'last_name', 'balance', 
                  'email',)
 

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username',  'first_name',
                  'last_name', 'email', 'profile_image')

# class UserDetailSerializer(serializers.ModelSerializer):
#     billing_user = BillingSerializer(read_only=True, many=True)
#     class Meta:
#         model = User 
#         fields = ('id', 'last_login', 'username', 'is_vip',
#                   'first_name', 'last_name', 'balance', 
#                   'email', 'profile_image', 'billing_user', )

class UserRegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=250,
        write_only=True
    )
    confirm_password =  serializers.CharField(
        max_length=255,
        write_only=True   
    )
    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'password': 'Пароли отличаются'})
        elif len(attrs['password']) < 8  and len(attrs['confirm_password']) < 8:
            raise serializers.ValidationError({'password_len':'Длина пароля меньше 8'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
