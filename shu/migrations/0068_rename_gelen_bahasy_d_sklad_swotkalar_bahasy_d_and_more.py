# Generated by Django 4.2.1 on 2023-07-16 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0067_world_cygmal_bigbag_kg_world_cygmal_paddon_kg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sklad_swotkalar',
            old_name='gelen_bahasy_d',
            new_name='bahasy_d',
        ),
        migrations.RenameField(
            model_name='sklad_swotkalar',
            old_name='gelen_bahasy_m',
            new_name='bahasy_m',
        ),
        migrations.RemoveField(
            model_name='sklad_swotkalar',
            name='giden_bahasy_d',
        ),
        migrations.RemoveField(
            model_name='sklad_swotkalar',
            name='giden_bahasy_m',
        ),
    ]
