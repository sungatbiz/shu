# Generated by Django 3.1.7 on 2023-06-04 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0025_auto_20230604_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='aydaky_halta',
            name='h_gornusi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus'),
        ),
        migrations.AddField(
            model_name='gundelik_halta',
            name='h_gornusi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus'),
        ),
        migrations.AddField(
            model_name='sehe_paylamak',
            name='h_gornusi',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shu.halta_gornus'),
        ),
    ]
