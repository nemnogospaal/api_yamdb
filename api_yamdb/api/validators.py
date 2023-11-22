from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

username_validator = UnicodeUsernameValidator()


def username_me_validator(value):
    if value.lower() == 'me':
        raise ValidationError('Невозможно использовать данный логин')