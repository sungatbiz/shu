# Generated by Django 4.2.2 on 2023-07-10 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0056_aydaky_dokma_aydaky_sapak_aydakydokma_hasabat_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zakaz_sapakswotka',
            name='jemi_sany',
        ),
        migrations.AddField(
            model_name='zakaz_sapakswotka',
            name='jemi_kg',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Harydyň jemi kg'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='ahyrky_galyndy',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Jemi aýdaky ahyrky galyndy kg'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='gecenay_galyndy',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Geçen aýdaky galyndy'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='jemi_dok_sapak',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Jemi aýdaky sapagyň kg'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='satylan_sapak_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Jemi aýdaky satylan sapagyň kg'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='tapawudy',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Aýdaky tapawut'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='wozwrat',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Jemi aýdaky wozwrat kg'),
        ),
        migrations.AlterField(
            model_name='aydakysapak_hasabat',
            name='yerinde_bar_haryt',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='Jemi aýdaky ýerinde bar harydyň kg'),
        ),
    ]
