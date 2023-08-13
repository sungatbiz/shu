# Generated by Django 4.2.1 on 2023-08-09 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0133_rename_z_sene_das_yurt_klientler_sene_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dokmaseh_sklad',
            name='cykrulon_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy $'),
        ),
        migrations.AddField(
            model_name='dokmaseh_sklad',
            name='cykrulon_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='abathalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Abat haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='abathalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Abat haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='brakhalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Brak haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='brakhalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Brak haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='ganarhalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Ganar haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='haltaseh_sklad',
            name='ganarhalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Ganar haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='sapakseh_sklad',
            name='cyksapak_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy $'),
        ),
        migrations.AddField(
            model_name='sapakseh_sklad',
            name='cyksapak_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy TMT'),
        ),
    ]
