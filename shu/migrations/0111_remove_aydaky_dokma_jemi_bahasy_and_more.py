# Generated by Django 4.2.1 on 2023-08-01 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0110_aydakydokma_hasabat_cykrulon_bahasy_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aydaky_dokma',
            name='jemi_bahasy',
        ),
        migrations.RemoveField(
            model_name='aydaky_halta',
            name='jemi_bahasy',
        ),
        migrations.RemoveField(
            model_name='aydaky_sapak',
            name='jemi_bahasy',
        ),
        migrations.RemoveField(
            model_name='aydakydokma_hasabat',
            name='cykrulon_bahasy',
        ),
        migrations.RemoveField(
            model_name='aydakyhalta_hasabat',
            name='abathalta_bahasy',
        ),
        migrations.RemoveField(
            model_name='aydakysapak_hasabat',
            name='cyksapak_bahasy',
        ),
        migrations.RemoveField(
            model_name='gundelik_dokma',
            name='cykrulon_bahasy',
        ),
        migrations.RemoveField(
            model_name='gundelik_halta',
            name='abathalta_bahasy',
        ),
        migrations.RemoveField(
            model_name='gundelik_halta',
            name='brakhalta_bahasy',
        ),
        migrations.RemoveField(
            model_name='gundelik_halta',
            name='ganarhalta_bahasy',
        ),
        migrations.RemoveField(
            model_name='gundelik_sapak',
            name='cyksapak_bahasy',
        ),
        migrations.AddField(
            model_name='aydaky_dokma',
            name='jemi_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky rulonyň bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_dokma',
            name='jemi_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky rulonyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky hardyn bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_halta',
            name='jemi_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky hardyn bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydaky_sapak',
            name='jemi_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky sapagyň bahasy $'),
        ),
        migrations.AddField(
            model_name='aydaky_sapak',
            name='jemi_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aydaky sapagyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydakydokma_hasabat',
            name='cykrulon_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy $'),
        ),
        migrations.AddField(
            model_name='aydakydokma_hasabat',
            name='cykrulon_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='abathalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Abat haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='aydakyhalta_hasabat',
            name='abathalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Abat haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='aydakysapak_hasabat',
            name='cyksapak_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy $'),
        ),
        migrations.AddField(
            model_name='aydakysapak_hasabat',
            name='cyksapak_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='gundelik_dokma',
            name='cykrulon_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy $'),
        ),
        migrations.AddField(
            model_name='gundelik_dokma',
            name='cykrulon_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan rulonyň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='abathalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Abat haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='abathalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Abat haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='brakhalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Brak haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='brakhalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Brak haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='ganarhalta_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Ganar haltaň bahasy $'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='ganarhalta_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Ganar haltaň bahasy TMT'),
        ),
        migrations.AddField(
            model_name='gundelik_sapak',
            name='cyksapak_bahasy_d',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy $'),
        ),
        migrations.AddField(
            model_name='gundelik_sapak',
            name='cyksapak_bahasy_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Çykan sapagyň bahasy TMT'),
        ),
    ]
