# Generated by Django 4.2.1 on 2023-07-24 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0096_aydakydokma_hasabat_zakaz_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inwentar',
            name='bahasy',
        ),
        migrations.AddField(
            model_name='inwentar',
            name='bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Bahasy $'),
        ),
        migrations.AddField(
            model_name='inwentar',
            name='bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Bahasy TMT'),
        ),
    ]
