from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Follow

User = get_user_model()

REQUIRED_TRUE = {'required': True}
VALIDATOR_USER = UniqueValidator(queryset=User.objects.all())


class CustomUserCreateSerializer(UserCreateSerializer):

    email = serializers.EmailField(validators=[VALIDATOR_USER])
    username = serializers.CharField(validators=[VALIDATOR_USER])

    class Meta:
        model = User
        fields = (
            'email', 'id', 'password', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'email': REQUIRED_TRUE,
            'username': REQUIRED_TRUE,
            'password': REQUIRED_TRUE,
            'first_name': REQUIRED_TRUE,
            'last_name': REQUIRED_TRUE,
        }


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()
