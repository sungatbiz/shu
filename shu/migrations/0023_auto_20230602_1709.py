# Generated by Django 3.1.7 on 2023-06-02 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0022_inwentar_sany'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bolek_hasaplar',
            name='ostatok',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.gir_ostatok'),
        ),
    ]
