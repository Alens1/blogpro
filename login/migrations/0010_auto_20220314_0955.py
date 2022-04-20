# Generated by Django 2.2.3 on 2022-03-14 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_user_headimg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='headimg',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]