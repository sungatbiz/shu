# Generated by Django 3.1.7 on 2023-06-15 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0040_auto_20230615_0808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gundelik_halta',
            name='zakaz_code',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Zakaz belgisi'),
        ),
    ]
