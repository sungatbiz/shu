# Generated by Django 3.1.7 on 2023-05-11 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shu', '0007_auto_20230511_1121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ojidanie',
            name='u_came_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
