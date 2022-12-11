from django.db import models

from . import validators


class Client(models.Model):
    """Модель клиента"""
    phone_number = models.CharField(
        'Номер телефона',
        max_length=11,
        unique=True,
        validators=(validators.PhoneNumberValidator(),)
    )
    phone_code = models.CharField(
        'Код мобильного оператора',
        max_length=3,
        editable=False,
    )
    timezone = models.CharField('Часовой пояс', max_length=3)
    tag = models.CharField('Тег', max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def save(self, *args, **kwargs):
        self.phone_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return self.phone_number


class Mailing(models.Model):
    """Модель рассылки"""
    started_at = models.DateTimeField('Дата начала')
    finished_at = models.DateTimeField('Дата окончани')
    text = models.TextField('Текст сообщения')
    filter = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.text


class Message(models.Model):
    """Модель сообщения"""
    STATUSES = (
        ('sent', 'Sent'),
        ('postponed', 'Postponed'),
        ('not_sent', 'Not sent'),
    )
    sent_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        'Статус',
        choices=STATUSES,
        max_length=9,
        default='Sent'
    )
    mailing = models.ForeignKey(
        'Mailing',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Рассылка',
    )
    client = models.ForeignKey(
        'Client',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Клиент',
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'Рассылка {self.mailing.pk} для клиента {self.client.phone_number}'
