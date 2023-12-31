# Generated by Django 4.2.1 on 2023-07-30 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0101_bank_shet_nomer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inwen_spisat',
            name='bahasy',
        ),
        migrations.AddField(
            model_name='inwen_spisat',
            name='bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Bahasy $'),
        ),
        migrations.AddField(
            model_name='inwen_spisat',
            name='bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Bahasy TMT'),
        ),
        migrations.AddField(
            model_name='inwen_spisat',
            name='inwent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.inwentar'),
        ),
        migrations.AlterField(
            model_name='das_karz_alynanpul',
            name='kimden',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Kimden almaly karz puly'),
        ),
        migrations.AlterField(
            model_name='das_karz_alynanpul',
            name='kime',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Kime bermeli karz puly'),
        ),
        migrations.AlterField(
            model_name='inwen_spisat',
            name='nirde_dur',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Haryt ozal nirde duran'),
        ),
    ]
