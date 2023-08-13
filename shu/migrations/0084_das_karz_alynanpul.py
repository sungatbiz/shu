# Generated by Django 4.2.1 on 2023-07-20 13:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_cigmal_zawodlar'),
        ('shu', '0083_aylyk_premya_has_sene_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Das_karz_alynanpul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_summa_m', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi berilen TMT')),
                ('b_summa_d', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi berilen $')),
                ('a_summa_m', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi alynan TMT')),
                ('a_summa_d', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi alynan $')),
                ('jemi_m', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi TMT')),
                ('jemi_d', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi $')),
                ('sebap', models.CharField(blank=True, max_length=100, null=True, verbose_name='Jemi girdejileriniň sebäbi')),
                ('bellik', models.TextField(blank=True, null=True, verbose_name='Bellik')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
                ('has_sene', models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi')),
                ('kimden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='karz_pul', to='users.sehler')),
                ('kime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.sehler')),
            ],
            options={
                'verbose_name': 'Daşyndan alynan karz pul',
                'verbose_name_plural': 'Daşyndan alynan karz pullar',
            },
        ),
    ]
