# Generated by Django 4.2.1 on 2023-08-06 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0115_remove_aydaky_halta_jemi_bahasy_d_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aydaky_halta',
            name='has_sene',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi'),
        ),
    ]
