# Generated by Django 4.2.1 on 2023-07-30 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0104_delete_giden_sklat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aydakysklad_hasabat',
            old_name='wozwrat',
            new_name='wozwrat_kg',
        ),
        migrations.AddField(
            model_name='aydakysklad_hasabat',
            name='wozwrat_sany',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky wozwrat sany'),
        ),
    ]
