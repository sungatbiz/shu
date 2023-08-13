# Generated by Django 4.2.1 on 2023-08-07 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0119_rename_sene_id_zakaz_swotka_has_sene'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aydakyhalta_hasabat',
            name='gecenay_galyndy',
        ),
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='gecenay_galyndy_abat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Abat halta geçen aýdaky galyndy'),
        ),
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='gecenay_galyndy_brak',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Brak halta geçen aýdaky galyndy'),
        ),
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='gecenay_galyndy_ganar',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Ganar halta geçen aýdaky galyndy'),
        ),
    ]
