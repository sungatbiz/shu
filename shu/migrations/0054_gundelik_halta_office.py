# Generated by Django 4.2.1 on 2023-07-01 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_sehler_office_office_all_sehler'),
        ('shu', '0053_auto_20230626_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='gundelik_halta',
            name='office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='my_office', to='users.office'),
        ),
    ]
