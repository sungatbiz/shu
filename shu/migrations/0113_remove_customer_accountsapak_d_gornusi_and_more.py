# Generated by Django 4.2.1 on 2023-08-02 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shu', '0112_zakaz_balans_seh'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer_accountsapak',
            name='d_gornusi',
        ),
        migrations.RemoveField(
            model_name='customer_accountsapak',
            name='user',
        ),
        migrations.DeleteModel(
            name='Customer_account',
        ),
        migrations.DeleteModel(
            name='Customer_accountSapak',
        ),
    ]
