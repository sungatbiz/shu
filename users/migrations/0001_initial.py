# Generated by Django 3.1.7 on 2023-04-19 10:35

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bolum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Bölümiň ady')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Gysga beýany')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Bölümi',
                'verbose_name_plural': 'Bölümler',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Edara-kärhananyň ady')),
                ('tel', models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefon belgisi')),
                ('reg_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='reg nomer')),
                ('ind_num', models.CharField(blank=True, max_length=100, null=True, verbose_name='indeks nomer')),
                ('kpp_num', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.TextField(blank=True, null=True, verbose_name='Salgysy')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Gysga beyany')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Edara-kärhana',
                'verbose_name_plural': 'Edara-kärhanalar',
            },
        ),
        migrations.CreateModel(
            name='Wez',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='wezipesi')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Gysga beyany')),
                ('slug', models.SlugField(max_length=300, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'wezipesi',
                'verbose_name_plural': 'Wezipeler',
            },
        ),
        migrations.CreateModel(
            name='AllUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('birth_date', models.DateField(default=django.utils.timezone.now, verbose_name='Doglan senesi')),
                ('tel', models.CharField(blank=True, max_length=12, null=True, verbose_name='Telefon belgisi')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('user_code', models.CharField(blank=True, default=users.models.random_string, max_length=12, null=True, unique=True)),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('bolum', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.bolum')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.office')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('wez', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.wez')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
