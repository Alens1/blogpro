# Generated by Django 2.2.3 on 2022-03-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_auto_20220327_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to='avatars'),
        ),
    ]
