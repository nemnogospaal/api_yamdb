# Generated by Django 3.2 on 2023-11-22 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='confirmation_code',
        ),
    ]
