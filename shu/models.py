from django.db import models
from django.utils import timezone
from users.models import *
from datetime import datetime
import random
from django.urls import reverse


def random_string():
    return str(random.randint(100000000000, 999999999999))

class Hasabat_sene(models.Model):
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ay sene'
        verbose_name_plural = 'Aydaky seneler'

    def get_absolute_url(self):
        return reverse('ay-sene-detail', kwargs={'pk': self.pk})

class Equ_money(models.Model):
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    dollar = models.DecimalField("Dollar bahasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    euro = models.DecimalField("Euro bahasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Equivalent'
        verbose_name_plural = 'Equivalents'

    def get_absolute_url(self):
        return reverse('equ-money-detail', kwargs={'pk': self.pk})

class Walyuta_hasap(models.Model):
    name = models.CharField("Walýuta hasap", max_length=100, blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Walýuta hasap'
        verbose_name_plural = 'Walýuta hasaplar'

    def get_absolute_url(self):
        return reverse('walyuta-bolum', kwargs={'pk': self.pk})

class Hasap_detail(models.Model):
    wal_hasap = models.ForeignKey(Walyuta_hasap, on_delete=models.CASCADE, null=True)
    gideji = models.DecimalField("Girdeji",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cykdajy = models.DecimalField("Çykdajy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ostatok = models.DecimalField("Ostatok",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Sebäbi", max_length=100, blank=True,null=True)
    bellik = models.CharField("Bellik", max_length=100, blank=True,null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Walýuta hasap maglumat'
        verbose_name_plural = 'Walýuta hasap maglumatlar'

    def get_absolute_url(self):
        return reverse('wal-hasap-detail', kwargs={'pk': self.pk})



# Dasyndan karz alynan pullar

class Das_karz_alynanpul(models.Model):
    karzcy = models.CharField("Kime bermeli we kimden almaly karz puly", max_length=1000, blank=True,null=True)
    a_summa_m = models.DecimalField("Jemi alynan TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    a_summa_d = models.DecimalField("Jemi alynan $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_m = models.DecimalField("Jemi TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_d = models.DecimalField("Jemi $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Jemi girdejileriniň sebäbi", max_length=100, blank=True,null=True,)
    bellik = models.TextField("Bellik", blank=True,null=True,)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.karzcy} Alynan karz pul'

    class Meta:
        verbose_name = 'Daşyndan alynan karz pul'
        verbose_name_plural = 'Daşyndan alynan karz pullar'

    def get_absolute_url(self):
        return reverse('karz-pul', kwargs={'pk': self.pk})

class Karz_yzyna_berilen(models.Model):
    alynan_karz = models.ForeignKey(Das_karz_alynanpul, on_delete=models.CASCADE, null=True)
    karzcy = models.CharField("Kime bermeli we kimden almaly karz puly", max_length=1000, blank=True,null=True)
    b_summa_m = models.DecimalField("Jemi berilen TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    b_summa_d = models.DecimalField("Jemi berilen $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Jemi girdejileriniň sebäbi", max_length=100, blank=True,null=True,)
    bellik = models.TextField("Bellik", blank=True,null=True,)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.karzcy} Berilen karz pul'

    class Meta:
        verbose_name = 'Daşyndan berilen karz pul'
        verbose_name_plural = 'Daşyndan berilen karz pullar'

    def get_absolute_url(self):
        return reverse('karz-pul-berilen', kwargs={'pk': self.pk})


# sklad

class World_cygmal(models.Model):
    zawod = models.ForeignKey(Cigmal_Zawodlar, on_delete=models.CASCADE, null=True)
    kontrak_nomer = models.CharField("Şertnama belgisi", max_length=100, blank=True,null=True)
    markasy = models.CharField("Markasy", max_length=100, blank=True,null=True)
    tony = models.DecimalField("Mukdary",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_m = models.DecimalField("Bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    paddon_kg = models.DecimalField("Paddon kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bigbag_kg = models.DecimalField("Big bag kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.kontrak_nomer

    class Meta:
        verbose_name = 'Zawotdan satyn alynan çigmal'
        verbose_name_plural = 'Zawotdan satyn alynan çigmallar'

    def get_absolute_url(self):
        return reverse('cigmal-zawotdan', kwargs={'pk': self.pk})

class World_sklad(models.Model):
    kime_dusdi = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True)
    zawod = models.ForeignKey(Cigmal_Zawodlar, on_delete=models.CASCADE, null=True)
    kontrak_nomer = models.CharField("Şertnama belgisi", max_length=100, blank=True,null=True)
    markasy = models.CharField("Markasy", max_length=100, blank=True,null=True)
    tony = models.IntegerField("Mukdary", null=True, blank=True, default=None)
    bahasy_m = models.DecimalField("Bahasy manatda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Bahasy dollarda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    paddon_kg = models.DecimalField("Paddon kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bigbag_kg = models.DecimalField("Big bag kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_m = models.DecimalField("Jemi bahasy manatda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi bahasy dollarda",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.kontrak_nomer

    class Meta:
        verbose_name = 'Daşyndan sklada gelen çigmal'
        verbose_name_plural = 'Daşyndan sklada gelen çigmallar'

    def get_absolute_url(self):
        return reverse('cigmal-gelen-zawod', kwargs={'pk': self.pk})

class Sklad_swotkalar(models.Model):
    kimden = models.ForeignKey(Cigmal_Zawodlar, on_delete=models.CASCADE, null=True)
    kime = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True)
    kontrak_nomer = models.CharField("Şertnama belgisi", max_length=100, blank=True,null=True)
    markasy = models.CharField("Markasy", max_length=100, blank=True,null=True)
    gelen_tony = models.IntegerField("Harydyň gelen sany",null=True, blank=True, default=None)
    giden_tony = models.IntegerField("Harydyň giden sany",null=True, blank=True, default=None)
    bahasy_m = models.DecimalField("Gelende özüne düşýän bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    # giden_bahasy_m = models.DecimalField("Gidende özüne düşýän bahasy TMT", max_digits=8, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Gelende özüne düşýän bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_m = models.DecimalField("Jemi alynan bahasy manatda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi alynan bahasy dollarda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_gel_bah_m = models.DecimalField("Jemi gelen bahasy manatda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_gel_bah_d = models.DecimalField("Jemi gelen bahasy dollarda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    galyndy_bahasy_m = models.DecimalField("Galyndy bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    galyndy_bahasy_d = models.DecimalField("Galyndy bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    galyndy_tony = models.DecimalField("Galyndy kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    paddon_kg = models.DecimalField("Paddon kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bigbag_kg = models.DecimalField("Big bag kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    gel_sene = models.DateField("Alynan senesi", default=timezone.now, null=True, blank=True)
    # gid_sene = models.DateField("Gelen senesi", default=timezone.now, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return self.kontrak_nomer

    class Meta:
        verbose_name = 'Daşyndan alynan we gelen çigmalyň swotkasy'
        verbose_name_plural = 'Daşyndan alynan we gelen çigmallaryň swotkasy'

    def get_absolute_url(self):
        return reverse('cigmal_swotka', kwargs={'pk': self.pk})

class Halta_gornus(models.Model):
    name = models.CharField("Haltaň görnüşi", max_length=100, blank=True,null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Haltaň görnüşi'
        verbose_name_plural = 'Haltaň görnüşleri'

    def get_absolute_url(self):
        return reverse('haltagornus-detail', kwargs={'pk': self.pk})

class Sehe_paylamak(models.Model):
    karhana = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    kim_eltipberdi = models.CharField("Kim eltip berdi", max_length=100, blank=True,null=True)
    paddon = models.IntegerField("Paddon sany", null=True, blank=True, default=None)
    big_bag = models.IntegerField("Big bag halta sany", null=True, blank=True, default=None)
    arassa_agram = models.DecimalField("Sehe gelen arassa agram",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.karhana

    class Meta:
        verbose_name = 'Sehlere paýlanan çygmal'
        verbose_name_plural = 'Sehlere paýlanan çygmallar'

    def get_absolute_url(self):
        return reverse('sehsendcygmal-detail', kwargs={'pk': self.pk})

class Gelen_sklat(models.Model):
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    nirden_gelen = models.CharField("Haryt nirden geldi", max_length=1000, blank=True,null=True)
    nira_gitdi = models.CharField("Haryt nirä gitdi", max_length=1000, blank=True,null=True)
    modeli = models.CharField("Modeli", max_length=500, blank=True,null=True)
    sany = models.IntegerField("Harydyň sany",null=True, blank=True, default=None)
    haryt_kg = models.CharField("Haryt kg", max_length=500, blank=True,null=True)
    g_sany = models.IntegerField("Giden harydyň sany",null=True, blank=True, default=None)
    g_haryt_kg = models.CharField("Giden haryt kg", max_length=500, blank=True,null=True)
    oz_bahasy_m = models.DecimalField("Özüne düşýän bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    oz_bahasy_dol = models.DecimalField("Özüne düşýän bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    satlyk_bahasy_m = models.DecimalField("Satlyk bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    satlyk_bahasy_dol = models.DecimalField("Satlyk bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    g_sene = models.DateField("Giden harydyň senesi", default=timezone.now, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    g_bellik = models.CharField("Giden harydyň belligi",max_length=1000, blank=True, null=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    jemi_bahasy_m = models.DecimalField("Harydyň jemi bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_bahasy_d = models.DecimalField("Harydyň jemi bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    g_jemi_bahasy_m = models.DecimalField("Giden harydyň jemi bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    g_jemi_bahasy_d = models.DecimalField("Giden harydyň jemi bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Gelen we giden haryt'
        verbose_name_plural = 'Gelen we giden harytlar'

    def get_absolute_url(self):
        return reverse('sklad', kwargs={'pk': self.pk})

class AydakySklad_hasabat(models.Model):
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    modeli = models.CharField("Harydyň modeli", max_length=500, blank=True,null=True)
    jemi_sany = models.DecimalField("Harydyň mukdary",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    haryt_kg = models.CharField("Haryt kg", max_length=500, blank=True,null=True)
    oz_bahasy_m = models.DecimalField("Özüne düşýän bahasy TMT", default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    oz_bahasy_d = models.DecimalField("Özüne düşýän bahasy $", default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy_sany = models.DecimalField("Geçen aýdaky galyndy sany",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy_kg = models.DecimalField("Geçen aýdaky galyndy kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy_m = models.DecimalField("Geçen aýdaky galyndy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy_d = models.DecimalField("Geçen aýdaky galyndy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_gelen_m = models.DecimalField("Jemi aýdaky gelen bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_giden_m = models.DecimalField("Jemi aýdaky giden bahasy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_gelen_d = models.DecimalField("Jemi aýdaky gelen bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_giden_d = models.DecimalField("Jemi aýdaky giden bahasy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    wozwrat_sany = models.DecimalField("Jemi aýdaky wozwrat sany", default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    wozwrat_kg = models.DecimalField("Jemi aýdaky wozwrat kg", default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy_sany = models.DecimalField("Jemi aýdaky ahyrky galyndy sany",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy_kg = models.DecimalField("Jemi aýdaky ahyrky galyndy kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy_m = models.DecimalField("Jemi aýdaky ahyrky galyndy TMT",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy_d = models.DecimalField("Jemi aýdaky ahyrky galyndy $",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    yerinde_bar_haryt_sany = models.DecimalField("Jemi aýdaky ýerinde bar harydyň sany",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    yerinde_bar_haryt_kg = models.DecimalField("Jemi aýdaky ýerinde bar harydyň kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    tapawudy_sany = models.DecimalField("Aýdaky tapawut sany",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    tapawudy_kg = models.DecimalField("Aýdaky tapawut kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Aýdaky sklad hasabaty'
        verbose_name_plural = 'Aýdaky sklad hasabatlary'

    def get_absolute_url(self):
        return reverse('aysklad-hasabat', kwargs={'pk': self.pk})

class Gir_ostatok(models.Model):
    user = models.ForeignKey(AllUsers, related_name='ostatok', on_delete=models.CASCADE)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    ostatok = models.DecimalField("Her günüň ostatogy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ostatok'
        verbose_name_plural = 'Ostatoklar'

    def get_absolute_url(self):
        return reverse('b-hasap-detail', kwargs={'pk': self.pk})

class Export_yukler(models.Model):
    # office = models.ForeignKey(Office,on_delete=models.CASCADE,blank=True,null=True)
    kimden = models.ForeignKey(Sehler, related_name='export', on_delete=models.CASCADE,blank=True,null=True)
    kime = models.CharField("Giden edara-kähananyň ady", max_length=100, blank=True,null=True)
    deklorasiya_nomer = models.CharField("Diklarasiýa belgisi", max_length=100, blank=True,null=True)
    name_haryt = models.CharField("Näme haryt gitdi", max_length=100, blank=True,null=True)
    summa_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    summa_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Exporta gitýän ýük'
        verbose_name_plural = 'Exporta gitýän ýükler'

    def get_absolute_url(self):
        return reverse('export', kwargs={'pk': self.pk})

class Import_yukpul(models.Model):
    kimden = models.ForeignKey(Sehler, related_name='import_pul', on_delete=models.CASCADE,blank=True,null=True)
    kime = models.ForeignKey(AllUsers, on_delete=models.CASCADE,blank=True,null=True)
    g_summa_m = models.DecimalField("Geçirilen pul TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    g_summa_d = models.DecimalField("Geçirilen pul $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    a_summa_m = models.DecimalField("Alynan pul TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    a_summa_d = models.DecimalField("Alynan pul $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    tapawut_m = models.DecimalField("Tapawut puly TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    tapawut_d = models.DecimalField("Tapawut puly $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Import: haryt getirýän bilen hasaplaşyk'
        verbose_name_plural = 'Import: haryt getirýänler bilen hasaplaşyklar'

    def get_absolute_url(self):
        return reverse('import', kwargs={'pk': self.pk})


# Dasyndan isleyan zawodlar

class Das_zawod(models.Model):
    name = models.CharField("Zawodyň ady", max_length=1000, blank=True,null=True)
    tel = models.CharField("Telefon belgisi", null=True, blank=True, max_length=12)
    address = models.TextField("Salgysy", null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Daşyndan işleşilýän zawod'
        verbose_name_plural = 'Daşyndan işleşilýän zawodlar'

    def get_absolute_url(self):
        return reverse('das-zawod', kwargs={'pk': self.pk})

class Das_isleyan_zawodlar(models.Model):
    zawod = models.ForeignKey(Das_zawod, on_delete=models.CASCADE,null=True, blank=True)
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    b_haryt_sany = models.IntegerField("Zakaz harydyň sany",null=True, blank=True, default=0)
    b_haryt_kg = models.DecimalField("Zakaz haryt kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    g_haryt_sany = models.IntegerField("Galan harydyň sany",null=True, blank=True, default=0)
    g_haryt_kg = models.DecimalField("Galan haryt kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    b_bahasy_m = models.DecimalField("Berilen bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    b_bahasy_d = models.DecimalField("Berilen Bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    satylan_haryt_sany = models.IntegerField("Satylan harydyň sany",null=True, blank=True, default=0)
    satylan_haryt_kg = models.DecimalField("Satylan harydyň kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    b_jemi_bahasy_m = models.DecimalField("Berilen jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    b_jemi_bahasy_d = models.DecimalField("Berilen jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    tapawut_m = models.DecimalField("Tapawudy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    tapawut_d = models.DecimalField("Tapawudy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",blank=True, null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    
    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Daşyndan işleşilýän zawoda berilen harydy'
        verbose_name_plural = 'Daşyndan işleşilýän zawoda berilen harytlary'

    def get_absolute_url(self):
        return reverse('das-zawod-detail', kwargs={'pk': self.pk})

class Das_is_zawod_Alynan(models.Model):
    zak_berilen = models.ForeignKey(Das_isleyan_zawodlar, on_delete=models.CASCADE,null=True, blank=True)
    zawod = models.ForeignKey(Das_zawod, on_delete=models.CASCADE,null=True, blank=True)
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    a_haryt_sany = models.IntegerField("Alynan harydyň sany",null=True, blank=True, default=0)
    a_haryt_kg = models.DecimalField("Alynan haryt kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    a_jemi_bahasy_m = models.DecimalField("Alynan jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    a_jemi_bahasy_d = models.DecimalField("Alynan jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",blank=True, null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    
    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Daşyndan işleşilýän zawoda alynan harydy'
        verbose_name_plural = 'Daşyndan işleşilýän zawoda alynan harytlary'

    def get_absolute_url(self):
        return reverse('das-zawod-alynan', kwargs={'pk': self.pk})


# Dasary yurt klientler

class Das_yurt_klientler(models.Model):
    klient = models.ForeignKey(Manager_user, on_delete=models.CASCADE,null=True, blank=True)
    shertnama_nomer = models.CharField("Şertnama belgisi", max_length=100, blank=True,null=True)
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    z_sany = models.DecimalField("Harydyň şertnama möçberi",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_m = models.DecimalField("Bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    zj_bahasy_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    zj_bahasy_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    tapawut_m = models.DecimalField("Tapawudy TMT",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    tapawut_d = models.DecimalField("Tapawudy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    peyda_m = models.DecimalField("Jemi galýan peýda TMT",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    peyda_d = models.DecimalField("Jemi galýan peýda $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    sene = models.DateField("zakaz Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    
    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Daşary ýurt klient we peýda'
        verbose_name_plural = 'Daşary ýurt klientler we peýda'

    def get_absolute_url(self):
        return reverse('klient-peyda', kwargs={'pk': self.pk})

# html edit delete etmeli
class Das_yurt_klient_cykdajy(models.Model):
    gir_klient = models.ForeignKey(Das_yurt_klientler, on_delete=models.CASCADE,null=True, blank=True)
    klient = models.ForeignKey(Manager_user, on_delete=models.CASCADE,null=True, blank=True)
    shertnama_nomer = models.CharField("Şertnama belgisi", max_length=100, blank=True,null=True)
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    i_sany = models.DecimalField("Işlenen harydyň möçberi",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    cykdajy_m = models.DecimalField("Jemi çykdajy TMT",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    cykdajy_d = models.DecimalField("Jemi çykdajy $",default=0,max_digits=10,decimal_places=2, null=True, blank=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    sene = models.DateField("zakaz Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    
    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Daşary ýurt klient çykdajysy'
        verbose_name_plural = 'Daşary ýurt klientler çykdajylary'

    def get_absolute_url(self):
        return reverse('klient-cykdajy', kwargs={'pk': self.pk})



# Hasaphana

class Ojidanie(models.Model):
    u_sent_id = models.ForeignKey(AllUsers, related_name='oj_cash', on_delete=models.CASCADE,null=True, blank=True)
    u_came_id = models.ForeignKey(AllUsers, on_delete=models.CASCADE,null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    cash = models.DecimalField("Nagt pul TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cash_d = models.DecimalField("Nagt pul $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_m = models.DecimalField("Awans TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_d = models.DecimalField("Awans $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Geçirim puluň sebäbi", max_length=100, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    tassyk = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ojidanie'
        verbose_name_plural = 'Ojidaniyalar'

    def get_absolute_url(self):
        return reverse('ojidanie-update', kwargs={'pk': self.pk})

class Bolek_hasaplar(models.Model):
    oj = models.ForeignKey(Ojidanie, on_delete=models.CASCADE,null=True, blank=True)
    user_sent = models.ForeignKey(AllUsers, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(AllUsers, related_name='b_hasap', on_delete=models.CASCADE,null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    kurs = models.DecimalField("$ kursy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_m = models.DecimalField("Awans TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_d = models.DecimalField("Awans $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    girdeji = models.DecimalField("Her günüň girdejisi",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    girdeji_dollar = models.DecimalField("Her günüň girdejisi dollarda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cykdajy = models.DecimalField("Her günüň çykdajysy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cykdajy_dollar = models.DecimalField("Her günüň çykdajysy dollarda",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Girdejiniň ya-da çykdajynyň sebäbi", max_length=100, blank=True)
    bellik = models.TextField("Bellik", blank=True)

    def __str__(self):
        return f'{self.user.username} Bolek_hasaplar'

    class Meta:
        verbose_name = 'Bölek hasap'
        verbose_name_plural = 'Bölek hasaplar'

    def get_absolute_url(self):
        return reverse('hasaphana', kwargs={'pk': self.pk})

class Inwentar(models.Model):
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    bahasy_m = models.DecimalField("Bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sany = models.IntegerField("Sany", null=True, blank=True, default=None)
    j_bahasy_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    nirde_dur = models.CharField("Haryt nirde dur", max_length=1000, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Inwentar'
        verbose_name_plural = 'Inwentarlar'

    def get_absolute_url(self):
        return reverse('inwentar', kwargs={'pk': self.pk})

class Inwen_spisat(models.Model):
    inwent = models.ForeignKey(Inwentar, on_delete=models.CASCADE,null=True, blank=True)
    harydyn_ady = models.CharField("Harydyň ady", max_length=500, blank=True,null=True)
    bahasy_m = models.DecimalField("Bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bahasy_d = models.DecimalField("Bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sany = models.IntegerField("Sany", null=True, blank=True, default=None)
    j_bahasy_m = models.DecimalField("Jemi bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    j_bahasy_d = models.DecimalField("Jemi bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    nirde_dur = models.CharField("Haryt ozal nirde duran", max_length=1000, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.harydyn_ady

    class Meta:
        verbose_name = 'Spisat edilen inwentar'
        verbose_name_plural = 'Spisat edilen inwentarlar'

    def get_absolute_url(self):
        return reverse('inwentar-spisat', kwargs={'pk': self.pk})

class Aylyk_premya(models.Model):
    user = models.ForeignKey(AllUsers, related_name='aylyk_premya', on_delete=models.CASCADE)
    summa_m = models.DecimalField("Jemi TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    summa_dollar = models.DecimalField("Jemi $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_m = models.DecimalField("Awans TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans_d = models.DecimalField("Awans $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_m = models.DecimalField("Jemi TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_d = models.DecimalField("Jemi $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.CharField("Jemi girdejileriniň sebäbi", max_length=100, blank=True,null=True,)
    bellik = models.TextField("Bellik", blank=True,null=True,)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return f'{self.user.username} Aýlyk peýda premýa'

    class Meta:
        verbose_name = 'Aýlyk peýda premýa'
        verbose_name_plural = 'Aýlyklar peýdalar premýalar'

    def get_absolute_url(self):
        return reverse('aylyk-premya', kwargs={'pk': self.pk})

class Bank_user(models.Model):
    wal = models.ForeignKey(Walyuta_hasap, on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField("F.A.A", max_length=1000, blank=True,null=True)
    tel = models.CharField("Telefon belgisi", null=True, blank=True, max_length=12)
    address = models.TextField("Salgysy", null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Bank user'
        verbose_name_plural = 'Bank users'

    def get_absolute_url(self):
        return reverse('bank-users', kwargs={'pk': self.pk})

class Bank(models.Model):
    user = models.ForeignKey(Bank_user, on_delete=models.CASCADE,null=True, blank=True)
    wal = models.ForeignKey(Walyuta_hasap, on_delete=models.CASCADE,null=True, blank=True)
    shet_nomer = models.IntegerField("Walýutaň hasap belgisi",null=True, blank=True, default=None)
    g_summa = models.DecimalField("Jemi gelen pul",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    c_summa = models.DecimalField("Jemi giden pul",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    galyndy = models.DecimalField("Galyndy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sebap = models.TextField("Jemi girdeji-çykdajylaryň sebäbi",blank=True,null=True,)
    bellik = models.TextField("Bellik", blank=True,null=True,)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.name} Bank hereketi'

    class Meta:
        verbose_name = 'Bakdaky hereket'
        verbose_name_plural = 'Bakdaky hereketler'

    def get_absolute_url(self):
        return reverse('bank-hereket', kwargs={'pk': self.pk})


# Sapak SEH 

class Gundelik_sapak(models.Model):
    user = models.ForeignKey(Other_users, related_name='s_sapakseh', on_delete=models.CASCADE)
    offices = models.ForeignKey(Office, related_name='mysapak_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='s_sehs', on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    cyksapak_kg = models.DecimalField("Çykan sapak kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    cyksapak_bahasy_m = models.DecimalField("Çykan sapagyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cyksapak_bahasy_d = models.DecimalField("Çykan sapagyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    wozwrat_kg = models.DecimalField("Wozwrat kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    katyska_agram = models.DecimalField("Katuşkaň agramy kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    nirden_gelen = models.CharField("Nirden gelen sapak", max_length=1000, blank=True,null=True)
    enjam = models.CharField("Haysy enjamda dikilen", max_length=500, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Gündelik dokalan sapak'
        verbose_name_plural = 'Gündelik dokalan sapaklar'

    def get_absolute_url(self):
        return reverse('sapak-seh', kwargs={'pk': self.pk})

class Aydaky_sapak(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    offices = models.ForeignKey(Office, related_name='aysapak_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='ays_sehs', on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_cyk_kg = models.DecimalField("Jemi aydaky sapagyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_bahasy_m = models.DecimalField("Jemi aydaky sapagyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_bahasy_d = models.DecimalField("Jemi aydaky sapagyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ayda dokalan sapak hasabaty'
        verbose_name_plural = 'Ayda dokalan sapak hasabatlary'

    def get_absolute_url(self):
        return reverse('aysapak-detail', kwargs={'pk': self.pk})

class AydakySapak_hasabat(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    cyksapak_bahasy_m = models.DecimalField("Çykan sapagyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cyksapak_bahasy_d = models.DecimalField("Çykan sapagyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_dok_sapak = models.DecimalField("Jemi aýdaky sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    satylan_sapak_kg = models.DecimalField("Jemi aýdaky satylan sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat kg", default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy = models.DecimalField("Jemi aýdaky ahyrky galyndy kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    yerinde_bar_haryt = models.DecimalField("Jemi aýdaky ýerinde bar harydyň kg",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    tapawudy = models.DecimalField("Aýdaky tapawut",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Sapak seh aýlyk hasabaty'
        verbose_name_plural = 'Sapak seh aýlyk hasabatlary'

    def get_absolute_url(self):
        return reverse('sapak-seh-hasabat', kwargs={'pk': self.pk})

class Zakaz_SapakSwotka(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_kg = models.DecimalField("Harydyň jemi kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_baha_m = models.DecimalField("Jemi girdeji bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_baha_d = models.DecimalField("Jemi girdeji bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cyk_summa = models.DecimalField("Jemi çykdaýjy",max_digits=10, decimal_places=2, null=True, blank=True)
    cyk_summa_dol = models.DecimalField("Jemi çykdaýjy walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa = models.DecimalField("Jemi peýda",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa_dol = models.DecimalField("Jemi peýda walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik", max_length=1000, blank=True)
    sene = models.DateField("senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi id",null=True, blank=True, default=None)

    def __str__(self):
        return self.gal_pey_summa

    class Meta:
        verbose_name = 'Sapak seh peýda swotka'
        verbose_name_plural = 'Sapak seh peýda swotkalar'

    def get_absolute_url(self):
        return reverse('sapak-peyda-swotka', kwargs={'pk': self.pk})

class Sapak_seh_ay_tabel(models.Model):
    user = models.ForeignKey(Other_users, related_name='s_sehayhasabat', on_delete=models.CASCADE)
    oklady = models.DecimalField("Oklady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ay_isguni = models.IntegerField("Aydaky iş güni",null=True, blank=True, default=None)
    gune_dusyan_haky = models.DecimalField("Bir güne düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sagady = models.DecimalField("Iş gün sagady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sagat_dusyan_haky = models.DecimalField("Sagadyna düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sany = models.IntegerField("Işlän gün sany",null=True, blank=True, default=None)
    artyk_is_sagady = models.DecimalField("Artyk işlän sagasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans = models.DecimalField("Awans",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    kart_sum = models.DecimalField("Kartyna geçýän summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    el_sum = models.DecimalField("Eline almaly summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Aýdaky dokalan sapak hasabaty (Tabeller)'
        verbose_name_plural = 'Aýdaky dokalan sapak hasabatlary (Tabeller)'

    def get_absolute_url(self):
        return reverse('s-aylyk-tabel', kwargs={'pk': self.pk})

class Sapakseh_sklad(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_dok_sapak = models.DecimalField("Jemi aýdaky sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    cyksapak_bahasy_m = models.DecimalField("Çykan sapagyň bahasy TMT",max_digits=10, decimal_places=2, null=True, blank=True)
    cyksapak_bahasy_d = models.DecimalField("Çykan sapagyň bahasy $",max_digits=10, decimal_places=2, null=True, blank=True)
    satylan_sapak_kg = models.DecimalField("Jemi aýdaky satylan sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ahyrky_galyndy = models.DecimalField("Jemi aýdaky abat haltanyň ahyrky galyndy sany",max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Dokma seh sklada giden önüm'
        verbose_name_plural = 'Dokma seh sklada giden önümler'

    def get_absolute_url(self):
        return reverse('sapaksklada-giden-onum', kwargs={'pk': self.pk})

class Sapakseh_sklad_satylan(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    gel_sklad = models.ForeignKey(Sapakseh_sklad, on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_dok_sapak = models.DecimalField("Jemi aýdaky sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    satylan_sapak_kg = models.DecimalField("Jemi aýdaky satylan sapagyň kg",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Sapak seh skladan satylan önüm'
        verbose_name_plural = 'Sapak seh skladan satylan önümler'

    def get_absolute_url(self):
        return reverse('sapaksklada-satylan-onum', kwargs={'pk': self.pk})




# Halta SEH

class Gundelik_halta(models.Model):
    user = models.ForeignKey(Other_users, related_name='g_halta', on_delete=models.CASCADE)
    office = models.ForeignKey(Office, related_name='my_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='h_sehs', on_delete=models.CASCADE, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    abathalta_bahasy_m = models.DecimalField("Abat haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_bahasy_d = models.DecimalField("Abat haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_kg = models.DecimalField("Abat haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    brakhalta_bahasy_m = models.DecimalField("Brak haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_bahasy_d = models.DecimalField("Brak haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_kg = models.DecimalField("Brak haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    ganarhalta_bahasy_m = models.DecimalField("Ganar haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_bahasy_d = models.DecimalField("Ganar haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_kg = models.DecimalField("Ganar haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    sarp_sapak_kg = models.DecimalField("Dikilyan halta gityan sapak kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    wozwrat_kg = models.DecimalField("Wozwrat kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    katyska_agram = models.DecimalField("Katuşkaň agramy kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    nirden_gelen = models.CharField("Nirden gelen rulon", max_length=1000, blank=True,null=True)
    enjam = models.CharField("Haysy enjamda dokalan", max_length=500, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Gündelik halta'
        verbose_name_plural = 'Gündelik haltalar'

    def get_absolute_url(self):
        return reverse('halta-seh', kwargs={'pk': self.pk})

class Aydaky_halta(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    office = models.ForeignKey(Office, related_name='ay_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='ayh_sehs', on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    abathalta_kg = models.DecimalField("Abat haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    brakhalta_kg = models.DecimalField("Brak haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    ganarhalta_kg = models.DecimalField("Ganar haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_abat_sany = models.IntegerField("Jemi ayda abat haltaň sany",null=True, blank=True, default=None)
    jemi_abat_kg = models.DecimalField("Jemi ayda abat haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_brak_sany = models.IntegerField("Jemi ayda brak haltaň sany",null=True, blank=True, default=None)
    jemi_brak_kg = models.DecimalField("Jemi ayda brak haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_ganar_sany = models.IntegerField("Jemi ayda ganar haltaň sany",null=True, blank=True, default=None)
    jemi_ganar_kg = models.DecimalField("Jemi ayda ganar haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_abat_baha_m = models.DecimalField("Jemi aydaky abat hardyn bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_abat_baha_d = models.DecimalField("Jemi aydaky abat hardyn bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_brak_baha_m = models.DecimalField("Jemi aydaky barak hardyn bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_brak_baha_d = models.DecimalField("Jemi aydaky barak hardyn bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_ganar_baha_m = models.DecimalField("Jemi aydaky ganar hardyn bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_ganar_baha_d = models.DecimalField("Jemi aydaky ganar hardyn bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ayda tikilen haltaň hasabaty'
        verbose_name_plural = 'Ayda tikilen haltaň hasabatlar'

    def get_absolute_url(self):
        return reverse('ayhalta-detail', kwargs={'pk': self.pk})

class Aydakyhalta_hasabat(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    abathalta_bahasy_m = models.DecimalField("Abat haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_bahasy_d = models.DecimalField("Abat haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_kg = models.DecimalField("Abat haltaň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    brakhalta_bahasy_m = models.DecimalField("Brak haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_bahasy_d = models.DecimalField("Brak haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_kg = models.DecimalField("Brak haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    ganarhalta_bahasy_m = models.DecimalField("Ganar haltaň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_bahasy_d = models.DecimalField("Ganar haltaň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_kg = models.DecimalField("Ganar haltan kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    satylan_halta_sany = models.IntegerField("Jemi aýdaky satylan haltaň sany",null=True, blank=True, default=None)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ahyrky_galyndy_abat = models.IntegerField("Jemi aýdaky abat haltanyň ahyrky galyndy sany",null=True, blank=True)
    ahyrky_galyndy_brak = models.IntegerField("Jemi aýdaky brak haltanyň ahyrky galyndy sany",null=True, blank=True)
    ahyrky_galyndy_ganar = models.IntegerField("Jemi aýdaky ganar haltanyň ahyrky galyndy sany",null=True, blank=True)
    yerinde_bar_haryt = models.IntegerField("Jemi aýdaky ýerinde bar harydyň sany",null=True, blank=True, default=None)
    tapawudy = models.IntegerField("Aýdaky tapawut",null=True, blank=True, default=None)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Aýdaky haltaň hasabaty'
        verbose_name_plural = 'Aýdaky haltaň hasabatlary'

    def get_absolute_url(self):
        return reverse('ayhalta-hasabat-detail', kwargs={'pk': self.pk})

class Halta_seh_ay_tabel(models.Model):
    user = models.ForeignKey(Other_users, related_name='h_sehayhasabat', on_delete=models.CASCADE)
    oklady = models.DecimalField("Oklady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ay_isguni = models.IntegerField("Aydaky iş güni",null=True, blank=True, default=None)
    gune_dusyan_haky = models.DecimalField("Bir güne düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sagady = models.DecimalField("Iş gün sagady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sagat_dusyan_haky = models.DecimalField("Sagadyna düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sany = models.IntegerField("Işlän gün sany",null=True, blank=True, default=None)
    artyk_is_sagady = models.DecimalField("Artyk işlän sagasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans = models.DecimalField("Awans",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    kart_sum = models.DecimalField("Kartyna geçýän summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    el_sum = models.DecimalField("Eline almaly summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Halta seh aýlyk hasabaty (Tabel)'
        verbose_name_plural = 'Halta seh aýlyk hasabatlary (Tabeller)'

    def get_absolute_url(self):
        return reverse('halsehay-hasabat-detail', kwargs={'pk': self.pk})

class Zakaz_balans(models.Model):
    user = models.ForeignKey(Other_users, related_name='zakaz_balans', on_delete=models.CASCADE)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    h_olceg = models.CharField("Önümiň ölçegi", max_length=1000, blank=True,null=True)
    balans = models.DecimalField("Balans",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    tolenen_pul = models.DecimalField("Tölän puly manat",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    algy = models.DecimalField("Algy manat",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bergi = models.DecimalField("Bergi manat",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sany = models.IntegerField("Harydyň sany",null=True, blank=True, default=None)
    bahasy = models.DecimalField("Harydyň bahasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    gelen_cygmal = models.DecimalField("Gelen çygmal",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    wozwrat = models.DecimalField("Çygmal wozwrat",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    bellik = models.TextField("Bellik", max_length=1000, blank=True)
    zakaz_sene = models.DateField("Haryt zakaz edilen senesi", default=timezone.now, null=True, blank=True)
    toleg_sene = models.DateField("Haryt töleg edilen senesi", null=True, blank=True)
    haryt_code = models.CharField(max_length=12, unique=True, default=random_string, null=True, blank=True)
    seh = models.ForeignKey(Sehler, on_delete=models.CASCADE, blank=True,null=True)

    def __str__(self):
        return self.user.faa

    class Meta:
        verbose_name = 'Zakazçynyň balansy'
        verbose_name_plural = 'Zakazçynyň balanslary'

    def get_absolute_url(self):
        return reverse('zakazuser-detail', kwargs={'pk': self.pk})

class Zakaz_swotka(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    jemi_baha_m = models.DecimalField("Jemi girdeji bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_baha_d = models.DecimalField("Jemi girdeji bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cyk_summa = models.DecimalField("Jemi çykdaýjy", max_digits=6, decimal_places=2, null=True, blank=True)
    cyk_summa_dol = models.DecimalField("Jemi çykdaýjy walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa = models.DecimalField("Jemi peýda",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa_dol = models.DecimalField("Jemi peýda walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik", max_length=1000, blank=True)
    sene = models.DateField("senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi id",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Halta seh peýda swotka'
        verbose_name_plural = 'Halta seh peýda swotkalar'

    def get_absolute_url(self):
        return reverse('halta-peyda-swotka', kwargs={'pk': self.pk})

class Haltaseh_sklad(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0, max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_bahasy_m = models.DecimalField("Abat haltaň bahasy TMT",max_digits=10, decimal_places=2, null=True, blank=True)
    abathalta_bahasy_d = models.DecimalField("Abat haltaň bahasy $",max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_bahasy_m = models.DecimalField("Brak haltaň bahasy TMT",max_digits=10, decimal_places=2, null=True, blank=True)
    brakhalta_bahasy_d = models.DecimalField("Brak haltaň bahasy $",max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_bahasy_m = models.DecimalField("Ganar haltaň bahasy TMT",max_digits=10, decimal_places=2, null=True, blank=True)
    ganarhalta_bahasy_d = models.DecimalField("Ganar haltaň bahasy $",max_digits=10, decimal_places=2, null=True, blank=True)
    satylan_halta_sany = models.IntegerField("Jemi aýdaky satylan haltaň sany",null=True, blank=True, default=None)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ahyrky_galyndy = models.IntegerField("Jemi aýdaky abat haltanyň ahyrky galyndy sany",null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Halta seh sklada giden önüm'
        verbose_name_plural = 'Halta seh sklada giden önümler'

    def get_absolute_url(self):
        return reverse('haltasklada-giden-onum', kwargs={'pk': self.pk})

class Haltaseh_sklad_satylan(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    gel_sklad = models.ForeignKey(Haltaseh_sklad, on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    h_olceg = models.CharField("Haltaň ölçegi", max_length=1000, blank=True,null=True)
    h_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    abathalta_sany = models.IntegerField("Abat haltaň sany",null=True, blank=True, default=None)
    brakhalta_sany = models.IntegerField("Brak haltaň sany",null=True, blank=True, default=None)
    ganarhalta_sany = models.IntegerField("Ganar haltaň sany",null=True, blank=True, default=None)
    satylan_halta_sany = models.IntegerField("Jemi aýdaky satylan haltaň sany",null=True, blank=True, default=None)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Halta seh skladan satylan önüm'
        verbose_name_plural = 'Halta seh skladan satylan önümler'

    def get_absolute_url(self):
        return reverse('haltasklada-satylan-onum', kwargs={'pk': self.pk})


# Dokma SEH

class Gundelik_dokma(models.Model):
    user = models.ForeignKey(Other_users, related_name='g_dokma', on_delete=models.CASCADE)
    offices = models.ForeignKey(Office, related_name='mydokma_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='d_sehs', on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    cykrulon_kg = models.DecimalField("Çykan rulonyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    cykrulon_bahasy_m = models.DecimalField("Çykan rulonyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cykrulon_bahasy_d = models.DecimalField("Çykan rulonyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    wozwrat_kg = models.DecimalField("Wozwrat kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    katyska_agram = models.DecimalField("Katuşkaň agramy kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    nirden_gelen = models.CharField("Nirden gelen sapak", max_length=1000, blank=True,null=True)
    enjam = models.CharField("Haysy enjamda dikilen", max_length=500, blank=True,null=True)
    bellik = models.CharField("Bellik",max_length=1000, blank=True, null=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Gündelik dokma'
        verbose_name_plural = 'Gündelik dokmalar'

    def get_absolute_url(self):
        return reverse('dokma-seh', kwargs={'pk': self.pk})

class Aydaky_dokma(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    offices = models.ForeignKey(Office, related_name='aydokma_office', on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, related_name='ayd_sehs', on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_cyk_kg = models.DecimalField("Jemi ayda çykan rulonyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_bahasy_m = models.DecimalField("Jemi aydaky rulonyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_bahasy_d = models.DecimalField("Jemi aydaky rulonyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Ayda dokalan rulonyň hasabaty'
        verbose_name_plural = 'Ayda dokalan rulonlaryň hasabatlary'

    def get_absolute_url(self):
        return reverse('aydokma-detail', kwargs={'pk': self.pk})

class AydakyDokma_hasabat(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    cykrulon_bahasy_m = models.DecimalField("Çykan rulonyň bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cykrulon_bahasy_d = models.DecimalField("Çykan rulonyň bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_dok_rulon = models.DecimalField("Jemi aýdaky dokalan rulonyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    satylan_dokma_kg = models.DecimalField("Jemi aýdaky satylan dokmanyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ahyrky_galyndy = models.DecimalField("Jemi aýdaky ahyrky galyndy kg",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    yerinde_bar_haryt = models.DecimalField("Jemi aýdaky ýerinde bar harydyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    tapawudy = models.DecimalField("Aýdaky tapawut",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Aýdaky dokalan rulonyň hasabaty'
        verbose_name_plural = 'Aýdaky dokalan rulonlaryň hasabatlary'

    def get_absolute_url(self):
        return reverse('aydokma-hasabat-detail', kwargs={'pk': self.pk})

class Zakaz_DokmaSwotka(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_kg = models.DecimalField("Harydyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    jemi_baha_m = models.DecimalField("Jemi girdeji bahasy TMT",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    jemi_baha_d = models.DecimalField("Jemi girdeji bahasy $",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    cyk_summa = models.DecimalField("Jemi çykdaýjy",max_digits=10, decimal_places=2, null=True, blank=True)
    cyk_summa_dol = models.DecimalField("Jemi çykdaýjy walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa = models.DecimalField("Jemi peýda",max_digits=10, decimal_places=2, null=True, blank=True)
    gal_pey_summa_dol = models.DecimalField("Jemi peýda walýuta",max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik", max_length=1000, blank=True)
    sene = models.DateField("senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi id",null=True, blank=True, default=None)

    def __str__(self):
        return self.gal_pey_summa

    class Meta:
        verbose_name = 'Dokma seh peýda swotka'
        verbose_name_plural = 'Dokma seh peýda swotkalar'

    def get_absolute_url(self):
        return reverse('dokma-peyda-swotka', kwargs={'pk': self.pk})

class Dokma_seh_ay_tabel(models.Model):
    user = models.ForeignKey(Other_users, related_name='d_sehayhasabat', on_delete=models.CASCADE)
    oklady = models.DecimalField("Oklady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    ay_isguni = models.IntegerField("Aydaky iş güni",null=True, blank=True, default=None)
    gune_dusyan_haky = models.DecimalField("Bir güne düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sagady = models.DecimalField("Iş gün sagady",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    sagat_dusyan_haky = models.DecimalField("Sagadyna düşýän haky",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    is_gun_sany = models.IntegerField("Işlän gün sany",null=True, blank=True, default=None)
    artyk_is_sagady = models.DecimalField("Artyk işlän sagasy",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    awans = models.DecimalField("Awans",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    kart_sum = models.DecimalField("Kartyna geçýän summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    el_sum = models.DecimalField("Eline almaly summa",default=0,max_digits=10, decimal_places=2, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Dokma seh aýlyk hasabaty (Tabel)'
        verbose_name_plural = 'Dokma seh aýlyk hasabatlary (Tabeller)'

    def get_absolute_url(self):
        return reverse('d-aylyk-tabel', kwargs={'pk': self.pk})

class Dokmaseh_sklad(models.Model):
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_dok_rulon = models.DecimalField("Jemi aýdaky dokalan rulonyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    cykrulon_bahasy_m = models.DecimalField("Çykan rulonyň bahasy TMT",max_digits=10, decimal_places=2, null=True, blank=True)
    cykrulon_bahasy_d = models.DecimalField("Çykan rulonyň bahasy $",max_digits=10, decimal_places=2, null=True, blank=True)
    satylan_dokma_kg = models.DecimalField("Jemi aýdaky satylan dokmanyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    gecenay_galyndy = models.DecimalField("Geçen aýdaky galyndy",default=0, max_digits=10, decimal_places=3, null=True, blank=True)
    wozwrat = models.DecimalField("Jemi aýdaky wozwrat",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    ahyrky_galyndy = models.DecimalField("Jemi aýdaky abat haltanyň ahyrky galyndy kg",max_digits=10, decimal_places=3,null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Dokma seh sklada giden önüm'
        verbose_name_plural = 'Dokma seh sklada giden önümler'

    def get_absolute_url(self):
        return reverse('dokmasklada-giden-onum', kwargs={'pk': self.pk})

class Dokmaseh_sklad_satylan(models.Model):
    zakaz_user = models.ForeignKey(Other_users, on_delete=models.CASCADE, null=True, blank=True)
    zakaz_code = models.CharField("Zakaz belgisi",max_length=1000, blank=True, null=True)
    gel_sklad = models.ForeignKey(Dokmaseh_sklad, on_delete=models.CASCADE, null=True, blank=True)
    sehs = models.ForeignKey(Sehler, on_delete=models.CASCADE, null=True, blank=True)
    d_gornusi = models.ForeignKey(Halta_gornus, on_delete=models.CASCADE, null=True)
    jemi_dok_rulon = models.DecimalField("Jemi aýdaky dokalan rulonyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    satylan_dokma_kg = models.DecimalField("Jemi aýdaky satylan dokmanyň kg",default=0,max_digits=10, decimal_places=3, null=True, blank=True)
    bellik = models.TextField("Bellik",null=True, blank=True)
    sene = models.DateField("Senesi", default=timezone.now, null=True, blank=True)
    has_sene = models.IntegerField("Senesi",null=True, blank=True, default=None)

    def __str__(self):
        return str(self.sene)

    class Meta:
        verbose_name = 'Dokma seh skladan satylan önüm'
        verbose_name_plural = 'Dokma seh skladan satylan önümler'

    def get_absolute_url(self):
        return reverse('dokmasklada-satylan-onum', kwargs={'pk': self.pk})










