# Generated by Django 4.2.1 on 2023-07-12 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_office_all_sehler_sehler_office'),
        ('shu', '0059_alter_aydakysapak_hasabat_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aydaky_dokma',
            name='sehs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ayd_sehs', to='users.sehler'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='sehs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ayh_sehs', to='users.sehler'),
        ),
        migrations.AddField(
            model_name='aydaky_sapak',
            name='sehs',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ays_sehs', to='users.sehler'),
        ),
    ]
