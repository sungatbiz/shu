# Generated by Django 4.2.1 on 2023-08-08 09:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_primary_seh_alter_sehler_options_sehler_pr_seh'),
        ('shu', '0126_rename_ahyrky_galyndy_abat_haltaseh_sklad_ahyrky_galyndy_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sapakseh_sklad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_olceg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ölçegi')),
                ('jemi_dok_sapak', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky sapagyň kg')),
                ('satylan_sapak_kg', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan sapagyň kg')),
                ('gecenay_galyndy', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Geçen aýdaky galyndy')),
                ('wozwrat', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky wozwrat')),
                ('ahyrky_galyndy', models.IntegerField(blank=True, null=True, verbose_name='Jemi aýdaky abat haltanyň ahyrky galyndy sany')),
                ('bellik', models.TextField(blank=True, null=True, verbose_name='Bellik')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
                ('has_sene', models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi')),
                ('h_gornusi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus')),
                ('sehs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sehler')),
            ],
            options={
                'verbose_name': 'Dokma seh sklada giden önüm',
                'verbose_name_plural': 'Dokma seh sklada giden önümler',
            },
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='abathalta_sany',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='ahyrky_galyndy',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='brakhalta_sany',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='ganarhalta_sany',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='gecenay_galyndy',
        ),
        migrations.RemoveField(
            model_name='haltaseh_sklad_satylan',
            name='wozwrat',
        ),
        migrations.AddField(
            model_name='haltaseh_sklad_satylan',
            name='zakaz_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.other_users'),
        ),
        migrations.CreateModel(
            name='Sapakseh_sklad_satylan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_olceg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ölçegi')),
                ('satylan_sapak_kg', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan sapagyň kg')),
                ('bellik', models.TextField(blank=True, null=True, verbose_name='Bellik')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
                ('has_sene', models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi')),
                ('gel_sklad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.sapakseh_sklad')),
                ('h_gornusi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus')),
                ('sehs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sehler')),
            ],
            options={
                'verbose_name': 'Sapak seh skladan satylan önüm',
                'verbose_name_plural': 'Sapak seh skladan satylan önümler',
            },
        ),
        migrations.CreateModel(
            name='Dokmaseh_sklad_satylan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_olceg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ölçegi')),
                ('satylan_dokma_kg', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan dokmanyň kg')),
                ('bellik', models.TextField(blank=True, null=True, verbose_name='Bellik')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
                ('has_sene', models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi')),
                ('gel_sklad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.haltaseh_sklad')),
                ('h_gornusi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus')),
                ('sehs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sehler')),
            ],
            options={
                'verbose_name': 'Dokma seh skladan satylan önüm',
                'verbose_name_plural': 'Dokma seh skladan satylan önümler',
            },
        ),
        migrations.CreateModel(
            name='Dokmaseh_sklad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h_olceg', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Ölçegi')),
                ('jemi_dok_rulon', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky dokalan rulonyň kg')),
                ('satylan_dokma_kg', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky satylan dokmanyň kg')),
                ('gecenay_galyndy', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Geçen aýdaky galyndy')),
                ('wozwrat', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Jemi aýdaky wozwrat')),
                ('ahyrky_galyndy', models.IntegerField(blank=True, null=True, verbose_name='Jemi aýdaky abat haltanyň ahyrky galyndy sany')),
                ('bellik', models.TextField(blank=True, null=True, verbose_name='Bellik')),
                ('sene', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Senesi')),
                ('has_sene', models.IntegerField(blank=True, default=None, null=True, verbose_name='Senesi')),
                ('h_gornusi', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus')),
                ('sehs', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sehler')),
            ],
            options={
                'verbose_name': 'Dokma seh sklada giden önüm',
                'verbose_name_plural': 'Dokma seh sklada giden önümler',
            },
        ),
    ]
