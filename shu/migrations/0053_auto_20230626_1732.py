# Generated by Django 3.1.7 on 2023-06-26 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0052_auto_20230625_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zakaz_balans',
            name='wozwrat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Çygmal wozwrat'),
        ),
    ]
