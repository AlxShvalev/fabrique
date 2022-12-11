from django.core.validators import RegexValidator


class PhoneNumberValidator(RegexValidator):
    regex = r'7\d{10}'
    message = 'Введите валидный номер телефона'
