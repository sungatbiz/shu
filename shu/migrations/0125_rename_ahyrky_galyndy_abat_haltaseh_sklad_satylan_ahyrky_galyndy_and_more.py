# Generated by Django 4.2.1 on 2023-08-08 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0124_haltaseh_sklad_satylan_gel_sklad'),
    ]

    operations = [
        migrations.RenameField(
            model_name='haltaseh_sklad_satylan',
            old_name='ahyrky_galyndy_abat',
            new_name='ahyrky_galyndy',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='ahyrky_galyndy_brak',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='ahyrky_galyndy_ganar',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='tapawudy',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='yerinde_bar_haryt',
        ),
    ]
