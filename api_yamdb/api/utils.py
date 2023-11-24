from django.core.mail import send_mail


def send_mail_confirmation_code(user, confirmation_code):
    send_mail(
        subject='YaMDB - код подтверждения',
        message=(
            f'Код подтверждения: {confirmation_code}'
        ),
        recipient_list=[user.email],
        from_email='YaMDB@mail.ru',
        fail_silently=True,
    )
