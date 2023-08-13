from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils import timezone
import os
import random
from django.urls import reverse


def random_string():
    return str(random.randint(100000000000, 999999999999))


class Office(models.Model):
    name = models.CharField("Edara-kärhananyň ady", max_length=1000, null=True, blank=True)
    tel = models.CharField("Telefon belgisi", null=True, blank=True, max_length=12)
    reg_num = models.CharField("reg nomer", max_length=100, null=True, blank=True,)
    ind_num = models.CharField("indeks nomer", max_length=100, null=True, blank=True,)
    kpp_num = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField("Salgysy", null=True, blank=True)
    description = models.TextField("Gysga beyany", null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Edara-kärhana'
        verbose_name_plural = 'Edara-kärhanalar'

    def get_absolute_url(self):
        return reverse('office-detail', kwargs={'office_slug': self.slug})

class Primary_Seh(models.Model):
    name = models.CharField("Sehiň ady", max_length=1000, blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Seh'
        verbose_name_plural = 'Sehler'

    def get_absolute_url(self):
        return reverse('seh', kwargs={'pk': self.pk})

class Sehler(models.Model):
    office = models.ForeignKey(Office, related_name='office_sehs', on_delete=models.CASCADE, null=True, blank=True)
    pr_seh = models.ForeignKey(Primary_Seh, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField("Sehler", max_length=1000, blank=True,null=True)
    tel = models.CharField("Telefon belgisi", null=True, blank=True, max_length=12)
    address = models.TextField("Salgysy", null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'sub Seh'
        verbose_name_plural = 'sub Sehler'

    def get_absolute_url(self):
        return reverse('seh-detail', kwargs={'pk': self.pk})

class Bolum(models.Model):
    name = models.CharField("Bölümiň ady", max_length=100)
    description = models.TextField("Gysga beýany", null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Bölümi'
        verbose_name_plural = 'Bölümler'

    def get_absolute_url(self):
        return reverse('bolum-detail', kwargs={'bolum_slug': self.slug})

class Wez(models.Model):
    name = models.CharField("wezipesi", max_length=100)
    description = models.TextField("Gysga beyany", null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'wezipesi'
        verbose_name_plural = 'Wezipeler'

    def get_absolute_url(self):
        return reverse('wez-detail', kwargs={'pk': self.pk})

class Wez_other(models.Model):
    name = models.CharField("wezipesi", max_length=100)
    description = models.TextField("Gysga beyany", null=True, blank=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Other wezipesi'
        verbose_name_plural = 'Other Wezipeler'

    def get_absolute_url(self):
        return reverse('wez-detail', kwargs={'wez_slug': self.slug})

class AllUsers(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True)
    sehs = models.ForeignKey(Sehler, related_name='user_sehs', on_delete=models.CASCADE, null=True, blank=True)
    bolum = models.ForeignKey(Bolum, on_delete=models.CASCADE,null=True)
    wez = models.ForeignKey(Wez, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField("Doglan senesi", default=timezone.now)
    tel = models.CharField("Telefon belgisi", max_length=12, null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.TextField(null=True, blank=True)
    user_code = models.CharField(max_length=12, unique=True, default=random_string, null=True, blank=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(AllUsers, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    # def get_delete_url(self):
    # 		return f"{self.get_absolute_url()}/delete"
  
  
    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     # os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
    #     super().delete(*args, **kwargs)
    
    # def delete(self, *args, **kwargs):
    #     # You have to prepare what you need before delete the model
    #     storage, path = self.image.storage, self.image.path
    #     # Delete the model before the file
    #     super(AllUsers, self).delete(*args, **kwargs)
    #     # Delete the file after the model
    #     storage.delete(path)
    
    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

class Other_users(models.Model):
    faa = models.CharField("F.A.A", max_length=100, blank=True,null=True)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=True,null=True)
    seh = models.ForeignKey(Sehler, on_delete=models.CASCADE, blank=True,null=True)
    wez = models.ForeignKey(Wez_other, on_delete=models.CASCADE, blank=True,null=True)
    birth_date = models.DateField("Doglan senesi", default=timezone.now)
    address = models.TextField("Öý salgysy",null=True, blank=True)
    user_code = models.CharField(max_length=12, unique=True, default=random_string, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.faa

    class Meta:
        verbose_name = 'Başga işgär'
        verbose_name_plural = 'Başga işgärler'

    def get_absolute_url(self):
        return reverse('other-users-detail', kwargs={'pk': self.pk})

class Cigmal_Zawodlar(models.Model):
    name = models.CharField("Daşky zawodyň ady", max_length=500, blank=True,null=True)
    tel = models.CharField("Telefon belgisi", null=True, blank=True, max_length=12)
    reg_num = models.CharField("reg nomer", max_length=100, null=True, blank=True,)
    ind_num = models.CharField("indeks nomer", max_length=100, null=True, blank=True,)
    kpp_num = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField("Salgysy", null=True, blank=True)
    description = models.TextField("Gysga beyany", null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Daşky zawod'
        verbose_name_plural = 'Daşky zawodlar'

    def get_absolute_url(self):
        return reverse('zawod', kwargs={'pk': self.pk})
    
class Manager_user(models.Model):
    faa = models.CharField("F.A.A", max_length=100, blank=True,null=True)
    # office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=True,null=True)
    seh = models.ForeignKey(Sehler, on_delete=models.CASCADE, blank=True,null=True)
    wez = models.ForeignKey(Wez_other, on_delete=models.CASCADE, blank=True,null=True)
    birth_date = models.DateField("Doglan senesi", default=timezone.now)
    address = models.TextField("Öý salgysy",null=True, blank=True)
    user_code = models.CharField(max_length=12, unique=True, default=random_string, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.faa

    class Meta:
        verbose_name = 'Daşary ýurt klient'
        verbose_name_plural = 'Daşary ýurt klientler'

    def get_absolute_url(self):
        return reverse('manager', kwargs={'pk': self.pk})