from rest_framework.viewsets import ModelViewSet

from . import models, serializers


class ClientViewSet(ModelViewSet):
    """Класс представления для модели Client"""
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')


class MailingViewSet(ModelViewSet):
    """Класс представления для модели Mailing"""
    queryset = models.Mailing.objects.all()
    serializer_class = serializers.MailingSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')


class MessageViewSet(ModelViewSet):
    """Класс представления для модели Message"""
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    http_method_names = ('get',)
