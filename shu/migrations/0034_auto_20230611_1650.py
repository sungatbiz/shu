# Generated by Django 3.1.7 on 2023-06-11 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0033_auto_20230611_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakaz_balans',
            name='toleg_sene',
            field=models.DateField(blank=True, null=True, verbose_name='Haryt töleg edilen senesi'),
        ),
    ]
