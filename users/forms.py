from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import *
from shu.models import *
from datetime import datetime, date
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.db.models import Q


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['office'].empty_label = _("Edara-kärhananyň welaýatyny saýlaň")
        self.fields['bolum'].empty_label = _("Edara-kärhananyň bölümini saýlaň")
        self.fields['wez'].empty_label = _("Wezipäni saýlaň")
    
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Ulanyjy ady'), 'class': 'form-control mb-3'}))
    office = forms.ModelChoiceField(Office.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Edara-kärhanany saýlaň', 'class': 'form-control mb-3'}))
    bolum = forms.ModelChoiceField(Bolum.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Bölümi', 'class': 'form-control mb-3'}))
    wez = forms.ModelChoiceField(Wez.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Wezipesi', 'class': 'form-control mb-3'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Ady'), 'class': 'form-control mb-3'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Familiýasy'), 'class': 'form-control mb-3'}))
    middle_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Atasynyň ady'), 'class': 'form-control mb-3'}))
    birth_date = forms.DateTimeField(label=False, required=False, help_text='Doglan senesi', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Telefon belgisi'), 'class': 'form-control mb-3'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(attrs={'placeholder': _('elektron poçtasy'), 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': _('Gizlin açary'), 'class': 'form-control mb-3'}))
    password2 = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': _('Gizlin açary gaýtala'), 'class': 'form-control mb-3'}))

    class Meta:
        model = AllUsers
        fields = ['username', 'office', 'bolum', 'wez', 'first_name','last_name','middle_name', 'birth_date', 'tel', 'email', 'address', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm,self).__init__(*args, **kwargs)
        self.fields['office'].empty_label = _("Edara-kärhananyň welaýatyny saýlaň")
        self.fields['bolum'].empty_label = _("Edara-kärhananyň bölümini saýlaň")
        self.fields['wez'].empty_label = _("Wezipäni saýlaň")
    
    office = forms.ModelChoiceField(Office.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Edara-kärhanany saýlaň', 'class': 'form-control mb-3'}))
    bolum = forms.ModelChoiceField(Bolum.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Bölümi', 'class': 'form-control mb-3'}))
    wez = forms.ModelChoiceField(Wez.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Wezipesi', 'class': 'form-control mb-3'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Ady', 'class': 'form-control mb-3'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Familiýasy', 'class': 'form-control mb-3'}))
    middle_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Atasynyň ady', 'class': 'form-control mb-3'}))
    # birth_date = forms.DateTimeField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Telefon belgisi', 'class': 'form-control mb-3'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(attrs={'placeholder': 'elektron poçtasy', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    image = forms.ImageField(label=False, initial='default.png', widget=forms.FileInput(attrs={'class': 'form-control mb-3'}))

    class Meta:
        model = AllUsers
        fields = ['office', 'bolum', 'wez', 'first_name','last_name','middle_name', 'tel', 'email', 'address','image']


# Cigmal zawodlar

class Cigmal_zawodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cigmal_zawodForm,self).__init__(*args, **kwargs)
        self.fields['zawod'].empty_label = _("Haýsy zawotdan satyn alynan")

    zawod = forms.ModelChoiceField(Cigmal_Zawodlar.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kontrak_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    markasy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Markasy', 'class': 'form-control mb-3'}))
    tony = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Mukdary', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy $', 'class': 'form-control mb-3'}))
    paddon_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Paddon kg', 'class': 'form-control mb-3'}))
    bigbag_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Big bag kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = World_cygmal
        fields = ('zawod', 'kontrak_nomer', 'markasy', 'tony','bahasy_m','bahasy_d','paddon_kg','bigbag_kg','bellik')

class Cigmal_zawod_editForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cigmal_zawod_editForm,self).__init__(*args, **kwargs)
        self.fields['zawod'].empty_label = _("Haýsy zawotdan satyn alynan")

    zawod = forms.ModelChoiceField(Cigmal_Zawodlar.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kontrak_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    markasy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Markasy', 'class': 'form-control mb-3'}))
    tony = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Mukdary', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy $', 'class': 'form-control mb-3'}))
    paddon_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Paddon kg', 'class': 'form-control mb-3'}))
    bigbag_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Big bag kg', 'class': 'form-control mb-3'}))
    j_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy TMT', 'class': 'form-control mb-3'}))
    j_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = World_cygmal
        fields = ('zawod', 'kontrak_nomer', 'markasy', 'tony','bahasy_m','bahasy_d','paddon_kg','bigbag_kg','j_bahasy_m','j_bahasy_d','bellik')

class Cigmal_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Cigmal_skladForm,self).__init__(*args, **kwargs)
        self.fields['zawod'].empty_label = _("Haýsy zawotdan satyn alynan")
        self.fields['kime_dusdi'].empty_label = _("Satyn alynan çigmaly haýsy sehe geçdi")

    zawod = forms.ModelChoiceField(Cigmal_Zawodlar.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kime_dusdi = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kontrak_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    markasy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Markasy', 'class': 'form-control mb-3'}))
    tony = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Mukdary', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy $', 'class': 'form-control mb-3'}))
    paddon_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Paddon kg', 'class': 'form-control mb-3'}))
    bigbag_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Big bag kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = World_cygmal
        fields = ('zawod','kime_dusdi','kontrak_nomer', 'markasy', 'tony','bahasy_m','bahasy_d','paddon_kg','bigbag_kg','bellik')


class Zawod_gelen_cigmalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Zawod_gelen_cigmalForm,self).__init__(*args, **kwargs)
        self.fields['kime_dusdi'].empty_label = _("Satyn alynan çigmaly haýsy sehe geçirmeli")

    kime_dusdi = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-4'}))
    tony = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Mukdary', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-5', 'style': 'height:100px;'}))

    class Meta:
        model = World_sklad
        fields = ('kime_dusdi','tony','bellik')



# SKLAD

class GelenHaryt_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GelenHaryt_skladForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haryt nirden geldi', 'class': 'form-control mb-3'}))
    modeli = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Modeli', 'class': 'form-control mb-3'}))
    sany = forms.IntegerField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    haryt_kg = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Haryt kg', 'class': 'form-control mb-3'}))
    oz_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Özüne düşýän bahasy TMT', 'class': 'form-control mb-3'}))
    oz_bahasy_dol = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Özüne düşýän bahasy $', 'class': 'form-control mb-3'}))
    satlyk_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Satlyk bahasy TMT', 'class': 'form-control mb-3'}))
    satlyk_bahasy_dol = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Satlyk bahasy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Gelen_sklat
        fields = ('harydyn_ady', 'nirden_gelen', 'modeli', 'sany','haryt_kg','oz_bahasy_m','oz_bahasy_dol','satlyk_bahasy_m','satlyk_bahasy_dol','bellik')

class GidenHaryt_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GidenHaryt_skladForm,self).__init__(*args, **kwargs)

    nira_gitdi = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haryt nirä gitdi', 'class': 'form-control mb-3'}))
    g_sany = forms.IntegerField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Giden harydyň sany', 'class': 'form-control mb-3'}))
    g_haryt_kg = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Giden haryt kg', 'class': 'form-control mb-3'}))
    g_bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Giden haryt üçin bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
        
    class Meta:
        model = Gelen_sklat
        fields = ('nira_gitdi', 'g_sany', 'g_haryt_kg','g_bellik')

class Ayjem_Sklad_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Ayjem_Sklad_UpdateForm,self).__init__(*args, **kwargs)

    yerinde_bar_haryt_sany = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt sany', 'class': 'form-control mb-3'}))
    yerinde_bar_haryt_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt kg', 'class': 'form-control mb-3'}))
    wozwrat_sany = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat sany', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = AydakySapak_hasabat
        fields = ('yerinde_bar_haryt_sany','yerinde_bar_haryt_kg','wozwrat_sany','wozwrat_kg','bellik')

class Sklad_sapakseh_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sklad_sapakseh_UpdateForm,self).__init__(*args, **kwargs)
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyn belgisini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=1),required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))    
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    satylan_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'satylan sapagyň kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False,widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Sapakseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','satylan_sapak_kg','bellik')

class Sklad_dokmaseh_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sklad_dokmaseh_UpdateForm,self).__init__(*args, **kwargs)
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyn belgisini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=3),required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))    
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    satylan_dokma_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'satylan dokma rulonyň kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False,widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Dokmaseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','satylan_dokma_kg','bellik')

class Sklad_haltaseh_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sklad_haltaseh_UpdateForm,self).__init__(*args, **kwargs)
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyn belgisini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=2),required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))    
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,required=False,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    satylan_halta_sany = forms.DecimalField(label=False,required=False,widget=forms.NumberInput(attrs={'placeholder': 'satylan haltanyň sany', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False,widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Haltaseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','satylan_halta_sany','bellik')

class Sklad_daszawod_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sklad_daszawod_UpdateForm,self).__init__(*args, **kwargs)

    satylan_haryt_sany = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'satylan harydyň sany', 'class': 'form-control mb-3'}))
    satylan_haryt_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'satylan harydyň kg', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Das_isleyan_zawodlar
        fields = ('satylan_haryt_sany','satylan_haryt_kg')

class Sapakseh_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sapakseh_skladForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_dok_sapak = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky sapagyň kg', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy TMT', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy $', 'class': 'form-control mb-3'}))
    satylan_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan sapagyň kg', 'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Sapakseh_sklad
        fields = ('d_gornusi','jemi_dok_sapak','cyksapak_bahasy_m','cyksapak_bahasy_d','satylan_sapak_kg','gecenay_galyndy','wozwrat','ahyrky_galyndy','bellik')

class Sapakseh_sklad_satylanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Sapakseh_sklad_satylanForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Haltaň görnüşini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_dok_sapak = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky sapagyň kg', 'class': 'form-control mb-3'}))
    satylan_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan sapagyň kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Sapakseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','d_gornusi','jemi_dok_sapak','satylan_sapak_kg','bellik')

class Dokmaseh_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Dokmaseh_skladForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_dok_rulon = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky dokma kg', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy TMT', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy $', 'class': 'form-control mb-3'}))
    satylan_dokma_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan dokma kg', 'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Dokmaseh_sklad
        fields = ('d_gornusi','jemi_dok_rulon','cykrulon_bahasy_m','cykrulon_bahasy_d','satylan_dokma_kg','gecenay_galyndy','wozwrat','ahyrky_galyndy','bellik')

class Dokmaseh_sklad_satylanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Dokmaseh_sklad_satylanForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Görnüşini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_dok_rulon = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky sapagyň kg', 'class': 'form-control mb-3'}))
    satylan_dokma_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan sapagyň kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Dokmaseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','d_gornusi','jemi_dok_rulon','satylan_dokma_kg','bellik')

class Haltaseh_skladForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Haltaseh_skladForm,self).__init__(*args, **kwargs)
        self.fields['h_gornusi'].empty_label = _("Görnüşini saýlaň")

    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'ölçegi', 'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    abathalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    abathalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy $', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy $', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy $', 'class': 'form-control mb-3'}))
    satylan_halta_sany = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan haltaň sany', 'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Haltaseh_sklad
        fields = ('h_gornusi','h_olceg','abathalta_sany','brakhalta_sany','ganarhalta_sany','abathalta_bahasy_m','abathalta_bahasy_d','brakhalta_bahasy_m','brakhalta_bahasy_d','ganarhalta_bahasy_m','ganarhalta_bahasy_m','satylan_halta_sany','gecenay_galyndy','wozwrat','ahyrky_galyndy','bellik')

class Haltaseh_sklad_satylanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Haltaseh_sklad_satylanForm,self).__init__(*args, **kwargs)
        self.fields['h_gornusi'].empty_label = _("Görnüşini saýlaň")

    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'ölçegi', 'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    satylan_halta_sany = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan halta sany', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3','style': 'height:100px;'}))
    
    class Meta:
        model = Haltaseh_sklad_satylan
        fields = ('zakaz_user','zakaz_code','h_gornusi','h_olceg','abathalta_sany','brakhalta_sany','ganarhalta_sany','satylan_halta_sany','bellik')



class OjUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OjUpdateForm,self).__init__(*args, **kwargs)

    u_came_id = forms.ModelChoiceField(AllUsers.objects.filter(is_superuser=False), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    sene = forms.DateTimeField(label=False, required=False, help_text='Senesi', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    cash = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Pul möçberi', 'class': 'form-control mb-3'}))
    cash_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Pul möçberi $', 'class': 'form-control mb-3'}))
    awans = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False, required=False,widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Ojidanie
        fields = ('u_sent_id', 'u_came_id','cash_d','awans', 'sene', 'cash', 'sebap', 'bellik', 'tassyk')

class OjSentForm(forms.ModelForm):
    # last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Familiýasy'), 'class': 'form-control mb-3'}))

    def __init__(self, *args, **kwargs):
        super(OjSentForm,self).__init__(*args, **kwargs)
        self.fields['u_came_id'].empty_label = _("Kim ulanyja ugratmaly")
        # self.fields['last_name'].initial = self.instance.u_came_id.last_name

    u_came_id = forms.ModelChoiceField(AllUsers.objects.filter(is_superuser=False), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    cash = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Pul möçberi TMT', 'class': 'form-control mb-3'}))
    cash_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Pul möçberi $', 'class': 'form-control mb-3'}))
    awans_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans TMT', 'class': 'form-control mb-3'}))
    awans_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Ojidanie
        fields = ('u_came_id', 'cash','cash_d','awans_m','awans_d','sebap', 'bellik')

class B_hasapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(B_hasapForm,self).__init__(*args, **kwargs)

    girdeji = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Girdeji TMT', 'class': 'form-control mb-3'}))
    girdeji_dollar=forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Girdeji $', 'class': 'form-control mb-3'}))
    cykdajy = forms.DecimalField(label=False, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdajy TMT', 'class': 'form-control mb-3'}))
    cykdajy_dollar=forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykdajy $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False, required=False,widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))    
    
    class Meta:
        model = Bolek_hasaplar
        fields = ('girdeji','girdeji_dollar','cykdajy','cykdajy_dollar','sebap','bellik')

class KadrUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(KadrUserForm,self).__init__(*args, **kwargs)
        # self.fields['bolum'].empty_label = _("Edara-kärhananyň bölümini saýlaň")
        self.fields['wez'].empty_label = _("Wezipäni saýlaň")
        # self.fields['group'].empty_label = _("Group saýlaň")
    
    username = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Ulanyjy ady'), 'class': 'form-control mb-3'}))
    # bolum = forms.ModelChoiceField(Bolum.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Bölümi', 'class': 'form-control mb-3'}))
    wez = forms.ModelChoiceField(Wez.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Wezipesi', 'class': 'form-control mb-3'}))
    # group = forms.ModelChoiceField(Group.objects, label=False, widget=forms.Select(attrs={'placeholder': 'Wezipesi', 'class': 'form-control mb-3'}))
    first_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Ady'), 'class': 'form-control mb-3'}))
    last_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Familiýasy'), 'class': 'form-control mb-3'}))
    middle_name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Atasynyň ady'), 'class': 'form-control mb-3'}))
    birth_date = forms.DateTimeField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': _('Telefon belgisi'), 'class': 'form-control mb-3'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(attrs={'placeholder': _('elektron poçtasy'), 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    image = forms.ImageField(label=False, initial='default.png', widget=forms.FileInput(attrs={'class': 'form-control mb-3'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={'placeholder': _('Gizlin açary'), 'class': 'form-control mb-3'}))

    class Meta:
        model = AllUsers
        fields = ['username','wez','first_name','last_name','middle_name','birth_date','tel', 'email', 'address','image', 'password']

class InwentarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InwentarForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Harydyň bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Harydyň bahasy $', 'class': 'form-control mb-3'}))
    sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    nirde_dur = forms.CharField(label=False, required=False,widget=forms.Textarea(attrs={'placeholder': 'Harydyň duran ýeri', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Inwentar
        fields = ('harydyn_ady', 'bahasy_m','bahasy_d', 'sany', 'nirde_dur', 'bellik')

class Inwentar_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Inwentar_UpdateForm,self).__init__(*args, **kwargs)

    sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Inwen_spisat
        fields = ('sany','bellik')


# Halta SEH
class GunhaltaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GunhaltaForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Tikinçini saýlaň")
        self.fields['h_gornusi'].empty_label = _("Haltaň görnüşini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haltaň ölçegi', 'class': 'form-control mb-3'}))
    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    abathalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    abathalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy $', 'class': 'form-control mb-3'}))
    abathalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň kg', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy $', 'class': 'form-control mb-3'}))
    brakhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň kg', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy $', 'class': 'form-control mb-3'}))
    ganarhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň kg', 'class': 'form-control mb-3'}))
    sarp_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Tikilyän halta gityän sapak kg', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Katuskaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_halta
        fields = ('user','h_olceg','h_gornusi','abathalta_sany','abathalta_bahasy_m','abathalta_bahasy_d','abathalta_kg','brakhalta_sany','brakhalta_bahasy_m','brakhalta_bahasy_d','brakhalta_kg','ganarhalta_sany','ganarhalta_bahasy_m','ganarhalta_bahasy_m','ganarhalta_kg','sarp_sapak_kg','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class ZakazOnumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakazOnumForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Tikinçini saýlaň")
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['h_gornusi'].empty_label = _("Haltaň görnüşini saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyn belgisini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=2), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haltaň ölçegi', 'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    abathalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    abathalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy $', 'class': 'form-control mb-3'}))
    abathalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň kg', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy $', 'class': 'form-control mb-3'}))
    brakhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň kg', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy $', 'class': 'form-control mb-3'}))
    ganarhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň kg', 'class': 'form-control mb-3'}))
    sarp_sapak_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tikilyän halta gityän sapak kg', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Katuşkaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_halta
        fields = ('user','zakaz_user','zakaz_code','h_olceg','h_gornusi','abathalta_sany','abathalta_bahasy_m','abathalta_bahasy_d','abathalta_kg','brakhalta_sany','brakhalta_bahasy_m','brakhalta_bahasy_d','brakhalta_kg','ganarhalta_sany','ganarhalta_bahasy_m','ganarhalta_bahasy_m','ganarhalta_kg','sarp_sapak_kg','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class ZakazForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakazForm, self).__init__(*args, **kwargs)
        self.fields['h_gornusi'].empty_label = _("Önümiň görnüşini saýlaň")

    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Önümiň ölçegi', 'class': 'form-control mb-3'}))
    tolenen_pul = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    bahasy = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň bahasy', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Zakaz_balans
        fields = ('h_gornusi','h_olceg','sany','bahasy','bellik')

class ZakUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakUpdateForm,self).__init__(*args, **kwargs)

    tolenen_pul = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Zakaz_balans
        fields = ('tolenen_pul','bellik')

class AyjemUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AyjemUpdateForm,self).__init__(*args, **kwargs)

    yerinde_bar_haryt = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Aydakyhalta_hasabat
        fields = ('yerinde_bar_haryt','bellik')

class ZakSwotkaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakSwotkaUpdateForm,self).__init__(*args, **kwargs)

    cyk_summa = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy TMT', 'class': 'form-control mb-3'}))
    cyk_summa_dol = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Zakaz_swotka
        fields = ('cyk_summa','cyk_summa_dol','bellik')

class HaltaSeh_TabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(HaltaSeh_TabelForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Işgäri saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(~Q(wez__name="Zakazçy"),~Q(wez__name="Manager")), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    oklady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Oklady', 'class': 'form-control mb-3'}))
    ay_isguni = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Aydaky iş güni', 'class': 'form-control mb-3'}))
    # gune_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bir güne düşýän haky', 'class': 'form-control mb-3'}))
    is_gun_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Iş gün sagady', 'class': 'form-control mb-3'}))
    # sagat_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Sagadyna düşýän haky', 'class': 'form-control mb-3'}))
    is_gun_sany = forms.IntegerField(label=False, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Işlän gün sany', 'class': 'form-control mb-3'}))
    artyk_is_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Artyk işlän sagasy', 'class': 'form-control mb-3'}))
    awans = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans', 'class': 'form-control mb-3'}))
    kart_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Kartyna geçýän summa', 'class': 'form-control mb-3'}))
    # el_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Eline almaly summa', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Halta_seh_ay_tabel
        fields = ('user','oklady','ay_isguni','is_gun_sagady','is_gun_sany','artyk_is_sagady','awans','kart_sum','bellik')

class ZakazcyAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakazcyAddForm,self).__init__(*args, **kwargs)
        self.fields['seh'].empty_label = _("Haýsy sehiň zakazçysy")
        self.fields['birth_date'].label = "Doglan senesi"

    seh = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    faa = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Zakazcynyn F.A.A', 'class': 'form-control mb-3'}))
    birth_date = forms.DateTimeField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Other_users
        fields = ('seh','faa','birth_date','address')

class TikinciAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TikinciAddForm,self).__init__(*args, **kwargs)
        self.fields['birth_date'].label = "Doglan senesi"

    faa = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Tikinçiniň F.A.A', 'class': 'form-control mb-3'}))
    birth_date = forms.DateTimeField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False,required=False,widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Other_users
        fields = ('faa','birth_date','address')

class Aydaky_haltaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aydaky_haltaForm,self).__init__(*args, **kwargs)
        self.fields['h_gornusi'].empty_label = _("Haltaň görnüşini saýlaň")

    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haltaň ölçegi', 'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    abathalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň kg', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň kg', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň kg', 'class': 'form-control mb-3'}))
    jemi_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi ayda haltaň sany', 'class': 'form-control mb-3'}))
    jemi_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi ayda haltaň kg', 'class': 'form-control mb-3'}))
    jemi_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky hardyn bahasy TMT', 'class': 'form-control mb-3'}))
    jemi_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky hardyn bahasy $', 'class': 'form-control mb-3'}))

    class Meta:
        model = Aydaky_halta
        fields = ('h_gornusi','h_olceg','abathalta_sany','abathalta_kg','brakhalta_sany','brakhalta_kg','ganarhalta_sany','ganarhalta_kg','jemi_sany','jemi_kg','jemi_bahasy_m','jemi_bahasy_d')

class Aydakyhalta_hasabatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aydakyhalta_hasabatForm,self).__init__(*args, **kwargs)
        self.fields['h_gornusi'].empty_label = _("Haltaň görnüşini saýlaň")

    h_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    h_olceg = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haltaň ölçegi', 'class': 'form-control mb-3'}))
    abathalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň sany', 'class': 'form-control mb-3'}))
    abathalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    abathalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň bahasy $', 'class': 'form-control mb-3'}))
    abathalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Abat haltaň kg', 'class': 'form-control mb-3'}))
    brakhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň sany', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    brakhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň bahasy $', 'class': 'form-control mb-3'}))
    brakhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Brak haltaň kg', 'class': 'form-control mb-3'}))
    ganarhalta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň sany', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy TMT', 'class': 'form-control mb-3'}))
    ganarhalta_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň bahasy $', 'class': 'form-control mb-3'}))
    ganarhalta_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Ganar haltaň kg', 'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    jemi_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi ayda haltaň sany', 'class': 'form-control mb-3'}))
    satylan_halta_sany = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan haltaň sany', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ahyrky galyndy sany', 'class': 'form-control mb-3'}))
    yerinde_bar_haryt = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ýerinde bar harydyň sany', 'class': 'form-control mb-3'}))
    tapawudy = forms.IntegerField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Aýdaky tapawut', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = Aydakyhalta_hasabat
        fields = ('h_gornusi','h_olceg','abathalta_sany','abathalta_bahasy_m','abathalta_bahasy_d','abathalta_kg','brakhalta_sany','brakhalta_bahasy_m','brakhalta_bahasy_d','brakhalta_kg','ganarhalta_sany','ganarhalta_bahasy_m','ganarhalta_bahasy_m','ganarhalta_kg','gecenay_galyndy','jemi_sany','satylan_halta_sany','wozwrat','ahyrky_galyndy','yerinde_bar_haryt','tapawudy','bellik')



# Sapak SEH
class GunSapakForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GunSapakForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Kim işlän saýlaň")
        self.fields['d_gornusi'].empty_label = _("Sapagyň görnüşini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh__pr_seh=1), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    cyksapak_kg = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapak kg', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy TMT', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy $', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Katuskaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_sapak
        fields = ('user','d_gornusi','cyksapak_kg','cyksapak_bahasy_m','cyksapak_bahasy_d','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class ZakazSapakForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakazSapakForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Kim işlän saýlaň")
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['d_gornusi'].empty_label = _("Sapagyň görnüşini saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyň belgisini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh__pr_seh=1), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=1), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    cyksapak_kg = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapak kg', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_m = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy TMT', 'class': 'form-control mb-3'}))
    cyksapak_bahasy_d = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan sapagyň bahasy $', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Katuskaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_sapak
        fields = ('user','zakaz_user','zakaz_code','d_gornusi','cyksapak_kg','cyksapak_bahasy_m','cyksapak_bahasy_d','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class AyjemSapakUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AyjemSapakUpdateForm,self).__init__(*args, **kwargs)

    yerinde_bar_haryt = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = AydakySapak_hasabat
        fields = ('yerinde_bar_haryt','bellik')

class ZakSwotkaSapakUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakSwotkaSapakUpdateForm,self).__init__(*args, **kwargs)

    cyk_summa = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy TMT', 'class': 'form-control mb-3'}))
    cyk_summa_dol = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Zakaz_SapakSwotka
        fields = ('cyk_summa','cyk_summa_dol','bellik')

class SapakSeh_TabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SapakSeh_TabelForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Işgäri saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez="1"), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    oklady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Oklady', 'class': 'form-control mb-3'}))
    ay_isguni = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Aydaky iş güni', 'class': 'form-control mb-3'}))
    gune_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bir güne düşýän haky', 'class': 'form-control mb-3'}))
    is_gun_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Iş gün sagady', 'class': 'form-control mb-3'}))
    sagat_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Sagadyna düşýän haky', 'class': 'form-control mb-3'}))
    is_gun_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Işlän gün sany', 'class': 'form-control mb-3'}))
    artyk_is_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Artyk işlän sagasy', 'class': 'form-control mb-3'}))
    awans = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans', 'class': 'form-control mb-3'}))
    kart_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Kartyna geçýän summa', 'class': 'form-control mb-3'}))
    el_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Eline almaly summa"', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Halta_seh_ay_tabel
        fields = ('user','oklady','ay_isguni','gune_dusyan_haky','is_gun_sagady','sagat_dusyan_haky','is_gun_sany','artyk_is_sagady','awans','kart_sum','el_sum','bellik')

class Aydaky_sapakForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aydaky_sapakForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Sapagyň görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_cyk_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi ayda sapagyň kg', 'class': 'form-control mb-3'}))
    jemi_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky hardyň bahasy TMT', 'class': 'form-control mb-3'}))
    jemi_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky hardyň bahasy $', 'class': 'form-control mb-3'}))

    class Meta:
        model = Aydaky_sapak
        fields = ('d_gornusi','jemi_cyk_kg','jemi_bahasy_m','jemi_bahasy_d')

class AydakySapak_hasabatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AydakySapak_hasabatForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Sapagyň görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    jemi_dok_sapak = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky sapagyň kg', 'class': 'form-control mb-3'}))
    satylan_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan sapagyň kg', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ahyrky galyndy kg', 'class': 'form-control mb-3'}))
    yerinde_bar_haryt = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ýerinde bar harydyň kg', 'class': 'form-control mb-3'}))
    tapawudy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Aýdaky tapawut', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = AydakySapak_hasabat
        fields = ('d_gornusi','gecenay_galyndy','jemi_dok_sapak','satylan_sapak_kg','wozwrat','ahyrky_galyndy','yerinde_bar_haryt','tapawudy','bellik')


# Dokma SEH
class GunDokmaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GunDokmaForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Kim işlän saýlaň")
        self.fields['d_gornusi'].empty_label = _("Dokmanyň görnüşini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh=3), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    cykrulon_kg = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň kg', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň bahasy TMT', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň bahasy $', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Katuskaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_dokma
        fields = ('user','d_gornusi','cykrulon_kg','cykrulon_bahasy_m','cykrulon_bahasy_d','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class ZakazDokmaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakazDokmaForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Kim işlän saýlaň")
        self.fields['zakaz_user'].empty_label = _("Zakazçyny saýlaň")
        self.fields['d_gornusi'].empty_label = _("Dokmanyň görnüşini saýlaň")
        self.fields['zakaz_code'].empty_label = _("Zakazyň belgisini saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez=1,seh__pr_seh=3), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_user = forms.ModelChoiceField(Other_users.objects.filter(wez=3,seh__pr_seh=3), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    zakaz_code = forms.ModelChoiceField(Zakaz_balans.objects,label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    cykrulon_kg = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň kg', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_m = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň bahasy TMT', 'class': 'form-control mb-3'}))
    cykrulon_bahasy_d = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykan rulonyň bahasy $', 'class': 'form-control mb-3'}))
    wozwrat_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Wozwrat kg', 'class': 'form-control mb-3'}))
    katyska_agram = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Katuskaň agramy kg', 'class': 'form-control mb-3'}))
    nirden_gelen = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Nirden gelen rulon', 'class': 'form-control mb-3'}))
    enjam = forms.CharField(label=False, required=False,widget=forms.TextInput(attrs={'placeholder': 'Haysy enjamda dokalan', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Gundelik_dokma
        fields = ('user','zakaz_user','zakaz_code','d_gornusi','cykrulon_kg','cykrulon_bahasy_m','cykrulon_bahasy_d','wozwrat_kg','katyska_agram','nirden_gelen','enjam','bellik')

class AyjemDokmaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AyjemDokmaUpdateForm,self).__init__(*args, **kwargs)

    yerinde_bar_haryt = forms.DecimalField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = AydakyDokma_hasabat
        fields = ('yerinde_bar_haryt','bellik')

class ZakSwotkaDokmaUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ZakSwotkaDokmaUpdateForm,self).__init__(*args, **kwargs)

    cyk_summa = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy TMT', 'class': 'form-control mb-3'}))
    cyk_summa_dol = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Çykdaýjy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Zakaz_DokmaSwotka
        fields = ('cyk_summa','cyk_summa_dol','bellik')

class DokmaSeh_TabelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DokmaSeh_TabelForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Işgäri saýlaň")

    user = forms.ModelChoiceField(Other_users.objects.filter(wez="1"), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    oklady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    ay_isguni = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt', 'class': 'form-control mb-3'}))
    gune_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    is_gun_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    sagat_dusyan_haky = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    is_gun_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Ýerinde bar bolan haryt', 'class': 'form-control mb-3'}))
    artyk_is_sagady = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    awans = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    kart_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    el_sum = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tölän puly manat', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Halta_seh_ay_tabel
        fields = ('user','oklady','ay_isguni','gune_dusyan_haky','is_gun_sagady','sagat_dusyan_haky','is_gun_sany','artyk_is_sagady','awans','kart_sum','el_sum','bellik')

class Aydaky_dokmaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aydaky_dokmaForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Önümiň görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    jemi_cyk_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi ayda rulonyň kg', 'class': 'form-control mb-3'}))
    jemi_bahasy_m = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky rulonyň bahasy TMT', 'class': 'form-control mb-3'}))
    jemi_bahasy_d = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aydaky rulonyň bahasy $', 'class': 'form-control mb-3'}))

    class Meta:
        model = Aydaky_dokma
        fields = ('d_gornusi','jemi_cyk_kg','jemi_bahasy_m','jemi_bahasy_d')

class AydakyDokma_hasabatForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AydakyDokma_hasabatForm,self).__init__(*args, **kwargs)
        self.fields['d_gornusi'].empty_label = _("Önümiň görnüşini saýlaň")

    d_gornusi = forms.ModelChoiceField(Halta_gornus.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    gecenay_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Geçen aýdaky galyndy', 'class': 'form-control mb-3'}))
    jemi_dok_rulon = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky rulonyň kg', 'class': 'form-control mb-3'}))
    satylan_sapak_kg = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky satylan rulonyň kg', 'class': 'form-control mb-3'}))
    wozwrat = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky wozwrat', 'class': 'form-control mb-3'}))
    ahyrky_galyndy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ahyrky galyndy kg', 'class': 'form-control mb-3'}))
    yerinde_bar_haryt = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Jemi aýdaky ýerinde bar harydyň kg', 'class': 'form-control mb-3'}))
    tapawudy = forms.DecimalField(label=False, required=False,widget=forms.NumberInput(attrs={'placeholder': 'Aýdaky tapawut', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = AydakyDokma_hasabat
        fields = ('d_gornusi','gecenay_galyndy','jemi_dok_rulon','satylan_sapak_kg','wozwrat','ahyrky_galyndy','yerinde_bar_haryt','tapawudy','bellik')



# Hasaphana
class Aylyk_PremyaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aylyk_PremyaForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Işgär")

    user = forms.ModelChoiceField(AllUsers.objects.filter(is_superuser=False), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi TMT', 'class': 'form-control mb-3'}))
    summa_dollar = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Aylyk_premya
        fields = ('user', 'summa_m','summa_dollar','sebap', 'bellik')

class Aylyk_Premya_editForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Aylyk_Premya_editForm,self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _("Işgär")

    user = forms.ModelChoiceField(AllUsers.objects.filter(is_superuser=False), label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi TMT', 'class': 'form-control mb-3'}))
    summa_dollar = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi $', 'class': 'form-control mb-3'}))
    awans_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans TMT', 'class': 'form-control mb-3'}))
    awans_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Awans $', 'class': 'form-control mb-3'}))
    jemi_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi TMT', 'class': 'form-control mb-3'}))
    jemi_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Aylyk_premya
        fields = ('user', 'summa_m','summa_dollar','awans_m','awans_d','jemi_m','jemi_d','sebap', 'bellik')

class Das_karz_alynanpulForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_karz_alynanpulForm,self).__init__(*args, **kwargs)

    karzcy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Kime bermeli we kimden almaly karz puly', 'class': 'form-control mb-3'}))
    b_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi berlen TMT', 'class': 'form-control mb-3'}))
    b_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi berlen $', 'class': 'form-control mb-3'}))
    a_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan TMT', 'class': 'form-control mb-3'}))
    a_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_karz_alynanpul
        fields = ('karzcy','a_summa_m','a_summa_d','b_summa_m','b_summa_d','sebap', 'bellik')

class Karz_AlynanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Karz_AlynanForm,self).__init__(*args, **kwargs)

    karzcy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Kimden almaly karz puly', 'class': 'form-control mb-3'}))
    a_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan TMT', 'class': 'form-control mb-3'}))
    a_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_karz_alynanpul
        fields = ('karzcy', 'a_summa_m','a_summa_d','sebap', 'bellik')

class Karz_Alynan_editForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Karz_Alynan_editForm,self).__init__(*args, **kwargs)

    karzcy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Kimden almaly karz puly', 'class': 'form-control mb-3'}))
    a_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan TMT', 'class': 'form-control mb-3'}))
    a_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan $', 'class': 'form-control mb-3'}))
    jemi_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi TMT', 'class': 'form-control mb-3'}))
    jemi_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_karz_alynanpul
        fields = ('karzcy', 'a_summa_m','a_summa_d','jemi_m','jemi_d','sebap', 'bellik')


class Karz_BerilenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Karz_BerilenForm,self).__init__(*args, **kwargs)

    b_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi berlen TMT', 'class': 'form-control mb-3'}))
    b_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi berlen $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Karz_yzyna_berilen
        fields = ('b_summa_m','b_summa_d','sebap', 'bellik')

class Karz_yzyna_berilenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Karz_yzyna_berilenForm,self).__init__(*args, **kwargs)

    karzcy = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Kimden almaly karz puly', 'class': 'form-control mb-3'}))
    b_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan TMT', 'class': 'form-control mb-3'}))
    b_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi alynan $', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Karz_yzyna_berilen
        fields = ('karzcy', 'b_summa_m','b_summa_d','sebap', 'bellik')

class ExportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExportForm,self).__init__(*args, **kwargs)
        self.fields['kimden'].empty_label = _("Kimiň adyndan gitdi")

    kimden = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kime = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Giden edara-kähananyň ady', 'class': 'form-control mb-3'}))
    deklorasiya_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Diklarasiýa belgisi', 'class': 'form-control mb-3'}))
    name_haryt = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Näme haryt gitdi', 'class': 'form-control mb-3'}))
    summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy TMT', 'class': 'form-control mb-3'}))
    summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Export_yukler
        fields = ('kimden','kime','deklorasiya_nomer','name_haryt','summa_m','summa_d','bellik')

class ImportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImportForm,self).__init__(*args, **kwargs)
        self.fields['kimden'].empty_label = _("Kimden alyndy")
        self.fields['kime'].empty_label = _("Kime geçirildi")

    kimden = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    kime = forms.ModelChoiceField(AllUsers.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    a_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Alynan pul TMT', 'class': 'form-control mb-3'}))
    a_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Alynan pul $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Import_yukpul
        fields = ('kimden','kime','a_summa_m','a_summa_d','bellik')

class Import_updateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Import_updateForm,self).__init__(*args, **kwargs)

    g_summa_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Geçirilen pul TMT', 'class': 'form-control mb-3'}))
    g_summa_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Geçirilen pul $', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Import_yukpul
        fields = ('g_summa_m','g_summa_d')


class ManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManagerForm,self).__init__(*args, **kwargs)
        self.fields['seh'].empty_label = _("Haýsy sehiň klienti")

    faa = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    seh = forms.ModelChoiceField(Sehler.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    birth_date = forms.DateTimeField(label=False, required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Öý salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = Manager_user
        fields = ('faa','seh','birth_date','address')

class Manager_zakazForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Manager_zakazForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    shertnama_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    z_sany = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň şertnama möçberi', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_yurt_klientler
        fields = ('harydyn_ady','shertnama_nomer','z_sany','bahasy_m','bahasy_d','bellik')

class Manager_zakaz_editForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Manager_zakaz_editForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    shertnama_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    z_sany = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň şertnama möçberi', 'class': 'form-control mb-3'}))
    bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy TMT', 'class': 'form-control mb-3'}))
    bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Bahasy $', 'class': 'form-control mb-3'}))
    zj_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy TMT', 'class': 'form-control mb-3'}))
    zj_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy $', 'class': 'form-control mb-3'}))
    tapawut_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tapawudy TMT', 'class': 'form-control mb-3'}))
    tapawut_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tapawudy $', 'class': 'form-control mb-3'}))
    peyda_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi galýan peýda TMT', 'class': 'form-control mb-3'}))
    peyda_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi galýan peýda $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_yurt_klientler
        fields = ('harydyn_ady','shertnama_nomer','z_sany','bahasy_m','bahasy_d','zj_bahasy_m','zj_bahasy_d','tapawut_m','tapawut_d','peyda_m','peyda_d','bellik')

class Manager_zakazUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Manager_zakazUpdateForm,self).__init__(*args, **kwargs)

    i_sany = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Işlenen harydyň möçberi', 'class': 'form-control mb-3'}))
    cykdajy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi çykdajy TMT', 'class': 'form-control mb-3'}))
    cykdajy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi çykdajy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_yurt_klientler
        fields = ('i_sany','cykdajy_m','cykdajy_d','bellik')

class Das_yurt_klient_cykdajyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_yurt_klient_cykdajyForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    shertnama_nomer = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Şertnama belgisi', 'class': 'form-control mb-3'}))
    i_sany = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň şertnama möçberi', 'class': 'form-control mb-3'}))
    j_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy TMT', 'class': 'form-control mb-3'}))
    j_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi bahasy TMT', 'class': 'form-control mb-3'}))
    cykdajy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi çykdajy TMT', 'class': 'form-control mb-3'}))
    cykdajy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi çykdajy $', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Das_yurt_klient_cykdajy
        fields = ('harydyn_ady','shertnama_nomer','i_sany','j_bahasy_m','j_bahasy_d','cykdajy_m','cykdajy_d')


class Wal_bolumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Wal_bolumForm,self).__init__(*args, **kwargs)

    name = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Walýuta hasabyň ady', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Walyuta_hasap
        fields = ('name',)

class Bank_userForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Bank_userForm,self).__init__(*args, **kwargs)

    name = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'F.A.A', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Telefon belgisi', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))

    class Meta:
        model = Bank_user
        fields = ('name','tel','address')

class BankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BankForm,self).__init__(*args, **kwargs)

    shet_nomer = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Walýutaň hasap belgisi', 'class': 'form-control mb-3'}))
    g_summa = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi gelen pul', 'class': 'form-control mb-3'}))
    c_summa = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Jemi giden pul', 'class': 'form-control mb-3'}))
    sebap = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Sebabi', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Bank
        fields = ('shet_nomer','g_summa','c_summa','sebap','bellik')


class SehlerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SehlerForm,self).__init__(*args, **kwargs)
        self.fields['office'].empty_label = _("Welaýaty saýlaň")
    
    office = forms.ModelChoiceField(Office.objects, label=False, widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Sehiň ady', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Telefon belgisi', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Sehler
        fields = ('office','name','tel','address')


# Daşyndan işleşilýän zawodlar

class Das_ZawodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_ZawodForm,self).__init__(*args, **kwargs)

    name = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Zawodyň ady', 'class': 'form-control mb-3'}))
    tel = forms.CharField(label=False,required=False, widget=forms.TextInput(attrs={'placeholder': 'Telefon belgisi', 'class': 'form-control mb-3'}))
    address = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Salgysy', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_zawod
        fields = ('name','tel','address')

class Das_isleyan_zawodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_isleyan_zawodForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    b_haryt_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    b_haryt_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Haryt kg', 'class': 'form-control mb-3'}))
    b_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen bahasy TMT', 'class': 'form-control mb-3'}))
    b_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen bahasy $', 'class': 'form-control mb-3'}))
    
    class Meta:
        model = Das_isleyan_zawodlar
        fields = ('harydyn_ady','b_haryt_sany','b_haryt_kg','b_bahasy_m','b_bahasy_d')

class Das_isleyan_zawod_editForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_isleyan_zawod_editForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    b_haryt_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    b_haryt_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Haryt kg', 'class': 'form-control mb-3'}))
    b_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen bahasy TMT', 'class': 'form-control mb-3'}))
    b_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen bahasy $', 'class': 'form-control mb-3'}))
    g_haryt_sany = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Galan harydyň sany', 'class': 'form-control mb-3'}))
    g_haryt_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Galan harydyň kg', 'class': 'form-control mb-3'}))
    satylan_haryt_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Satylan harydyň sany', 'class': 'form-control mb-3'}))
    satylan_haryt_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Satylan harydyň kg', 'class': 'form-control mb-3'}))
    b_jemi_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen jemi bahasy TMT', 'class': 'form-control mb-3'}))
    b_jemi_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Berilen jemi bahasy $', 'class': 'form-control mb-3'}))
    tapawut_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tapawudy TMT', 'class': 'form-control mb-3'}))
    tapawut_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Tapawudy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_isleyan_zawodlar
        fields = ('harydyn_ady','b_haryt_sany','b_haryt_kg','b_bahasy_m','b_bahasy_d','g_haryt_sany','g_haryt_kg','satylan_haryt_sany','satylan_haryt_kg','b_jemi_bahasy_m','b_jemi_bahasy_d','tapawut_m','tapawut_d','bellik')


class Das_isleyan_zawod_UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_isleyan_zawod_UpdateForm,self).__init__(*args, **kwargs)

    a_haryt_sany = forms.IntegerField(label=False,required=False,widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    a_haryt_kg = forms.DecimalField(label=False,required=False,widget=forms.NumberInput(attrs={'placeholder': 'Haryt kg', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False,widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_is_zawod_Alynan
        fields = ('a_haryt_sany','a_haryt_kg','bellik')

class Das_is_zawod_AlynanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Das_is_zawod_AlynanForm,self).__init__(*args, **kwargs)

    harydyn_ady = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Harydyň ady', 'class': 'form-control mb-3'}))
    a_haryt_sany = forms.IntegerField(label=False, widget=forms.NumberInput(attrs={'placeholder': 'Harydyň sany', 'class': 'form-control mb-3'}))
    a_haryt_kg = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Haryt kg', 'class': 'form-control mb-3'}))
    a_jemi_bahasy_m = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Alynan bahasy TMT', 'class': 'form-control mb-3'}))
    a_jemi_bahasy_d = forms.DecimalField(label=False,required=False, widget=forms.NumberInput(attrs={'placeholder': 'Alynan bahasy $', 'class': 'form-control mb-3'}))
    bellik = forms.CharField(label=False,required=False, widget=forms.Textarea(attrs={'placeholder': 'Bellik', 'class': 'form-control mb-3', 'style': 'height:100px;'}))
    
    class Meta:
        model = Das_is_zawod_Alynan
        fields = ('harydyn_ady','a_haryt_sany','a_haryt_kg','a_jemi_bahasy_m','a_jemi_bahasy_d','bellik')


    
