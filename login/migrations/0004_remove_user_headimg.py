# Generated by Django 2.2.3 on 2022-03-13 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20220313_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='headimg',
        ),
    ]
