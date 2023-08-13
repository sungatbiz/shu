from itertools import chain
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, OjUpdateForm
from django.contrib.auth import login as django_login, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, date
from users.models import Office
from shu.models import *
from django.db.models import Sum, Avg, Count
from django.urls import reverse
from .models import *
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.http import HttpResponseRedirect
import logging
from django.utils.module_loading import import_string
from django.contrib.auth.signals import user_logged_in, user_logged_out 
from django.dispatch import receiver 
import os
from pathlib import Path
from users.forms import *
from django.db.models import Q
import decimal
from django.db.models.functions import TruncMonth
from django.db.models import Sum, F, FloatField, Count

# logger = logging.getLogger("main")
# BASE_DIR = Path(__file__).resolve().parent.parent
# LOG_PATH = os.path.join(BASE_DIR, "log/")

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Ulanyjylar')
            user.is_staff = True
            user.groups.add(group)
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Siziň akauntyňyz döredildi {username}')
            # logger.info('Taze ulanyjy girizildi!' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
            return redirect('login')
    else:
        # logger.info('Taze ulanyjy girizilmedi! - (Maglumaty doly girizilmedi ya-da ulanyjy ulgamda)' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class LoginFormView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        user = AllUsers.objects.get(id=self.request.user.id)
        if user.wez.name=="Admin":
            messages.success(self.request, f'Hoş geldiňiz {user.last_name} {user.first_name}')
            return reverse('dashboard')
        if user.wez.name=="Işgärler bölüminiň hünärmeni":
            messages.success(self.request, f'Hoş geldiňiz {user.last_name} {user.first_name}')
            return reverse('office-kadr')
        if user.wez.name=="Işgärler bölüminiň başlygy":
            messages.success(self.request, f"Hoş geldiňiz  {user.last_name} {user.first_name}")
            return reverse('office-kadr')
        if user.wez.name=="Hasaphana hünärmeni":
            messages.success(self.request, f"Hoş geldiňiz  {user.last_name} {user.first_name}")
            return reverse('hasaphana',args=[user.pk])
        if user.wez.name=="Baş hasapçy":
            messages.success(self.request, f"Hoş geldiňiz  {user.last_name} {user.first_name}")
            return reverse('hasaphana',args=[user.pk])
        if user.wez.name=="Seh hasapçy":
            messages.success(self.request, f"Hoş geldiňiz  {user.last_name} {user.first_name}")
            return reverse('sehler')
        if user.wez.name=="Ulanyjylar":
            messages.success(self.request, f"Hoş geldiňiz  {user.last_name} {user.first_name}")
            return reverse('profile')

# return reverse('hukuk-home', args=[user.sehs_id]) 

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        # logger.error('Ulgama girmek synanshygy' + " - IP: " + self.request.META.get('REMOTE_ADDR', '') + ":" + self.request.META['SERVER_PORT'])
        return self.render_to_response(ctx)

# @receiver(user_logged_in) 
# def _user_logged_in(sender, user, request, **kwargs):
#     logger.info(request.user.username + ' - ulanyjy ulgama girdi!' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
#     # if request.user.is_authenticated():
#     #     logger.info(request.user.username + ' - ulanyjy ulgamda!' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
#     # else:
#         # logger.error(request.user.username + ' - ulanyjy ulgamda!' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
    
# @receiver(user_logged_out) 
# def _user_logged_out(sender, user, request, **kwargs):
#     logger.info(request.user.username + ' - ulanyjy ulgamdan cykdy!' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])

@login_required(login_url='login')
def Profile(request):
    page_title = _('Şahsy otag')
    user = request.user
    oj=Ojidanie.objects.all()
    b_has=Bolek_hasaplar.objects.filter(Q(user=user) | Q(user_sent=user)).all()
    
    total = Bolek_hasaplar.objects.filter(Q(user=user) | Q(user_sent=user)).aggregate(total=Sum(F('girdeji')))['total']
    total_d = Bolek_hasaplar.objects.filter(Q(user=user) | Q(user_sent=user)).aggregate(total=Sum(F('girdeji_dollar')))['total']

    total_cyk = Bolek_hasaplar.objects.filter(Q(user=user) | Q(user_sent=user)).aggregate(total=Sum(F('cykdajy')))['total']
    total_cyk_d = Bolek_hasaplar.objects.filter(Q(user=user) | Q(user_sent=user)).aggregate(total=Sum(F('cykdajy_dollar')))['total']
    
    paginator = Paginator(b_has, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)
    
    context = {'title': page_title,'myuser':myuser,'oj':oj, 'b_has':b_has,'total':total,'total_d':total_d,'total_cyk':total_cyk,'total_cyk_d':total_cyk_d}
    return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def delete_oj(request, pk):
    record = Ojidanie.objects.get(pk=pk)
    record.delete()
    return redirect('profile')

# @login_required(login_url='login')
# def update_myuser(request):
#     obj = AllUsers.objects.get(id=request.user)
#     form = UserUpdateForm(instance=obj)
    
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, request.FILES, instance=obj)
#         if form.is_valid():
#            form.save()
#         #    logger.info(request.user.username + ' - ulanyjy tarapyndan: Degishli ulanyjynyn maglumatlary uytgedildi' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
#            return redirect('Profile')
#     else:
#         # logger.warning(request.user.username + ' - ulanyjy tarapyndan: Degishli ulanyjynyn maglumatlary uytgedilmedi "YALNYSHLYK"' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
#         form = UserUpdateForm(instance=obj)
#     return render(request, 'ezd/user_edit.html', {'form': form})


# def gozle_user(request):
#     user_cur_office = request.user.trudlar.get(cyk="")
#     if request.method == "POST":
#         gozle = request.POST['gozle']

#         myuser = AllUsers.objects.filter(is_superuser=False)

#         office_users = []
#         for deg in myuser:
#             deg_cur = Trud.objects.filter(user=deg.id).order_by('id').reverse()[0]
#             if deg_cur.cyk == "" and deg_cur.office.id == user_cur_office.office.id:
#                 office_users.append(deg)

#         gozle_users = AllUsers.objects.filter(user_code__contains=gozle)

#         return render(request, 'users/gozle_user.html', {'gozle':gozle, "gozle_users":gozle_users, 'office_users': office_users,})
#     else:
#         logger.warning(request.user.username + ' - ulanyjy maglumat gozledi! "YALNYSHLYK"' + ": " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
#         context = {}
#         return render(request, 'users/gozle_user.html', context)

# def Loglar(request):
#     f = open(LOG_PATH + "loggers.log", "r")
#     context = {'f': f,}
#     return render(request, 'users/my_logs.html', context)

@login_required(login_url='login')
def Zakaz_sanaw(request):
    page_title = _('Zakazçylar sanawy')
    zakazcylar = Other_users.objects.filter(wez=3)

    if request.method == 'POST':
        form2 = ZakazcyAddForm(request.POST, request.FILES)
        form = ZakazForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('zakaz-users')
        if form2.is_valid():
            seh=form2.cleaned_data['seh']
            faa=form2.cleaned_data['faa']
            birth_date=form2.cleaned_data['birth_date']
            address=form2.cleaned_data['address']

            zakcyadd = Other_users.objects.create(seh=seh,faa=faa,birth_date=birth_date,address=address)
            zakcyadd.save()
            messages.success(request, f'{faa} täze zakazçy girizildi!')
            return redirect('zakaz-users')
    else:
        form = ZakazForm()
        form2 = ZakazcyAddForm()


    paginator = Paginator(zakazcylar, 10) 
    page = request.GET.get('page')
    try:
        zakaz_user = paginator.get_page(page)
    except PageNotAnInteger:
        zakaz_user = paginator.page(1)
    except EmptyPage:
        zakaz_user = paginator.page(paginator.num_pages)

    context = {'title': page_title,'zakaz_user':zakaz_user,'form': form,'form2': form2}
    return render(request, 'shu/zakaz_users.html', context)

@login_required(login_url='login')
def Zakaz_detail(request, pk):
    page_title = _('Zakazçynyň giňişleýin hasabatlary')
    zak_user = Other_users.objects.get(id=pk)
    user_hasaby=Zakaz_balans.objects.filter(user=pk).order_by("zakaz_sene")

    sapak_satylan = Sapakseh_sklad_satylan.objects.filter(zakaz_user_id=pk).order_by("sene")
    dokma_satylan = Dokmaseh_sklad_satylan.objects.filter(zakaz_user_id=pk).order_by("sene")
    halta_satylan = Haltaseh_sklad_satylan.objects.filter(zakaz_user_id=pk).order_by("sene")
  
    win=list(chain(sapak_satylan,dokma_satylan,halta_satylan))
    kim=[]
    for x in win:
        if x.zakaz_user.pk==pk:
            kim.append(x)
        break

    if request.method == 'POST':
        form = ZakazForm(request.POST, request.FILES)
        
        if form.is_valid():
            h_gornusi = form.cleaned_data['h_gornusi']
            h_olceg = form.cleaned_data['h_olceg']
            sany = form.cleaned_data['sany']
            bahasy = form.cleaned_data['bahasy']
            tolenen_pul = form.cleaned_data['tolenen_pul']
            bellik = form.cleaned_data['bellik']
            if tolenen_pul == 0 or tolenen_pul == None:
                zak = Zakaz_balans.objects.create(seh=zak_user.seh,bergi=sany*bahasy,user=zak_user,h_gornusi=h_gornusi,h_olceg=h_olceg,sany=sany,bahasy=bahasy,balans=sany*bahasy,algy=sany*bahasy,tolenen_pul=tolenen_pul,bellik=bellik)
                zak.save()
            elif tolenen_pul > 0:
                zak = Zakaz_balans.objects.create(seh=zak_user.seh,bergi=sany*bahasy-tolenen_pul,user=zak_user,h_gornusi=h_gornusi,h_olceg=h_olceg,sany=sany,bahasy=bahasy,balans=sany*bahasy,algy=sany*bahasy,tolenen_pul=tolenen_pul,bellik=bellik)
                zak.save()
            return redirect('zakazusers-detail', pk)
    else:
        form = ZakazForm()
        form2 = ZakUpdateForm()

    # test2=Aydaky_halta.objects.filter(zakaz_user=pk).select_related('h_gornusi').annotate(
    #         month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg')).annotate(zakazcy=F('zakaz_code')).values('month','gornus','olceg','zakazcy').annotate(
    #             jemi_sany=Sum(F("jemi_sany"))).annotate(jemi_kg=Sum(F("jemi_kg"))).annotate(jemi_bahasy_m=Sum(F("jemi_bahasy_m"))).annotate(jemi_bahasy_d=Sum(F("jemi_bahasy_d")))

    # paginator = Paginator(gun_hal, 10) 
    # page = request.GET.get('page')
    # try:
    #     myuser = paginator.get_page(page)
    # except PageNotAnInteger:
    #     myuser = paginator.page(1)
    # except EmptyPage:
    #     myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'form': form, 'form2': form2,
               'user_hasaby':user_hasaby,'zak_user':zak_user,
               'sapak_satylan':sapak_satylan,'dokma_satylan':dokma_satylan,
               'halta_satylan':halta_satylan,'win':win,'kim':kim}
    return render(request, 'shu/zakaz_users_detail.html', context)

def load_zakupdate(request, pk):
    page_title = _('Zakaz tölegi geçirmek')

    test = Zakaz_balans.objects.filter(id=pk)
    zz=Other_users.objects.all()

    cur_user = []
    for deg in test:
        if Other_users.objects.filter(id=deg.user.id):
            d=deg.user.id
            cur_user.append({'d':d})
    
    if request.method == 'POST':
        form = ZakUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            tolenen_pul = form.cleaned_data['tolenen_pul']
            bellik = form.cleaned_data['bellik']
            obj = Zakaz_balans.objects.get(id=pk)
            if obj.tolenen_pul > 0:
                obj.tolenen_pul = tolenen_pul + obj.tolenen_pul
                obj.bergi = obj.bergi - tolenen_pul
                obj.bellik=bellik
                obj.toleg_sene=timezone.now()
                obj.save()
                return redirect('zakazusers-detail', d)
            else:
                obj.tolenen_pul = tolenen_pul
                obj.bergi = obj.bergi - tolenen_pul
                obj.bellik=bellik
                obj.toleg_sene=timezone.now()
                obj.save()
                return redirect('zakazusers-detail', d)
    else:
        form = ZakUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

def Zakaz_balans_edit(request, pk):
    page_title = _('Zakazçynyň hasabyny üýtgetmek')
    obj = Zakaz_balans.objects.get(id=pk)
    
    if request.method == 'POST':
        form = ZakazForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Zakazçynyň hasabyny üýtgedildi!')
           return redirect('zakazusers-detail', pk)
    else:
        form = ZakazForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

