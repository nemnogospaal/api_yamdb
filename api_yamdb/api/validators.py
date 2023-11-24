from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

username_validator = UnicodeUsernameValidator()

USERNAME_ME_REGEX = RegexValidator(r'^[\w.@+-]+\Z')
USERNAME_SYMBOLS_REGEX = RegexValidator(r'[^m][^e]')


def username_me_validator(value):
    if value.lower() == 'me':
        raise ValidationError('Невозможно использовать данный логин')
