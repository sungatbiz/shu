# Generated by Django 4.2.2 on 2023-07-11 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0057_remove_zakaz_sapakswotka_jemi_sany_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zakaz_dokmaswotka',
            name='jemi_sany',
        ),
        migrations.AddField(
            model_name='zakaz_dokmaswotka',
            name='jemi_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Harydyň kg'),
        ),
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='ahyrky_galyndy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Jemi aýdaky ahyrky galyndy kg'),
        ),
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='jemi_dok_rulon',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Jemi aýdaky dokalan rulonyň kg'),
        ),
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='satylan_dokma_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Jemi aýdaky satylan dokmanyň kg'),
        ),
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='tapawudy',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Aýdaky tapawut'),
        ),
        migrations.AlterField(
            model_name='aydakydokma_hasabat',
            name='yerinde_bar_haryt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Jemi aýdaky ýerinde bar harydyň kg'),
        ),
        migrations.AlterField(
            model_name='zakaz_sapakswotka',
            name='jemi_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Harydyň jemi kg'),
        ),
    ]
