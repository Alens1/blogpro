# Generated by Django 2.2.3 on 2022-03-29 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blog.Tag', verbose_name='标签'),
        ),
    ]
