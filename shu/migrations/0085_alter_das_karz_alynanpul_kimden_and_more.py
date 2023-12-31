# Generated by Django 4.2.1 on 2023-07-20 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_cigmal_zawodlar'),
        ('shu', '0084_das_karz_alynanpul'),
    ]

    operations = [
        migrations.AlterField(
            model_name='das_karz_alynanpul',
            name='kimden',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='karz_pul', to='users.sehler'),
        ),
        migrations.AlterField(
            model_name='das_karz_alynanpul',
            name='kime',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.sehler'),
        ),
    ]
