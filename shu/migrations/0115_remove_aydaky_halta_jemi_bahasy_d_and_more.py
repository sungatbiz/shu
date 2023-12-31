# Generated by Django 4.2.1 on 2023-08-06 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0114_remove_hasaplasylmadyk_algy_kimden_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aydaky_halta',
            name='jemi_bahasy_d',
        ),
        migrations.RemoveField(
            model_name='aydaky_halta',
            name='jemi_bahasy_m',
        ),
        migrations.RemoveField(
            model_name='aydaky_halta',
            name='jemi_kg',
        ),
        migrations.RemoveField(
            model_name='aydaky_halta',
            name='jemi_sany',
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_abat_baha_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky abat hardyn bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_abat_baha_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky abat hardyn bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_abat_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi ayda abat haltaň kg'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_abat_sany',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Jemi ayda abat haltaň sany'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_brak_baha_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky barak hardyn bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_brak_baha_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky barak hardyn bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_brak_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi ayda brak haltaň kg'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_brak_sany',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Jemi ayda brak haltaň sany'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_ganar_baha_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky ganar hardyn bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_ganar_baha_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky ganar hardyn bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_ganar_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi ayda ganar haltaň kg'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_ganar_sany',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Jemi ayda ganar haltaň sany'),
        ),
    ]
