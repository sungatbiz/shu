# Generated by Django 3.1.7 on 2023-04-29 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shu', '0005_auto_20230428_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ojidanie',
            name='u_came_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ojidanie',
            name='u_sent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='oj_cash', to=settings.AUTH_USER_MODEL),
        ),
    ]
