# Generated by Django 3.1.7 on 2023-06-23 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0047_auto_20230622_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aydakyhalta_hasabat',
            name='has_sene',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi'),
        ),
        migrations.AlterField(
            model_name='gundelik_halta',
            name='has_sene',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi'),
        ),
    ]
