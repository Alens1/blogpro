# Generated by Django 2.2.3 on 2022-03-28 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0018_auto_20220328_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.FileField(blank=True, upload_to='avatar'),
        ),
    ]
