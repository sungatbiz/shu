# Generated by Django 4.2.1 on 2023-07-30 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0105_rename_wozwrat_aydakysklad_hasabat_wozwrat_kg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aydakysklad_hasabat',
            old_name='gecenay_galyndy',
            new_name='gecenay_galyndy_kg',
        ),
        migrations.AddField(
            model_name='aydakysklad_hasabat',
            name='gecenay_galyndy_sany',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Geçen aýdaky galyndy sany'),
        ),
    ]
