# Generated by Django 3.1.7 on 2023-06-24 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0050_zakaz_swotka_sene_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aydakyhalta_hasabat',
            name='ahyrky_galyndy',
            field=models.IntegerField(blank=True, null=True, verbose_name='Jemi aýdaky ahyrky galyndy sany'),
        ),
    ]
