# Generated by Django 4.2.1 on 2023-07-21 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0088_alter_das_isleyan_zawod_tapawut_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='das_isleyan_zawod_tapawut',
            name='jemi_bahasy_d',
        ),
        migrations.RemoveField(
            model_name='das_isleyan_zawod_tapawut',
            name='jemi_bahasy_m',
        ),
        migrations.AddField(
            model_name='das_isleyan_zawod_tapawut',
            name='j_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy $'),
        ),
        migrations.AddField(
            model_name='das_isleyan_zawod_tapawut',
            name='j_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy TMT'),
        ),
        migrations.AddField(
            model_name='das_isleyan_zawod_tapawut',
            name='zj_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy $'),
        ),
        migrations.AddField(
            model_name='das_isleyan_zawod_tapawut',
            name='zj_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi bahasy TMT'),
        ),
        migrations.AlterField(
            model_name='das_isleyan_zawod_tapawut',
            name='i_sany',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Işlenen harydyň möçberi'),
        ),
        migrations.AlterField(
            model_name='das_isleyan_zawod_tapawut',
            name='z_sany',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Harydyň şertnama möçberi'),
        ),
    ]
