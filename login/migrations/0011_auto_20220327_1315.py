# Generated by Django 2.2.3 on 2022-03-27 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20220314_0955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sex',
        ),
        migrations.AddField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='birth',
            field=models.CharField(blank=True, default='unkonwn', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
