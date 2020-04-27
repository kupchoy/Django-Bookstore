from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from books.models import Book

UserModel = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#
#     password = serializers.CharField(write_only=True)
#
#     def create(self, validated_data):
#
#         user = UserModel.objects.create(
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#
#         Token.objects.create(user=user)
#
#         return user
#
#     class Meta:
#         model = UserModel
#         # Tuple of serialized model fields (see link [2])
#         fields = ( "id", "username", "password", )
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'price', 'description', 'cover',)