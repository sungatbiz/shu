# Generated by Django 4.2.2 on 2023-08-12 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0136_alter_gundelik_sapak_cyksapak_kg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='wozwrat',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky wozwrat'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='satylan_sapak_kg',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan sapagyň kg'),
        ),
        migrations.AlterField(
            model_name='dokmaseh_sklad',
            name='satylan_dokma_kg',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan dokmanyň kg'),
        ),
        migrations.AlterField(
            model_name='gundelik_halta',
            name='wozwrat_kg',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Wozwrat kg'),
        ),
        migrations.AlterField(
            model_name='haltaseh_sklad',
            name='wozwrat',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky wozwrat'),
        ),
        migrations.AlterField(
            model_name='sapakseh_sklad_satylan',
            name='jemi_dok_sapak',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky sapagyň kg'),
        ),
        migrations.AlterField(
            model_name='zakaz_balans',
            name='gelen_cygmal',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Gelen çygmal'),
        ),
        migrations.AlterField(
            model_name='zakaz_balans',
            name='wozwrat',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True, verbose_name='Çygmal wozwrat'),
        ),
    ]
