# Generated by Django 4.2.1 on 2023-07-22 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_manager_user'),
        ('shu', '0093_aydakydokma_hasabat_sehs_aydakyhalta_hasabat_sehs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='zakaz_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.other_users'),
        ),
    ]
