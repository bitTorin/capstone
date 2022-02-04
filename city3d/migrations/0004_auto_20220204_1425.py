# Generated by Django 3.2.7 on 2022-02-04 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city3d', '0003_auto_20220203_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='architect',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='building',
            name='contractor',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AddField(
            model_name='building',
            name='developer',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
    ]
