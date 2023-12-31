# Generated by Django 4.2.1 on 2023-07-31 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0108_das_isleyan_zawodlar_t_haryt_kg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inwen_spisat',
            name='j_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy $'),
        ),
        migrations.AddField(
            model_name='inwen_spisat',
            name='j_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy TMT'),
        ),
        migrations.AddField(
            model_name='inwentar',
            name='j_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy $'),
        ),
        migrations.AddField(
            model_name='inwentar',
            name='j_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy TMT'),
        ),
        migrations.AlterField(
            model_name='das_isleyan_zawodlar',
            name='satylan_haryt_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Satylan harydyň kg'),
        ),
    ]
