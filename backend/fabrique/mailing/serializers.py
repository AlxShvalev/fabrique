from rest_framework.serializers import ModelSerializer

from . import models, validators


class ClientSerializer(ModelSerializer):
    """Сериализатор для модели Client"""

    class Meta:
        model = models.Client
        validators = (validators.PhoneNumberValidator(),)
        fields = ('id', 'phone_number', 'phone_code', 'timezone', 'tag')


class MailingSerializer(ModelSerializer):
    """Сериализатор для модели Mailing"""
    class Meta:
        model = models.Mailing
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    """Сериализатор для модели Message"""
    class Meta:
        model = models.Message
        fields = '__all__'
