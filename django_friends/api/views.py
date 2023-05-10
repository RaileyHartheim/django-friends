from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from users.models import FriendRequest, User
from .serializers import (CustomUserSerializer,
                          FriendRequestFromUserSerializer,
                          FriendRequestSerializer,
                          FriendRequestToUserSerializer)


class CustomUserViewSet(UserViewSet):
    """ Пользовательский вьюсет. """

    @action(
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        detail=False
    )
    def friends(self, request):
        """ Метод для просмотра списка друзей. """

        user = request.user
        friends = user.friends.all()
        serializer = CustomUserSerializer(
            friends,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def add_friend(self, request, id):
        """ Метод для добавления пользователя в друзья. """
        user = request.user
        friend = get_object_or_404(User, id=id)

        # попытка добавить себя в друзья
        if user == friend:
            data = {'error': 'Вы не можете добавить себя в друзья'}
            return Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        # пользователь уже в друзьях
        if friend in user.friends.all():
            data = {'error': 'Этот пользователь - уже ваш друг'}
            return Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )

        # если пользователь уже отправил заявку
        if FriendRequest.objects.filter(sender=friend, receiver=user).exists():
            user.friends.add(friend)
            friend_request = FriendRequest.objects.get(
                sender=friend,
                receiver=user)
            friend_request.delete()
            serializer = CustomUserSerializer(
                friend,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # само добавление в друзья
        try:
            request_sent = FriendRequest.objects.create(
                sender=user,
                receiver=friend)
            serializer = FriendRequestSerializer(
                request_sent,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            data = {'error': f'Не удалось отправить заявку в друзья: {exc}'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['DELETE'],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def delete_friend(self, request, id):
        """ Метод для удаления пользователя из друзей. """
        user = request.user
        friend = get_object_or_404(User, id=id)

        if friend not in user.friends.all():
            data = {'error': 'Этот пользователь не в списке ваших друзей'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user.friends.remove(friend)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            data = {'error': f'Не удалось удалить друга: {exc}'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RequestInViewSet(ListModelMixin, GenericViewSet):
    """ Вьюсет для обработки входящих заявок. """

    serializer_class = FriendRequestToUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user.is_anonymous:
            friend_requests = FriendRequest.objects.filter(receiver=user)
            return friend_requests
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def accept_request(self, request, pk):
        """ Подтверждение заявки в друзья. """
        user = self.request.user
        friend_request = get_object_or_404(FriendRequest, id=pk)
        friend = get_object_or_404(User, id=friend_request.sender.id)
        try:
            user.friends.add(friend)
            friend_request.delete()
            serializer = CustomUserSerializer(
                friend,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as exc:
            data = {'error': f'Не удалось принять заявку в друзья: {exc}'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST'],
        permission_classes=[IsAuthenticated],
        detail=True
    )
    def decline_request(self, request, pk):
        """ Отклонение заявки в друзья. """
        friend_request = get_object_or_404(FriendRequest, id=pk)
        try:
            friend_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exc:
            data = {'error': f'Не удалось отклонить заявку в друзья: {exc}'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class RequestOutViewSet(ListModelMixin, GenericViewSet):
    """ Вьюсет для отображения исходящих заявок. """

    serializer_class = FriendRequestFromUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(sender=user)
        return friend_requests
