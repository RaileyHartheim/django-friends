from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import FriendRequest, User


class CustomUserSerializer(UserSerializer):
    """ Сериализатор для пользователей. """
    is_in_friendship = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'is_in_friendship',
        )

    def get_is_in_friendship(self, obj):
        user = self.context.get('request').user
        if obj == user:
            return 'Это ваш профиль'
        if user.is_anonymous:
            return 'Войдите в аккаунт для просмотра статуса'
        if obj in user.friends.all():
            return 'Вы друзья'
        if FriendRequest.objects.filter(sender=obj, receiver=user).exists():
            return 'Этот пользователь направил вам заявку в друзья'
        if FriendRequest.objects.filter(sender=user, receiver=obj).exists():
            return 'Вы направили этому пользователю заявку в друзья'
        return 'Вы не друзья'


class CustomCreateUserSerializer(UserCreateSerializer):
    """ Сериализатор для создания пользователя. """

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def to_representation(self, instance):
        serializer = CustomCreateUserResponseSerializer(instance)
        return serializer.data


class CustomCreateUserResponseSerializer(CustomUserSerializer):
    """ Сериализатор для отображения пользователя после регистрации. """

    class Meta:
        model = User
        fields = (
            'id',
            'username',
        )


class FriendRequestFromUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для исходящих заявок в друзья. """

    class Meta:
        model = FriendRequest
        fields = (
            'id',
            'receiver'
        )


class FriendRequestToUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для входящих заявок в друзья. """

    class Meta:
        model = FriendRequest
        fields = (
            'id',
            'sender'
        )


class FriendRequestSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания заявок в друзья. """

    class Meta:
        model = FriendRequest
        fields = (
            'sender',
            'receiver'
        )
