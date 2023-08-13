# Generated by Django 4.2.1 on 2023-07-13 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_allusers_sehs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cigmal_Zawodlar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='Daşky zawodyň ady')),
                ('tel', models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefon belgisi')),
                ('reg_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='reg nomer')),
                ('ind_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='indeks nomer')),
                ('kpp_num', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True, verbose_name='Salgysy')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Gysga beyany')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
            ],
            options={
                'verbose_name': 'Daşky zawod',
                'verbose_name_plural': 'Daşky zawodlar',
            },
        ),
    ]
