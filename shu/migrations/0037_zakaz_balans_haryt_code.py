# Generated by Django 3.1.7 on 2023-06-14 11:46

from django.db import migrations, models
import shu.models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0036_auto_20230613_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='zakaz_balans',
            name='haryt_code',
            field=models.CharField(blank=True, default=shu.models.random_string, max_length=12, null=True, unique=True),
        ),
    ]
