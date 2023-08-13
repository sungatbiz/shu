from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.forms import *
from .models import *
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from datetime import datetime, date
from django.db.models import Sum
from io import BytesIO
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
from django.views import View
import io
from django.db.models import Sum, F, FloatField, Count,When, Case, IntegerField
from django.db.models.functions import ExtractMonth
from django.db.models.functions import TruncMonth, TruncDay
from django.contrib.auth.decorators import login_required, permission_required
from mydocor.auth import group_required
from django.db import connection
from django.contrib.auth.models import Group
from django.forms import formset_factory
from django.db.models import Q
from django.utils.translation import gettext as _
import logging
from django.urls import reverse, reverse_lazy
from decimal import *
from django import template
from django.contrib import messages
from statistics import mean
from itertools import chain
from typing import Union
import functools
from django.views.generic.base import RedirectView
import re
# import time


# logger = logging.getLogger("main")



@login_required(login_url='login')
def home(request):
    # print(request.META.get('HTTP_COOKIE'), request.META.get('CSRF_COOKIE'), request.META.get('REMOTE_ADDR', ''))
    # from django.utils import translation
    # if translation.LANGUAGE_SESSION_KEY in request.session:
    #     del request.session[translation.LANGUAGE_SESSION_KEY]
    
    # logger.info('Bash sahypa girildi!' + " - " + request.META.get('REMOTE_ADDR', '') + ":" + request.META['SERVER_PORT'])
    # return redirect('login')
    return render(request, 'shu/test.html')


# Hasaphana

@login_required(login_url='login')
def Hasaphana_admin(request):
    page_title = _('Hasaphana bölümi')
    cur_user = request.user
    b_has=Bolek_hasaplar.objects.all()
    oj=Ojidanie.objects.all()
    user_oj=AllUsers.objects.all()
    tot_b=Bolek_hasaplar.objects.aggregate(gir_m=Sum((F("girdeji"))),gir_d=Sum((F("girdeji_dollar"))),cyk_m=Sum((F("cykdajy"))),cyk_d=Sum((F("cykdajy_dollar"))))
    
    gal_d=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji_dollar')) - Sum(F('cykdajy_dollar')))['total']
    gal_m=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji')) - Sum(F('cykdajy')))['total']

    if request.method == 'POST':
        form2 = OjSentForm(request.POST, request.FILES)
        form3 = B_hasapForm(request.POST, request.FILES)
        
        if form2.is_valid():
            u_came_id = form2.cleaned_data['u_came_id']
            cash = form2.cleaned_data['cash']
            cash_d = form2.cleaned_data['cash_d']
            awans_m = form2.cleaned_data['awans_m']
            awans_d = form2.cleaned_data['awans_d']
            sebap = form2.cleaned_data['sebap']
            bellik = form2.cleaned_data['bellik']
            
            oj_create = Ojidanie.objects.create(u_sent_id=cur_user,u_came_id=u_came_id,cash=cash,cash_d=cash_d,awans_m=awans_m,awans_d=awans_d,sebap=sebap,bellik=bellik)
            oj_create.save()
            b = Bolek_hasaplar.objects.create(user_sent=cur_user,cykdajy=cash,cykdajy_dollar=cash_d,sebap=sebap,bellik=bellik)
            b.save()
            return redirect('hasaphana-admin')
        
        if form3.is_valid():
            girdeji=form3.cleaned_data['girdeji']
            cykdajy = form3.cleaned_data['cykdajy']
            sebap = form3.cleaned_data['sebap']
            bellik = form3.cleaned_data['bellik']
            cykdajy_dollar=form3.cleaned_data['cykdajy_dollar']
            girdeji_dollar=form3.cleaned_data['girdeji_dollar']

            b = Bolek_hasaplar.objects.create(user=cur_user,girdeji=girdeji,girdeji_dollar=girdeji_dollar,cykdajy=cykdajy,cykdajy_dollar=cykdajy_dollar,sebap=sebap,bellik=bellik)
            b.save()
            return redirect('hasaphana-admin')
    else:
        form2 = OjSentForm()
        form3 = B_hasapForm()
    
    paginator = Paginator(b_has, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'tot_b':tot_b, 'oj':oj,'form2': form2, 'form3':form3,'gal_m':gal_m,'gal_d':gal_d}
    return render(request, 'shu/hasaphana_admin.html', context)

@login_required(login_url='login')
def Bolek_hasaplar_edit(request, pk):
    page_title = _('Bölek hasaby üýtgetmek')
    obj = Bolek_hasaplar.objects.get(id=pk)
    
    if request.method == 'POST':
        form = B_hasapForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Bölek hasaby üýtgedildi!')
           return redirect('hasaphana-admin')
    else:
        form = B_hasapForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


# @group_required(['Hasaphana hünärmeni','Baş hasapçy','Başlyk','Admin'])
# @group_required(['Admin','Baş hasapçy'])
@login_required(login_url='login')
def Hasaphana(request,pk):
    page_title = _('Hasaphana bölümi')
    cur_user = request.user
    b_has=Bolek_hasaplar.objects.filter(Q(user_id=pk) | Q(user_sent_id=pk))
    oj=Ojidanie.objects.filter(Q(u_came_id=cur_user),Q(tassyk=0))
    user_oj=AllUsers.objects.filter(is_superuser=False)
    
    tot_b=Bolek_hasaplar.objects.filter(Q(user=cur_user) | Q(user_sent=cur_user) | Q(user_id=pk) | Q(user_sent_id=pk)).aggregate(gir_m=Sum((F("girdeji"))),gir_d=Sum((F("girdeji_dollar"))),cyk_m=Sum((F("cykdajy"))),cyk_d=Sum((F("cykdajy_dollar"))),gal_m=Sum((F("girdeji") - F("cykdajy"))),gal_d=Sum((F("girdeji_dollar") - F("cykdajy_dollar"))))
    gal_d=Bolek_hasaplar.objects.filter(Q(user=cur_user) | Q(user_sent=cur_user) | Q(user_id=pk) | Q(user_sent_id=pk)).aggregate(total=Sum(F('girdeji_dollar')) - Sum(F('cykdajy_dollar')))
    gal_m=Bolek_hasaplar.objects.filter(Q(user=cur_user) | Q(user_sent=cur_user) | Q(user_id=pk) | Q(user_sent_id=pk)).aggregate(total=Sum(F('girdeji')) - Sum(F('cykdajy')))
    
    cur_oj = []
    for deg in oj:
        if deg.tassyk == 0 and deg.u_sent_id.id==cur_user.id or deg.u_came_id==cur_user.id:
            cur_oj.append(deg)

    if request.method == 'POST':
        form2 = OjSentForm(request.POST, request.FILES)
        form3 = B_hasapForm(request.POST, request.FILES)
        
        if form2.is_valid():
            u_came_id = form2.cleaned_data['u_came_id']
            cash = form2.cleaned_data['cash']
            cash_d = form2.cleaned_data['cash_d']
            awans_m = form2.cleaned_data['awans_m']
            awans_d = form2.cleaned_data['awans_d']
            sebap = form2.cleaned_data['sebap']
            bellik = form2.cleaned_data['bellik']
            
            if awans_m is not None or awans_d is not None:
                oj_create = Ojidanie.objects.create(u_sent_id=cur_user,u_came_id=u_came_id,cash=cash,cash_d=cash_d,awans_m=awans_m,awans_d=awans_d,sebap=sebap,bellik=bellik)
                oj_create.save()
            else:
                oj_create = Ojidanie.objects.create(u_sent_id=cur_user,u_came_id=u_came_id,cash=cash,cash_d=cash_d,sebap=sebap,bellik=bellik)
                oj_create.save()
            obj = Ojidanie.objects.last() #get(u_sent_id=cur_user.id)
            b = Bolek_hasaplar.objects.create(oj_id=obj.pk,user_sent=cur_user,cykdajy=cash,cykdajy_dollar=cash_d,sebap=sebap,bellik=bellik)
            b.save()
            return redirect('hasaphana',pk)
        if form3.is_valid():
            # awans=bhasap_form.cleaned_data['awans']
            girdeji=form3.cleaned_data['girdeji']
            cykdajy = form3.cleaned_data['cykdajy']
            sebap = form3.cleaned_data['sebap']
            bellik = form3.cleaned_data['bellik']
            cykdajy_dollar=form3.cleaned_data['cykdajy_dollar']
            girdeji_dollar=form3.cleaned_data['girdeji_dollar']

            b = Bolek_hasaplar.objects.create(user=cur_user,girdeji=girdeji,girdeji_dollar=girdeji_dollar,cykdajy=cykdajy,cykdajy_dollar=cykdajy_dollar,sebap=sebap,bellik=bellik)
            b.save()
            return redirect('hasaphana',pk)
    else:
        form2 = OjSentForm()
        form3 = B_hasapForm()
    
    paginator = Paginator(b_has, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'cur_oj':cur_oj,'form2': form2, 'form3':form3,'oj':oj,'tot_b':tot_b,'gal_m':gal_m,'gal_d':gal_d}
    return render(request, 'shu/hasaphana.html', context)

@login_required(login_url='login')
def Ojidanie_update(request,pk):
    cur_user = request.user
    trans=Ojidanie.objects.get(id=pk)

    if trans.awans_m is not None or trans.awans_d is not None:
        obj = Ojidanie.objects.filter(id=pk).update(tassyk=1)
        b = Bolek_hasaplar.objects.create(user=cur_user,awans_m=trans.awans_m,awans_d=trans.awans_d,girdeji=trans.cash,girdeji_dollar=trans.cash_d,sebap=trans.sebap,bellik=trans.bellik)
        b.save()
        if trans.tassyk==0:
            d_b=Bolek_hasaplar.objects.get(oj_id=pk)
            d_b.delete()
            trans.delete()
    else:
        obj = Ojidanie.objects.filter(id=pk).update(tassyk=1)
        b = Bolek_hasaplar.objects.create(user=cur_user,awans_d=trans.awans_d,girdeji=trans.cash,girdeji_dollar=trans.cash_d,sebap=trans.sebap,bellik=trans.bellik)
        b.save()
        if trans.tassyk==0:
            d_b=Bolek_hasaplar.objects.get(oj_id=pk)
            d_b.delete()
            trans.delete()
    return redirect('hasaphana',pk)

@login_required(login_url='login')
def AylykPeydaPremya(request):
    page_title = _('Aýlyk, peýda ýa-da premýa')
    ay_pr = Aylyk_premya.objects.all()
    seneid1=Hasabat_sene.objects.last().id
    if request.method == 'POST':
        form = Aylyk_PremyaForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['user']
            summa_m = form.cleaned_data['summa_m']
            summa_dollar = form.cleaned_data['summa_dollar']
            sebap = form.cleaned_data['sebap']
            bellik = form.cleaned_data['bellik']

            aw_m=Bolek_hasaplar.objects.filter(user=user).aggregate(total=Sum(F('awans_m')))['total']
            aw_d=Bolek_hasaplar.objects.filter(user=user).aggregate(total=Sum(F('awans_d')))['total']

            awan_m=aw_m if aw_m is not None else 0
            awan_d=aw_d if aw_d is not None else 0

            ay_peyda=Aylyk_premya.objects.create(user=user,has_sene=seneid1,
                                                 summa_m=summa_m,summa_dollar=summa_dollar,
                                                 awans_m=awan_m,awans_d=awan_d,
                                                 jemi_m=summa_m - awan_m,
                                                 jemi_d=summa_dollar - awan_d,
                                                 sebap=sebap,bellik=bellik)
            ay_peyda.save()

            messages.success(request, 'Aýlyk, peýda ýa-da premýa girizildi!')
            return redirect('aylyk-premya')
        else:
            messages.error(request, 'Ýalňyşlyk: Aýlyk, peýda ýa-da premýa girizilmedi!')
    else:
        form = Aylyk_PremyaForm()
    
    paginator = Paginator(ay_pr, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form}
    return render(request, 'shu/aylyk_peyda_premya.html', context)

@login_required(login_url='login')
def Aylyk_premya_edit(request, pk):
    page_title = _('Aýlyk, peýda ýa-da premýa üýtgetmek')
    obj = Aylyk_premya.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Aylyk_Premya_editForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýlyk, peýda ýa-da premýa üýtgedildi!')
           return redirect('aylyk-premya')
    else:
        form = Aylyk_Premya_editForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


@login_required(login_url='login')
def Karz_pul(request):
    page_title = _('Daşyndan alynan karz pullar')
    krz_pul = Das_karz_alynanpul.objects.all()
    berilen = Karz_yzyna_berilen.objects.all()

    seneid1=Hasabat_sene.objects.last().id
    if request.method == 'POST':
        form = Karz_AlynanForm(request.POST, request.FILES)
        
        if form.is_valid():
            karzcy = form.cleaned_data['karzcy']
            a_summa_m = form.cleaned_data['a_summa_m']
            a_summa_d = form.cleaned_data['a_summa_d']
            sebap = form.cleaned_data['sebap']
            bellik = form.cleaned_data['bellik']

            al_karz=Das_karz_alynanpul.objects.create(karzcy=karzcy,has_sene=seneid1,
                                                 a_summa_m=a_summa_m,a_summa_d=a_summa_d,
                                                 sebap=sebap,bellik=bellik)
            al_karz.save()

            messages.success(request, 'Daşyndan alynan karz pul girizildi!')
            return redirect('karz-pul')
        else:
            messages.error(request, 'Ýalňyşlyk: Daşyndan alynan karz pul girizilmedi!')
    else:
        form = Karz_AlynanForm()
        
    
    paginator = Paginator(krz_pul, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form,'berilen':berilen}
    return render(request, 'shu/karz_pullar.html', context)

@login_required(login_url='login')
def Karaz_pul_update(request, pk):
    page_title = _('Alynan karzy bermek')

    seneid1=Hasabat_sene.objects.last().id

    if request.method == 'POST':
        form = Karz_BerilenForm(request.POST, request.FILES)
        if form.is_valid():
            obj = Das_karz_alynanpul.objects.get(id=pk)

            b_summa_m = form.cleaned_data['b_summa_m']
            b_summa_d = form.cleaned_data['b_summa_d']
            sebap = form.cleaned_data['sebap']
            bellik = form.cleaned_data['bellik']
            
            ber_create=Karz_yzyna_berilen.objects.create(alynan_karz_id=obj.pk,has_sene=seneid1,
                                                         karzcy=obj.karzcy,b_summa_m=b_summa_m,b_summa_d=b_summa_d,
                                                         sebap=sebap,bellik=bellik)
            ber_create.save()


            if obj.a_summa_m is not None:
                obj.jemi_m=obj.a_summa_m-b_summa_m
            elif obj.a_summa_d is not None:
                obj.jemi_d=obj.a_summa_d-b_summa_d
            else:
                obj.jemi_m=0
                obj.jemi_d=0
            obj.save()

            messages.success(request, 'Daşyndan alynan karz pul girizildi!')
            return redirect('karz-pul')
        else:
            messages.error(request, 'Ýalňyşlyk: Daşyndan alynan karz pul girizilmedi')
    else:
        form = Karz_BerilenForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Das_karz_edit(request, pk):
    page_title = _('Daşyndan alynan karz puly üýtgetmek')
    obj = Das_karz_alynanpul.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Karz_Alynan_editForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşyndan alynan karz pul üýtgedildi!')
           return redirect('karz-pul')
    else:
        form = Karz_Alynan_editForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Karz_yzyna_berilen_edit(request, pk):
    page_title = _('Daşyndan alynan karz puly üýtgetmek')
    obj = Karz_yzyna_berilen.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Karz_yzyna_berilenForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşyndan alynan karz pul üýtgedildi!')
           return redirect('karz-pul')
    else:
        form = Karz_yzyna_berilenForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


@login_required(login_url='login')
def ExportYuk(request):
    page_title = _('Exporta gitýän ýükleriň hasabaty')
    exp = Export_yukler.objects.all()
    if request.method == 'POST':
        form = ExportForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Exporta gitýän ýük girizildi!')
            return redirect('export')
        else:
            messages.error(request, 'Ýalňyşlyk: Exporta gitýän ýük girizilmedi!')
    else:
        form = ExportForm()
        
    
    paginator = Paginator(exp, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form}
    return render(request, 'shu/export.html', context)

@login_required(login_url='login')
def Export_yukler_edit(request, pk):
    page_title = _('Exporta gitýän ýüki üýtgetmek')
    obj = Export_yukler.objects.get(id=pk)
    
    if request.method == 'POST':
        form = ExportForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Exporta gitýän ýük üýtgedildi!')
           return redirect('export')
    else:
        form = ExportForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Import_pulYuk(request):
    page_title = _('Import: haryt getirýänler bilen hasaplaşyklaryň hasabaty')
    imp = Import_yukpul.objects.all()
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Import üçin pul girizildi!')
            return redirect('import')
        else:
            messages.error(request, 'Ýalňyşlyk: Import üçin pul girizilmedi!')
    else:
        form = ImportForm()
        
    
    paginator = Paginator(imp, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form}
    return render(request, 'shu/import.html', context)

@login_required(login_url='login')
def Import_update(request, pk):
    page_title = _('Import: haryt getirýän bilen hasaplaşyk')

    if request.method == 'POST':
        form = Import_updateForm(request.POST, request.FILES)
        if form.is_valid():
            g_summa_m = form.cleaned_data['g_summa_m']
            g_summa_d = form.cleaned_data['g_summa_d']

            obj = Import_yukpul.objects.get(id=pk)
            obj.g_summa_m=g_summa_m
            obj.g_summa_d=g_summa_d

            if obj.a_summa_m is not None:
                obj.tapawut_m=obj.a_summa_m-g_summa_m
            elif obj.a_summa_d is not None:
                obj.tapawut_d=obj.a_summa_d-g_summa_d
            else:
                obj.tapawut_m=0
                obj.tapawut_d=0
            obj.save()
            messages.success(request, 'Import üçin alynan pul geçirildi!')
            return redirect('import')
        else:
            messages.error(request, 'Ýalňyşlyk: Import üçin alynan pul geçirilmedi')
    else:
        form = Import_updateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Import_pulYuk_edit(request, pk):
    page_title = _('Import: haryt getirýänler bilen hasaplaşyklary üýtgetmek')
    obj = Import_yukpul.objects.get(id=pk)
    
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Import: haryt getirýänler bilen hasaplaşyk üýtgedildi!')
           return redirect('import')
    else:
        form = ImportForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


@login_required(login_url='login')
def Managers(request):
    page_title = _('Daşary ýurt klientler')
    mang = Manager_user.objects.all()
    if request.method == 'POST':
        form = ManagerForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Täze daşary ýurt klient girizildi!')
            return redirect('managers')
        else:
            messages.error(request, 'Ýalňyşlyk: Daşary ýurt klient girizilmedi!')
    else:
        form = ManagerForm()
        
    
    paginator = Paginator(mang, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form}
    return render(request, 'shu/managers.html', context)

@login_required(login_url='login')
def Manager_detail(request,pk):
    page_title = _('Daşary ýurt klient we peýdalary')
    mang_detail = Das_yurt_klientler.objects.filter(klient_id=pk)
    cykdajy = Das_yurt_klient_cykdajy.objects.filter(klient_id=pk)
    seneid1=Hasabat_sene.objects.last().id
    pkk=pk
    if request.method == 'POST':
        form = Manager_zakazForm(request.POST, request.FILES)
        
        if form.is_valid():
            harydyn_ady = form.cleaned_data['harydyn_ady']
            shertnama_nomer = form.cleaned_data['shertnama_nomer']
            z_sany = form.cleaned_data['z_sany']
            bahasy_m = form.cleaned_data['bahasy_m']
            bahasy_d = form.cleaned_data['bahasy_d']

            baha_m = bahasy_m if bahasy_m is not None else 0
            baha_d = bahasy_d if bahasy_d is not None else 0

            obj = Das_yurt_klientler.objects.create(klient_id=pk,harydyn_ady=harydyn_ady,has_sene=seneid1,
                                                           shertnama_nomer=shertnama_nomer,z_sany=z_sany,
                                                           bahasy_m=bahasy_m,bahasy_d=bahasy_d,
                                                           zj_bahasy_m=z_sany*baha_m,
                                                           zj_bahasy_d=z_sany*baha_d)
            obj.save()
            messages.success(request, 'Täze daşary ýurt klient we peýda girizildi!')
            return redirect('manager-detail',pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Daşary ýurt klient we peýda girizilmedi!')
    else:
        form = Manager_zakazForm()
        
    
    paginator = Paginator(mang_detail, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form':form,'cykdajy':cykdajy,'pkk':pkk}
    return render(request, 'shu/manager_detail.html', context)

@login_required(login_url='login')
def Mangr_detail_update(request, pk):
    page_title = _('Çykdaýjylary girizmek')
    seneid1=Hasabat_sene.objects.last().id
    
    if request.method == 'POST':
        form = Manager_zakazUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            i_sany = form.cleaned_data['i_sany']
            cykdajy_m = form.cleaned_data['cykdajy_m']
            cykdajy_d = form.cleaned_data['cykdajy_d']
            bellik = form.cleaned_data['bellik']

            obj = Das_yurt_klientler.objects.get(id=pk)
            j_baha_m=i_sany*obj.bahasy_m if obj.bahasy_m is not None else 0
            j_baha_d=i_sany*obj.bahasy_d if obj.bahasy_d is not None else 0
            cyk_create=Das_yurt_klient_cykdajy.objects.create(gir_klient_id=obj.pk,klient=obj.klient,has_sene=seneid1,
                                                              shertnama_nomer=obj.shertnama_nomer,harydyn_ady=obj.harydyn_ady,
                                                              i_sany=i_sany,cykdajy_m=cykdajy_m,cykdajy_d=cykdajy_d,
                                                              j_bahasy_m=j_baha_m,j_bahasy_d=j_baha_d,bellik=bellik)
            cyk_create.save()


            if cykdajy_m is not None:
                if obj.tapawut_m == 0:
                    obj.tapawut_m = obj.zj_bahasy_m - j_baha_m
                else:
                    obj.tapawut_m = obj.tapawut_m - j_baha_m
                obj.peyda_m=obj.tapawut_m-cykdajy_m
            elif cykdajy_d is not None:
                if obj.tapawut_d == 0:
                    obj.tapawut_d = obj.zj_bahasy_d - j_baha_d
                else:
                    obj.tapawut_d = obj.tapawut_d - j_baha_d
                obj.peyda_d=obj.tapawut_d-cykdajy_d
            else:
                obj.peyda_m=0
                obj.peyda_d=0
            obj.save()
            messages.success(request, 'Işlenilen haryt we çykdajy girizildi!')
            return redirect('manager-detail', obj.klient.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Işlenilen haryt we çykdajy girizilmedi')
    else:
        form = Manager_zakazUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Das_klient_edit(request, pk):
    page_title = _('Daşary ýurt klient we peýdasyny üýtgetmek')
    obj = Das_yurt_klientler.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Manager_zakaz_editForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşary ýurt klient we peýdalary üýtgedildi!')
           return redirect('manager-detail',pk)
    else:
        form = Manager_zakaz_editForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Das_yurt_klient_cykdajy_edit(request, pk):
    page_title = _('Daşary ýurt klientleriň çykdajylary üýtgetmek')
    obj = Das_yurt_klient_cykdajy.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Das_yurt_klient_cykdajyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşary ýurt klientleriň çykdajylary üýtgedildi!')
           return redirect('manager-detail',pk)
    else:
        form = Das_yurt_klient_cykdajyForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

# Bank hereketler
@login_required(login_url='login')
def Walyuta_bolum(request):
    page_title = _('Walýuta bölümi')
    wall = Walyuta_hasap.objects.all()
    if request.method == 'POST':
        form = Wal_bolumForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Täze walýuta hasap girizildi!')
            return redirect('walyuta-bolum')
        else:
            messages.error(request, 'Ýalňyşlyk: walýuta hasap girizilmedi!')
    else:
        form = Wal_bolumForm()
        
    
    paginator = Paginator(wall, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form}
    return render(request, 'shu/wal_bolum.html', context)

@login_required(login_url='login')
def Bank_Users(request,pk):
    page_title = _('Bank hereketini ulanyjylar')
    b_user = Bank_user.objects.filter(wal_id=pk)
    if request.method == 'POST':
        form = Bank_userForm(request.POST, request.FILES)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            tel = form.cleaned_data['tel']
            address = form.cleaned_data['address']
            obj = Bank_user.objects.create(wal_id=pk,name=name,tel=tel,address=address)
            obj.save()
            messages.success(request, 'Täze ulanyjy girizildi!')
            return redirect('bank-users',pk)
        else:
            messages.error(request, 'Ýalňyşlyk: ulanyjy girizilmedi!')
    else:
        form = Bank_userForm()
        
    
    paginator = Paginator(b_user, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form}
    return render(request, 'shu/bank_users.html', context)

@login_required(login_url='login')
def Bank_hereket(request,pk):
    page_title = _('Bankdaky hereketler')
    banks = Bank.objects.filter(user_id=pk)
    bankwal = Bank.objects.filter(user_id=pk).values_list('wal__name',flat=True).first()
    hasap=Bank.objects.filter(user_id=pk).aggregate(total=Sum(F('g_summa')) - Sum(F('c_summa')),gelen=Sum(F('g_summa')),giden=Sum(F('c_summa')))
    pkk=pk
    if request.method == 'POST':
        form = BankForm(request.POST, request.FILES)
        
        if form.is_valid():
            g_summa = form.cleaned_data['g_summa']
            c_summa = form.cleaned_data['c_summa']
            sebap = form.cleaned_data['sebap']
            bellik = form.cleaned_data['bellik']
            obj = Bank.objects.create(wal_id=pk,user_id=pk,g_summa=g_summa,c_summa=c_summa,
                                      galyndy=g_summa-c_summa,sebap=sebap,bellik=bellik)
            obj.save()
            messages.success(request, 'Täze bank hereketi girizildi!')
            return redirect('bank-hereket',pk)
        else:
            messages.error(request, 'Ýalňyşlyk: bank hereketi girizilmedi!')
    else:
        form = BankForm()
        
    paginator = Paginator(banks, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form,'hasap':hasap,'bankwal':bankwal,'pkk':pkk}
    return render(request, 'shu/bank.html', context)

@login_required(login_url='login')
def Bank_edit(request, pk):
    page_title = _('Bakdaky hereketi üýtgetmek')
    obj = Bank.objects.get(id=pk)
    
    if request.method == 'POST':
        form = BankForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Bakdaky hereket üýtgedildi!')
           return redirect('bank-hereket',pk)
    else:
        form = BankForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


# Algy bergiler
@login_required(login_url='login')
def Algy(request):
    page_title = _('Algylar')
    dok_al=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    hal_al=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    sap_al=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    ay_pr_m=Aylyk_premya.objects.filter(~Q(awans_m=None)).annotate(ady=F('user__last_name'),senesi=F('sene'),tap=Sum('jemi_m')).values('ady','tap','senesi')
    ay_pr_d=Aylyk_premya.objects.filter(~Q(awans_d=None)).annotate(ady=F('user__last_name'),senesi=F('sene'),tap_d=Sum('jemi_d')).values('ady','tap_d','senesi')
    
    zw_m=Das_isleyan_zawodlar.objects.annotate(ady=F('zawod__name'),senesi=F('sene'),tap_m=Sum('tapawut_m')).values('ady','tap_m','senesi')
    zw_d=Das_isleyan_zawodlar.objects.annotate(ady=F('zawod__name'),senesi=F('sene'),tap_d=Sum('tapawut_d')).values('ady','tap_d','senesi')
    
    a_karz_m=Das_karz_alynanpul.objects.annotate(ady=F('karzcy'),senesi=F('sene'),tap_m=Sum('jemi_m')).values('ady','tap_m','senesi')
    a_karz_d=Das_karz_alynanpul.objects.annotate(ady=F('karzcy'),senesi=F('sene'),tap_d=Sum('jemi_d')).values('ady','tap_d','senesi')
    
    gpz_m=Sklad_swotkalar.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_m=Sum('galyndy_bahasy_m')).values('ady','tap_m','senesi')
    gpz_d=Sklad_swotkalar.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_d=Sum('galyndy_bahasy_d')).values('ady','tap_d','senesi')
    
    imp_m=Import_yukpul.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_m=Sum('tapawut_m')).values('ady','tap_m','senesi')
    imp_d=Import_yukpul.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_d=Sum('tapawut_d')).values('ady','tap_d','senesi')
    
    bank=Bank.objects.annotate(ady=F('user__name'),senesi=F('sene'),tap=Sum('galyndy')).values('ady','tap','senesi')
    
    inwen_m=Inwentar.objects.annotate(ady=F('harydyn_ady'),senesi=F('sene'),tap_m=Sum('j_bahasy_m')).values('ady','tap_m','senesi')
    inwen_d=Inwentar.objects.annotate(ady=F('harydyn_ady'),senesi=F('sene'),tap_d=Sum('j_bahasy_d')).values('ady','tap_d','senesi')
    
    z_dok_al=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(algy=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('algy')).values('zady','tap','senesi')
    z_hal_al=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(algy=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('algy')).values('zady','tap','senesi')
    z_sap_al=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(algy=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('algy')).values('zady','tap','senesi')
    
    res=list(chain(dok_al,hal_al,sap_al,ay_pr_m,ay_pr_d,z_dok_al,z_hal_al,z_sap_al,zw_m,zw_d,gpz_m,gpz_d,bank,imp_m,imp_d,inwen_m,inwen_d,a_karz_m,a_karz_d))

    paginator = Paginator(res, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser}
    return render(request, 'shu/algylar.html', context)

@login_required(login_url='login')
def Bergi(request):
    page_title = _('Bergiler')
    dok_al=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    hal_al=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    sap_al=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).annotate(ady=F('sehs__name'),senesi=F('sene'),tap=Sum('tapawudy')).values('ady','tap','senesi')
    ay_pr_m=Aylyk_premya.objects.filter(~Q(awans_m=None)).annotate(ady=F('user__last_name'),senesi=F('sene'),tap=Sum('jemi_m')).values('ady','tap','senesi')
    ay_pr_d=Aylyk_premya.objects.filter(~Q(awans_d=None)).annotate(ady=F('user__last_name'),senesi=F('sene'),tap_d=Sum('jemi_d')).values('ady','tap_d','senesi')

    zw_m=Das_isleyan_zawodlar.objects.annotate(ady=F('zawod__name'),senesi=F('sene'),tap_d=Sum('tapawut_m')).values('ady','tap_d','senesi')
    zw_d=Das_isleyan_zawodlar.objects.annotate(ady=F('zawod__name'),senesi=F('sene'),tap_d=Sum('tapawut_d')).values('ady','tap_d','senesi')
    
    b_karz_m=Das_karz_alynanpul.objects.annotate(ady=F('karzcy'),senesi=F('sene'),tap_m=Sum('jemi_m')).values('ady','tap_m','senesi')
    b_karz_d=Das_karz_alynanpul.objects.annotate(ady=F('karzcy'),senesi=F('sene'),tap_d=Sum('jemi_d')).values('ady','tap_d','senesi')
    
    gpz_m=Sklad_swotkalar.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_d=Sum('galyndy_bahasy_m')).values('ady','tap_d','senesi')
    gpz_d=Sklad_swotkalar.objects.annotate(ady=F('kimden__name'),senesi=F('sene'),tap_d=Sum('galyndy_bahasy_d')).values('ady','tap_d','senesi')

    bank=Bank.objects.annotate(ady=F('user__name'),senesi=F('sene'),tap_d=Sum('galyndy')).values('ady','tap_d','senesi')

    inwen_m=Inwentar.objects.annotate(ady=F('harydyn_ady'),senesi=F('sene'),tap_m=Sum('j_bahasy_m')).values('ady','tap_m','senesi')
    inwen_d=Inwentar.objects.annotate(ady=F('harydyn_ady'),senesi=F('sene'),tap_d=Sum('j_bahasy_d')).values('ady','tap_d','senesi')

    z_dok_ber=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(bergi=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('bergi')).values('zady','tap','senesi')
    z_hal_ber=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(bergi=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('bergi')).values('zady','tap','senesi')
    z_sap_ber=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(bergi=None).annotate(zady=F('user__faa'),senesi=F('zakaz_sene'),tap=Sum('bergi')).values('zady','tap','senesi')
    
    res=list(chain(dok_al,hal_al,sap_al,ay_pr_m,ay_pr_d,z_dok_ber,z_hal_ber,z_sap_ber,zw_m,zw_d,gpz_m,gpz_d,bank,inwen_m,inwen_d,b_karz_m,b_karz_d))

    paginator = Paginator(res, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser}
    return render(request, 'shu/bergiler.html', context)

@login_required(login_url='login')
def Balans_view(request):
    page_title = _('Balans')
    # Jemi algylar
    dok_jem_m=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cykrulon_bahasy_m")))['jemi']
    hal_jem_m=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("abathalta_bahasy_m")))['jemi']
    sap_jem_m=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cyksapak_bahasy_m")))['jemi']
    
    dok_jem_d=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cykrulon_bahasy_d")))['jemi']
    hal_jem_d=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("abathalta_bahasy_d")))['jemi']
    sap_jem_d=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cyksapak_bahasy_d")))['jemi']
    
    ay_pr_m_jem=Aylyk_premya.objects.filter(~Q(awans_m=None)).aggregate(jemi=Sum(F('jemi_m')))['jemi']
    ay_pr_d_jem=Aylyk_premya.objects.filter(~Q(awans_d=None)).aggregate(jemi=Sum(F('jemi_d')))['jemi']
    
    z_dok_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(algy=None).aggregate(jemi=Sum(F('algy')))['jemi']
    z_hal_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(algy=None).aggregate(jemi=Sum((F'algy')))['jemi']
    z_sap_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(algy=None).aggregate(jemi=Sum(F('algy')))['jemi']

    zw_m=Das_isleyan_zawodlar.objects.aggregate(tap_m=Sum('tapawut_m'))['tap_m']
    zw_d=Das_isleyan_zawodlar.objects.aggregate(tap_d=Sum('tapawut_d'))['tap_d']
    
    a_karz_m=Das_karz_alynanpul.objects.aggregate(tap_m=Sum('jemi_m'))['tap_m']
    a_karz_d=Das_karz_alynanpul.objects.aggregate(tap_d=Sum('jemi_d'))['tap_d']
    
    gpz_m=Sklad_swotkalar.objects.aggregate(tap_m=Sum('galyndy_bahasy_m'))['tap_m']
    gpz_d=Sklad_swotkalar.objects.aggregate(tap_d=Sum('galyndy_bahasy_d'))['tap_d']
    
    bank_m=Bank.objects.filter(wal=1).aggregate(tap=Sum('galyndy'))['tap']
    bank_d=Bank.objects.filter(wal=2).aggregate(tap=Sum('galyndy'))['tap']
    
    a_algy_m=dok_jem_m if dok_jem_m is not None else 0
    b_algy_m=hal_jem_m if hal_jem_m is not None else 0
    c_algy_m=sap_jem_m if sap_jem_m is not None else 0
    d_algy_m=ay_pr_m_jem if ay_pr_m_jem is not None else 0
    g_algy=z_dok_al_jem if z_dok_al_jem is not None else 0
    t_algy=z_hal_al_jem if z_hal_al_jem is not None else 0
    j_algy=z_sap_al_jem if z_sap_al_jem is not None else 0
    p_algy_m=zw_m if zw_m is not None else 0
    s_algy_m=a_karz_m if a_karz_m is not None else 0
    k_algy_m=gpz_m if gpz_m is not None else 0
    w_algy_m=bank_m if bank_m is not None else 0

    a_algy_d=dok_jem_d if dok_jem_d is not None else 0
    b_algy_d=hal_jem_d if hal_jem_d is not None else 0
    c_algy_d=sap_jem_d if sap_jem_d is not None else 0
    d_algy_d=ay_pr_d_jem if ay_pr_d_jem is not None else 0
    p_algy_d=zw_d if zw_d is not None else 0
    s_algy_d=a_karz_d if a_karz_d is not None else 0
    k_algy_d=gpz_d if gpz_d is not None else 0
    w_algy_d=bank_d if bank_d is not None else 0


    ajem_m=sum(list(chain([a_algy_m,b_algy_m,c_algy_m,d_algy_m,g_algy,t_algy,j_algy,p_algy_m,s_algy_m,k_algy_m,w_algy_m])))
    ajem_d=sum(list(chain([a_algy_d,b_algy_d,c_algy_d,d_algy_d,p_algy_d,s_algy_d,k_algy_d,w_algy_d])))


    # Jemi bergiler
    beray_pr_m_jem=Aylyk_premya.objects.filter(~Q(awans_m=None)).aggregate(jemi=Sum(F('awans_m')))['jemi']
    beray_pr_d_jem=Aylyk_premya.objects.filter(~Q(awans_d=None)).aggregate(jemi=Sum(F('awans_d')))['jemi']
    z_dok_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']
    z_hal_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']
    z_sap_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']

    a_bergi_m=beray_pr_m_jem if beray_pr_m_jem is not None else 0
    c_bergi=z_dok_ber_jem if z_dok_ber_jem is not None else 0
    d_bergi=z_hal_ber_jem if z_hal_ber_jem is not None else 0
    e_bergi=z_sap_ber_jem if z_sap_ber_jem is not None else 0
    
    a_bergi_d=beray_pr_d_jem if beray_pr_d_jem is not None else 0

    ajem_mtest=list(chain([a_algy_m,b_algy_m,c_algy_m,d_algy_m,g_algy,t_algy,j_algy,p_algy_m,s_algy_m,k_algy_m,w_algy_m]))
    ajem_dtest=list(chain([a_algy_d,b_algy_d,c_algy_d,d_algy_d,p_algy_d,s_algy_d,k_algy_d,w_algy_d]))

    fr_m=[]
    for x in ajem_mtest:
        if x < 0:
            fr_m.append(x)
    
    fr_d=[]
    for x in ajem_dtest:
        if x < 0:
            fr_m.append(x)

    bjem_m=sum(list(chain(fr_m,[a_bergi_m,c_bergi,d_bergi,e_bergi])))
    bjem_d=sum(list(chain(fr_d,[a_bergi_d])))


    # Jemi inwentar
    inwen_m=Inwentar.objects.aggregate(jemi=Sum(F('bahasy_m')))['jemi']
    inwen_d=Inwentar.objects.aggregate(jemi=Sum(F('bahasy_d')))['jemi']
    # print(inwen_m)

    # Jemi GPZ
    cig_m=World_cygmal.objects.aggregate(jemi=Sum(F('j_bahasy_m')))['jemi']
    cig_d=World_cygmal.objects.aggregate(jemi=Sum(F('j_bahasy_d')))['jemi']


    # Jemi bolek hasaplar
    bgal_d=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji_dollar')) - Sum(F('cykdajy_dollar')))['total']
    bgal_m=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji')) - Sum(F('cykdajy')))['total']
    
    inw_m=inwen_m if inwen_m is not None else 0
    inw_d=inwen_d if inwen_d is not None else 0
    c_m=cig_m if cig_m is not None else 0
    c_d=cig_d if cig_d is not None else 0
    g_m=bgal_m if bgal_m is not None else 0
    g_d=bgal_d if bgal_d is not None else 0

    # Jemi sehler
    sapak_m=Sapakseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cyksapak_bahasy_m')))['jemi']
    sapak_d=Sapakseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cyksapak_bahasy_d')))['jemi']

    dokma_m=Dokmaseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cykrulon_bahasy_m')))['jemi']
    dokma_d=Dokmaseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cykrulon_bahasy_d')))['jemi']

    halta_abat_m=Haltaseh_sklad.objects.filter(~Q(abathalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('abathalta_bahasy_m')))['jemi']
    halta_abat_d=Haltaseh_sklad.objects.filter(~Q(abathalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('abathalta_bahasy_d')))['jemi']

    halta_brak_m=Haltaseh_sklad.objects.filter(~Q(brakhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('brakhalta_bahasy_m')))['jemi']
    halta_brak_d=Haltaseh_sklad.objects.filter(~Q(brakhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('brakhalta_bahasy_d')))['jemi']
    
    halta_ganar_m=Haltaseh_sklad.objects.filter(~Q(ganarhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('ganarhalta_bahasy_m')))['jemi']
    halta_ganar_d=Haltaseh_sklad.objects.filter(~Q(ganarhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('ganarhalta_bahasy_d')))['jemi']


    s_m=sapak_m if sapak_m is not None else 0
    d_m=dokma_m if dokma_m is not None else 0
    h_m=halta_abat_m if halta_abat_m is not None else 0
    hbrak_m=halta_brak_m if halta_brak_m is not None else 0
    hganar_m=halta_ganar_m if halta_ganar_m is not None else 0

    s_d=sapak_d if sapak_d is not None else 0
    d_d=dokma_d if dokma_d is not None else 0
    h_d=halta_abat_d if halta_abat_d is not None else 0
    hbrak_d=halta_brak_d if halta_brak_d is not None else 0
    hganar_d=halta_ganar_d if halta_ganar_d is not None else 0

    seh_jem_m = sum(list(chain([s_m,d_m,h_m,hbrak_m,hganar_m])))
    seh_jem_d = sum(list(chain([s_d,d_d,h_d,hbrak_d,hganar_d])))

    # Umumy jemleri Balansdaky
    jemleri_m=sum(list(chain([ajem_m,bjem_m, inw_m,c_m,g_m,seh_jem_m])))
    jemleri_d=sum(list(chain([ajem_d,bjem_d, inw_d,c_d,g_d,seh_jem_d])))

    # print(inwen_m)
    # paginator = Paginator(ajem_m, 10) 
    # page = request.GET.get('page')
    # try:
    #     myuser = paginator.get_page(page)
    # except PageNotAnInteger:
    #     myuser = paginator.page(1)
    # except EmptyPage:
    #     myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'ajem_m':ajem_m,'ajem_d':ajem_d,
               'bjem_m':bjem_m,'bjem_d':bjem_d, 'inw_m':inw_m,'inw_d':inw_d,
               'c_m':c_m,'c_d':c_d, 'g_m':g_m,'g_d':g_d, 'seh_jem_m':seh_jem_m,'seh_jem_d':seh_jem_d,
               'jemleri_m':jemleri_m,'jemleri_d':jemleri_d}
    return render(request, 'shu/balans.html', context)


# Kadr
@login_required(login_url='login')
def KadrPanel(request):
    page_title = _('Işgärler bölümi')
    cur_user = request.user
    my_users = AllUsers.objects.filter(office=cur_user.office).filter(is_superuser=False)
    gro = Group.objects.all()
    of = Office.objects.all()

    paginator = Paginator(my_users, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser': myuser,'of':of}
    return render(request, 'shu/kadr_panel.html', context)

@login_required(login_url='login')
def Kadr_office(request, pk):
    page_title = _('Işgärleriň sanawy')
    cur_user = AllUsers.objects.filter(office=pk)

    if request.method == 'POST':
        form = KadrUserForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            bolum = form.cleaned_data['bolum']
            wez = form.cleaned_data['wez']
            # group = form.cleaned_data['group']
            tel = form.cleaned_data['tel']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            birth_date = form.cleaned_data['birth_date']
            image = form.cleaned_data['image']
            password = form.cleaned_data['password']
            newuser = AllUsers.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, middle_name=middle_name,office=cur_user.office,bolum=bolum,wez=wez, tel=tel, address=address, birth_date=birth_date, image=image)
            # group = Group.objects.get(name='Ulanyjylar')
            newuser.is_staff = True
            # newuser.groups.add(group)
            newuser.save()
            newuser.refresh_from_db()
            return redirect('office-kadr')
    else:
        form = KadrUserForm()
    
    paginator = Paginator(cur_user, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form':form}
    return render(request, 'shu/kadr_office.html', context)

@login_required(login_url='login')
def Kadr_detail(request, pk):
    page_title = _('Işgärleriň giňişleýin maglumatlary')
    cur_user = AllUsers.objects.get(id=pk)
    total = cur_user.b_hasap.all().aggregate(Sum('girdeji')).get('girdeji__sum')
    total_cyk = cur_user.b_hasap.all().aggregate(Sum('cykdajy')).get('cykdajy__sum')
    gir = cur_user.b_hasap.all()
    pkk=cur_user.office.pk
    form = UserUpdateForm(instance=cur_user)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=cur_user)
        if form.is_valid():
           form.save()
           return redirect('kadr-detail', pk)
    else:
        form = UserUpdateForm(instance=cur_user)

    context = {'title': page_title,'cur_user':cur_user,'total':total,'total_cyk':total_cyk,'gir':gir,'form': form,'pkk':pkk}
    return render(request, 'shu/kadr_detail.html', context)

@login_required(login_url='login')
def delete_myuser(request, pk):
    if request.method == 'POST':
        person = AllUsers.objects.get(pk=pk)
        person.delete()
    else:
        return redirect('office-kadr')


# Inwentar
@login_required(login_url='login')
def Inwentar_sanaw(request):
    page_title = _('Inwentarlaryň sanawy')
    inwen = Inwentar.objects.all()
    spi=Inwen_spisat.objects.all()

    if request.method == 'POST':
        form = InwentarForm(request.POST, request.FILES)
        if form.is_valid():
            harydyn_ady = form.cleaned_data['harydyn_ady']
            bahasy_m = form.cleaned_data['bahasy_m']
            bahasy_d = form.cleaned_data['bahasy_d']
            sany = form.cleaned_data['sany']
            nirde_dur = form.cleaned_data['nirde_dur']
            bellik = form.cleaned_data['bellik']
            if bahasy_m is not None:
                obj = Inwentar.objects.create(harydyn_ady=harydyn_ady,bahasy_m=bahasy_m,bahasy_d=bahasy_d,
                                              sany=sany,nirde_dur=nirde_dur,bellik=bellik,
                                              j_bahasy_m=sany*bahasy_m)
                obj.save()
            elif bahasy_d is not None:
                obj = Inwentar.objects.create(harydyn_ady=harydyn_ady,bahasy_m=bahasy_m,bahasy_d=bahasy_d,
                                              sany=sany,nirde_dur=nirde_dur,bellik=bellik,
                                              j_bahasy_d=sany*bahasy_d)
                obj.save()
            messages.success(request, 'Täze inwentar girizildi!')
            return redirect('inwentar')
        else:
            messages.error(request, 'Ýalňyşlyk: inwentar girizilmedi!')
    else:
        form = InwentarForm()
    
    paginator = Paginator(inwen, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form':form,'spi':spi}
    return render(request, 'shu/inwentar.html', context)

@login_required(login_url='login')
def Inwentar_update(request, pk):
    page_title = _('Spisat edilen inwentarlary girizmek')

    if request.method == 'POST':
        form = Inwentar_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            inw=Inwentar.objects.get(id=pk)
            sany = form.cleaned_data['sany']
            bellik = form.cleaned_data['bellik']
            obj = Inwen_spisat.objects.create(inwent_id=pk,harydyn_ady=inw.harydyn_ady,
                                                     bahasy_m=inw.bahasy_m,bahasy_d=inw.bahasy_d,
                                                     sany=sany,nirde_dur=inw.nirde_dur,bellik=bellik,
                                                     j_bahasy_m=sany*inw.bahasy_m if inw.bahasy_m is not None else 0,
                                                     j_bahasy_d=sany*inw.bahasy_d if inw.bahasy_d is not None else 0)
            obj.save()
            inw.sany = inw.sany - sany
            inw.save()
            messages.success(request, 'Spisat edilen inwentar girizildi!')
            return redirect('inwentar')
        else:
            messages.error(request, 'Ýalňyşlyk: spisat edilen inwentar girizilmedi')
    else:
        form = Inwentar_UpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Inwentar_edit(request, pk):
    page_title = _('Inwentary üýtgetmek')
    obj = Inwentar.objects.get(id=pk)
    
    if request.method == 'POST':
        form = InwentarForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Inwentar üýtgedildi!')
           return redirect('inwentar')
    else:
        form = InwentarForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


# Sapak SEH
@login_required(login_url='login')
def Gun_ondSapak_sanaw(request,pk):
    page_title = _('Sapak sehde gündelik öndürilýän sapaklaryň sanawy')
    cur_user=request.user

    myseh = Gundelik_sapak.objects.filter(sehs_id=pk).order_by("sene")
    ay_has = Aydaky_sapak.objects.filter(sehs_id=pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_cyk_kg')).values('month','gornus','onum','id','jemi_bahasy_m','jemi_bahasy_d').order_by("sene")
    prpk=Sehler.objects.get(id=pk)

    seneid=Hasabat_sene.objects.all().last()
    
    if request.method == 'POST':
        form = GunSapakForm(request.POST, request.FILES)
        form3 = TikinciAddForm(request.POST, request.FILES)
        if form.is_valid():
            # Sene insert etmek
            if seneid == None or seneid.sene.month is not datetime.now().month:
                sene_create=Hasabat_sene.objects.create(sene=timezone.now())
                sene_create.save()
                sene_create.refresh_from_db()
            else:
                pass
            
            user = form.cleaned_data['user']
            d_gornusi = form.cleaned_data['d_gornusi']
            cyksapak_kg = form.cleaned_data['cyksapak_kg']
            cyksapak_bahasy_m = form.cleaned_data['cyksapak_bahasy_m']
            cyksapak_bahasy_d = form.cleaned_data['cyksapak_bahasy_d']
            wozwrat_kg = form.cleaned_data['wozwrat_kg']
            katyska_agram = form.cleaned_data['katyska_agram']
            nirden_gelen = form.cleaned_data['nirden_gelen']
            enjam = form.cleaned_data['enjam']
            bellik = form.cleaned_data['bellik']

            seneid1=Hasabat_sene.objects.last().id

            sap = cyksapak_kg if cyksapak_kg is not None else 0
            sap_m = cyksapak_bahasy_m if cyksapak_bahasy_m is not None else 0
            sap_d = cyksapak_bahasy_d if cyksapak_bahasy_d is not None else 0
            
            # Gundelik haryt insert we Gundelik hasabat (Aydaky_halta) modele insert
            if cyksapak_bahasy_m is not None:
                ay_jem_baha_m = sap * sap_m
                ayhas = Aydaky_sapak.objects.create(offices=cur_user.office,sehs_id=pk,d_gornusi=d_gornusi,jemi_cyk_kg=cyksapak_kg,jemi_bahasy_m=ay_jem_baha_m)
                ayhas.save()
            elif cyksapak_bahasy_d is not None:
                ay_jem_baha_d = sap * sap_d
                ayhas = Aydaky_sapak.objects.create(offices=cur_user.office,sehs_id=pk,d_gornusi=d_gornusi,jemi_cyk_kg=cyksapak_kg,jemi_bahasy_d=ay_jem_baha_d)
                ayhas.save()

            
            guncreate = Gundelik_sapak.objects.create(user=user,has_sene=seneid1,offices=cur_user.office,sehs_id=pk,
                                                           d_gornusi=d_gornusi,cyksapak_kg=cyksapak_kg,cyksapak_bahasy_m=cyksapak_bahasy_m,
                                                           cyksapak_bahasy_d=cyksapak_bahasy_d,wozwrat_kg=wozwrat_kg,
                                                           katyska_agram=katyska_agram,nirden_gelen=nirden_gelen,enjam=enjam,bellik=bellik)
            guncreate.save()
                
            seneid2=list(Hasabat_sene.objects.all())[-2].id
            abj1=Gundelik_sapak.objects.filter(has_sene=seneid1)
            ay2=AydakySapak_hasabat.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            ay3=AydakySapak_hasabat.objects.all()
            
            sap_j=Gundelik_sapak.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('cyksapak_kg')))['total']
            wz_j=Gundelik_sapak.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('wozwrat_kg')))['total']
            ahg_j=AydakySapak_hasabat.objects.filter(has_sene=seneid2,d_gornusi=d_gornusi).aggregate(total=Sum(F('ahyrky_galyndy')))['total']
            zak_j=Gundelik_sapak.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('cyksapak_kg')))['total']

            a_j=sap_j if sap_j is not None else 0
            b_j=wz_j if wz_j is not None else 0
            c_j=zak_j if zak_j is not None else 0
            d_j=ahg_j if ahg_j is not None else 0

            # Aydaky hasabat insert we update
            if ay2 == 0:
                cur_ay_create = AydakySapak_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,
                                                                                                                                            sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,
                                                                                                                                            gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,
                                                                                                                                            ahyrky_galyndy=d_j + a_j)
                cur_ay_create.save()
            for x in ay3:
                if x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    ay_update = AydakySapak_hasabat.objects.filter(Q(has_sene=seneid1), Q(d_gornusi=d_gornusi)).update(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,
                                                                                                                 sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,
                                                                                                                 gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                elif ay2 > 0 and x.jemi_dok_sapak == None:
                    cur_ay_create = AydakySapak_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,
                                                                                                                                                sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,
                                                                                                                                                gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,
                                                                                                                                                ahyrky_galyndy=d_j + a_j)
                    cur_ay_create.save()
                continue

            #swotka sehin peydasyny cykarmaly
            swotka_count=Zakaz_SapakSwotka.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            swotka=Zakaz_SapakSwotka.objects.all()

            sklad_onum_count=Sapakseh_sklad.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            sklad_onum=Sapakseh_sklad.objects.all()

            if swotka_count == 0:
                swotka_create=Zakaz_SapakSwotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * sap_m,jemi_baha_d=a_j * sap_d)
                swotka_create.save()
            for x in swotka:
                if x.jemi_kg is not None and x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    swotka_update = Zakaz_SapakSwotka.objects.filter(~Q(jemi_kg=None),Q(has_sene=seneid1), Q(d_gornusi=d_gornusi)).update(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * sap_m,jemi_baha_d=a_j * sap_d)
                elif swotka_count > 0 and x.jemi_kg == None:
                    create_zak_swot=Zakaz_SapakSwotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * sap_m,jemi_baha_d=a_j * sap_d)
                    create_zak_swot.save()
                continue

            if sklad_onum_count == 0:
                sk_onum_create=Sapakseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cyksapak_bahasy_m=sap_m,cyksapak_bahasy_d=sap_d,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                sk_onum_create.save()
            for x in sklad_onum:
                if x.jemi_dok_sapak is not None and x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    sk_onum_update = Sapakseh_sklad.objects.filter(~Q(jemi_dok_sapak=None),Q(has_sene=seneid1), Q(d_gornusi=d_gornusi)).update(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cyksapak_bahasy_m=sap_m,cyksapak_bahasy_d=sap_d,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                elif sklad_onum_count > 0 and x.jemi_dok_sapak == None:
                    create_sk_onum=Sapakseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cyksapak_bahasy_m=sap_m,cyksapak_bahasy_d=sap_d,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                    create_sk_onum.save()
                continue
            
            messages.success(request, 'Täze öndürilen sapak girizildi!')
            return redirect('sapak-seh',pk)
        
        if form3.is_valid():
            faa=form3.cleaned_data['faa']
            birth_date=form3.cleaned_data['birth_date']
            address=form3.cleaned_data['address']

            tikiciadd = Other_users.objects.create(seh_id=pk,wez_id=1,faa=faa,birth_date=birth_date,address=address)
            tikiciadd.save()
            messages.success(request, f'{faa} täze zakazçy girizildi!')
            return redirect('sapak-seh',pk)
    else:
        form = GunSapakForm()
        form3 = TikinciAddForm()
    
    # test2=Aydaky_sapak.objects.select_related('d_gornusi').annotate(
    #     month=TruncMonth('sene'),gornus=F('d_gornusi__name'),cur_off=F('offices')).values('month', 'gornus','cur_off').annotate(
    #         jemi_kg=Sum(F("jemi_cyk_kg"))).annotate(jemi_bahasy_m=Sum(F("jemi_bahasy_m"))).annotate(jemi_bahasy_d=Sum(F("jemi_bahasy_d")))
    pkk=prpk.pr_seh.pk
    # Paginator
    paginator = Paginator(myseh, 10)
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    paginator1 = Paginator(ay_has, 10)
    page1 = request.GET.get('page')
    try:
        ay_h = paginator1.get_page(page1)
    except PageNotAnInteger:
        ay_h = paginator1.page(1)
    except EmptyPage:
        ay_h = paginator1.page(paginator1.num_pages)

    context = {'title': page_title,'myuser':myuser, 'ay_h':ay_h,'form':form,'form3':form3,'pkk':pkk}
    return render(request, 'shu/sapakseh.html', context)

@login_required(login_url='login')
def Sapakseh_zakaz(request, pk):
    page_title = _('Täze zakaz girizmek')
    seneid=Hasabat_sene.objects.all().last()
    cur_user=request.user
    
    if request.method == 'POST':
        form2 = ZakazSapakForm(request.POST, request.FILES)
        if form2.is_valid():
            if seneid == None or seneid.sene.month is not datetime.now().month:
                sene_create=Hasabat_sene.objects.create(sene=timezone.now())
                sene_create.save()
                sene_create.refresh_from_db()
            else:
                pass
            zcode=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
            
            cur_code = []
            for deg in zcode:
                c=deg.haryt_code
                cur_code.append({'c':c})

            user = form2.cleaned_data['user']
            zakaz_user = form2.cleaned_data['zakaz_user']
            d_gornusi = form2.cleaned_data['h_gornusi']
            cyksapak_kg = form2.cleaned_data['cyksapak_kg']
            cyksapak_bahasy_m = form2.cleaned_data['cyksapak_bahasy_m']
            cyksapak_bahasy_d = form2.cleaned_data['cyksapak_bahasy_d']
            wozwrat_kg = form2.cleaned_data['wozwrat_kg']
            katyska_agram = form2.cleaned_data['katyska_agram']
            nirden_gelen = form2.cleaned_data['nirden_gelen']
            enjam = form2.cleaned_data['enjam']
            bellik = form2.cleaned_data['bellik']

            seneid1=Hasabat_sene.objects.last().id
            limit=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
            
            # Gundelik haryt insert we Gundelik hasabat (Aydaky_sapak) modele insert
            for deg in limit:
                rb1=deg.algy-cyksapak_kg*deg.bahasy
                if deg.algy != 0:
                    s=deg.algy/deg.bahasy
                    if s >= cyksapak_kg:
                        zakgun = Gundelik_sapak.objects.create(has_sene=seneid1,user=user,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,sehs_id=pk,
                                                               d_gornusi=d_gornusi,cyksapak_kg=cyksapak_kg,cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,wozwrat_kg=wozwrat_kg,
                                                               katyska_agram=katyska_agram,nirden_gelen=nirden_gelen,enjam=enjam,bellik=bellik)
                        zakgun.save()

                        up=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code'])).update(algy = rb1)
                        
                        if cyksapak_bahasy_m is not None:
                            ay_jem_baha_m = cyksapak_kg * cyksapak_bahasy_m
                            ayhas = Aydaky_sapak.objects.create(sehs_id=pk,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,d_gornusi=d_gornusi,jemi_cyk_kg=cyksapak_kg,jemi_bahasy_m=ay_jem_baha_m)
                            ayhas.save()
                        elif cyksapak_bahasy_d is not None:
                            ay_jem_baha_d = cyksapak_kg * cyksapak_bahasy_d
                            ayhas = Aydaky_sapak.objects.create(sehs_id=pk,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,d_gornusi=d_gornusi,jemi_cyk_kg=cyksapak_kg,jemi_bahasy_d=ay_jem_baha_d)
                            ayhas.save()

            seneid2=list(Hasabat_sene.objects.all())[-2].id
            ay2=AydakySapak_hasabat.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            ay3=AydakySapak_hasabat.objects.all()
            
            sap_j=Gundelik_sapak.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('cyksapak_kg',flat=True)
            wz_j=Gundelik_sapak.objects.exclude(wozwrat_kg=None).filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('wozwrat_kg',flat=True)
            ahg_j=AydakySapak_hasabat.objects.filter(has_sene=seneid2,d_gornusi=d_gornusi).values_list('ahyrky_galyndy',flat=True)
            zak_j=Gundelik_halta.objects.exclude(zakaz_user=None).filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('cyksapak_kg',flat=True)

            # Aydaky hasabat insert we update
            if ay2 == 0:
                cur_ay_create = AydakySapak_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
                cur_ay_create.save()
            for x in ay3:
                if ay2 > 0 and x.has_sene is not seneid1 and x.d_gornusi is not d_gornusi:
                    cur_ay_create = AydakySapak_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
                    cur_ay_create.save()
                else:
                    ay_update = AydakySapak_hasabat.objects.filter(has_sene=seneid1, d_gornusi=d_gornusi).update(cyksapak_bahasy_m=cyksapak_bahasy_m,cyksapak_bahasy_d=cyksapak_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_sapak=a_j,gecenay_galyndy=d_j,satylan_sapak_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
    
            sene_zak=Hasabat_sene.objects.last()
            seneid3=Hasabat_sene.objects.earliest('sene')
            zak_bal=Zakaz_balans.objects.all()
            zak_swS=Zakaz_SapakSwotka.objects.all().count()
            zak_sw=Zakaz_SapakSwotka.objects.all()

            senejik=list(Hasabat_sene.objects.all())[-2]
            tot_kg=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(j_kg=Sum(F("cyk_sapak_kg"))).values_list('j_kg',flat=True)
            tot_bah=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(j_baha=Sum(F("balans"))).values_list('j_baha',flat=True)
            baha_tot=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(baha_j=Sum(F("bahasy"))).values_list('baha_j',flat=True)

            a_j=sap_j if sap_j is not None else 0
            b_j=wz_j if wz_j is not None else 0
            c_j=zak_j if zak_j is not None else 0
            d_j=ahg_j if ahg_j is not None else 0

            # Zakazçy tarapyndan gelyan peýda we çykdaýjy hasabat (Zakaz_swotka) insert we update
            if zak_swS == 0:
                create_zak_swot=Zakaz_SapakSwotka.objects.filter(Q(sene_id=None) | ~Q(sene_id=seneid1)).create(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
                create_zak_swot.save()
            for i in zak_sw:
                if zak_swS > 0 and i.sene_id==None and i.sene_id is not seneid1:
                    create_zak_swot=Zakaz_SapakSwotka.objects.filter(Q(sene_id=None) | ~Q(sene_id=seneid1)).create(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
                    create_zak_swot.save()
                else:
                    up_zak_swot=Zakaz_SapakSwotka.objects.filter(sene_id=seneid1).update(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
            messages.success(request, 'Täze ZAKAZ üçin dokalan sapak girizildi!')
            return redirect('sapak-seh',pk)
    else:
        form2 = ZakazSapakForm()

    context = {'title': page_title,'form2': form2}
    return render(request, 'shu/sapakseh_zakaz.html', context)

@login_required(login_url='login')
def Sapakseh_hasabat(request,pk):
    page_title = _('Aýdaky hasabatlar')
    sh=Sehler.objects.filter(pr_seh_id=pk).first()
    
    ayjem = AydakySapak_hasabat.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_sapak')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_sapak_kg','wozwrat','ahyrky_galyndy','yerinde_bar_haryt','tapawudy','bellik').order_by("sene")
    tikinci_sany=Gundelik_sapak.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),).values('user__faa','month').distinct().annotate(sany=Sum(F('cyksapak_kg'))).order_by("month")
    
    zak_sw=Zakaz_SapakSwotka.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_kg')).values('month', 'gornus','onum','id','jemi_baha_m','jemi_baha_d','cyk_summa','cyk_summa_dol','gal_pey_summa','gal_pey_summa_dol','bellik').order_by("sene")
    pkk=sh.pk
    paginator = Paginator(ayjem, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'tikinci_sany':tikinci_sany,'zak_sw':zak_sw,'pkk':pkk}
    return render(request, 'shu/sapakseh_hasabatlar.html', context)

@login_required(login_url='login')
def AyjemiSapak_update(request, pk):
    page_title = _('Ýerinde bar bolan harydy girizmek')

    if request.method == 'POST':
        form = AyjemSapakUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            yerinde_bar_haryt = form.cleaned_data['yerinde_bar_haryt']
            bellik = form.cleaned_data['bellik']
            obj = AydakySapak_hasabat.objects.get(id=pk)
            obj.yerinde_bar_haryt=yerinde_bar_haryt
            if obj.ahyrky_galyndy == 0:
                obj.tapawudy = 0
            else:
                obj.tapawudy = obj.ahyrky_galyndy-yerinde_bar_haryt
            obj.bellik=bellik
            obj.sene=timezone.now()
            obj.save()
            messages.success(request, 'Aýdaky hasabata ýerinde bar bolan haryt girizildi!')
            return redirect('sapak-seh-hasabat',pk)
        else:
            messages.error(request, 'Ýalňyşlyk: ýerinde bar bolan haryt girizilmedi')
    else:
        form = AyjemSapakUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def ZakSwotkaSapak_update(request, pk):
    page_title = _('Çykdaýjylary girizmek')

    if request.method == 'POST':
        form = ZakSwotkaSapakUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            cyk_summa = form.cleaned_data['cyk_summa']
            cyk_summa_dol = form.cleaned_data['cyk_summa_dol']
            bellik = form.cleaned_data['bellik']
            obj = Zakaz_SapakSwotka.objects.get(id=pk)
            if cyk_summa is not None:
                obj.cyk_summa=cyk_summa
                obj.gal_pey_summa = obj.jemi_baha_m-cyk_summa
                obj.bellik=bellik
                obj.save()
            elif cyk_summa_dol is not None:
                obj.cyk_summa_dol=cyk_summa_dol
                obj.gal_pey_summa_dol=obj.jemi_baha_d-cyk_summa_dol
                obj.bellik=bellik
                obj.save()
            messages.success(request, 'Öndürilýän önüm üçin edilýän çykdaýjy girizildi!')
            return redirect('sapak-seh-hasabat',obj.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Öndürilýän önüm üçin edilýän çykdaýjy girizilmedi')
    else:
        form = ZakSwotkaSapakUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def SapakSeh_tabel(request):
    page_title = _('Sapak seh aýlyk hasabaty (Tabel)')
    cur_user=request.user
    tabel=Sapak_seh_ay_tabel.objects.all()

    if request.method == 'POST':
        form = SapakSeh_TabelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['user']
            oklady = form.cleaned_data['oklady']
            ay_isguni = form.cleaned_data['ay_isguni']
            is_gun_sagady = form.cleaned_data['is_gun_sagady']
            is_gun_sany = form.cleaned_data['is_gun_sany']
            artyk_is_sagady = form.cleaned_data['artyk_is_sagady']
            awans = form.cleaned_data['awans']
            kart_sum = form.cleaned_data['kart_sum']
            bellik = form.cleaned_data['bellik']

            aww = awans if awans is not None else 0
            kartjyk=kart_sum if kart_sum is not None else 0

            gun_dus_hak=oklady/ay_isguni
            sag_dus_hak=gun_dus_hak/is_gun_sagady
            el_al_sum=((is_gun_sany*gun_dus_hak)+(sag_dus_hak*artyk_is_sagady)-aww)-kartjyk

            t_create=Sapak_seh_ay_tabel.objects.create(user=user,oklady=oklady,ay_isguni=ay_isguni,
                                                       gune_dusyan_haky=gun_dus_hak,is_gun_sagady=is_gun_sagady,
                                                       sagat_dusyan_haky=sag_dus_hak,is_gun_sany=is_gun_sany,
                                                       artyk_is_sagady=artyk_is_sagady,awans=awans,
                                                       kart_sum=kart_sum,el_sum=el_al_sum,bellik=bellik)
            t_create.save()
            messages.success(request, 'Aýlyk zähmet hak hasabat (Tabel) girizildi!')
            return redirect('s-aylyk-tabel')
        else:
            messages.error(request, 'Ýalňyşlyk: Aýlyk zähmet hasabat (Tabel) girizilmedi!')
    else:
        form = SapakSeh_TabelForm()
    
    
    paginator = Paginator(tabel, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form}
    return render(request, 'shu/sapakseh_tabel.html', context)

@login_required(login_url='login')
def Sapakseh_edit(request, pk):
    page_title = _('Sapak sehde gündelik ödürilýän önümi üýtgetmek')
    obj = Gundelik_sapak.objects.get(id=pk)
    
    if request.method == 'POST':
        form = GunSapakForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sapak sehde gündelik ödürilýän önüm üýtgedildi!')
           return redirect('sapak-seh',pk)
    else:
        form = GunSapakForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Aydaky_sapak_edit(request, pk):
    page_title = _('Gündelik öndürilýän önümiň hasabatyny üýtgetmek')
    obj = Aydaky_sapak.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Aydaky_sapakForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Gündelik öndürilýän önümiň hasabaty üýtgedildi!')
           return redirect('sapak-seh',pk)
    else:
        form = Aydaky_sapakForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def AydakySapak_hasabat_edit(request, pk):
    page_title = _('Aýdaky sapagyň hasabatyny üýtgetmek')
    obj = AydakySapak_hasabat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = AydakySapak_hasabatForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýdaky sapagyň hasabaty üýtgedildi!')
           return redirect('sapak-seh-hasabat',pk)
    else:
        form = AydakySapak_hasabatForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sapak_seh_ay_tabel_edit(request, pk):
    page_title = _('Aýlyk zähmet hak hasabatyny (tabel) üýtgetmek')
    obj = Sapak_seh_ay_tabel.objects.get(id=pk)
    
    if request.method == 'POST':
        form = SapakSeh_TabelForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýlyk zähmet hak hasabaty (tabel) üýtgedildi!')
           return redirect('s-aylyk-tabel')
    else:
        form = SapakSeh_TabelForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sapakseh_Skladjyk(request,pk):
    page_title = _('Sapak sehdäki taýýar önümleriň hasabaty')
    sh=Sehler.objects.filter(pr_seh_id=pk).first()

    sap = Sapakseh_sklad.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_sapak')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_sapak_kg','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    pkk=sh.pk
    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'pkk':pkk}
    return render(request, 'shu/sapakseh_skladjyk.html', context)


# Dokma SEH
@login_required(login_url='login')
def Gun_ondDokma_sanaw(request,pk):
    page_title = _('Dokma sehde gündelik öndürilýän dokmalar we rulonlaryň sanawy')
    cur_user=request.user

    myseh = Gundelik_dokma.objects.filter(sehs_id=pk).order_by("sene")
    ay_has = Aydaky_dokma.objects.filter(sehs_id=pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_cyk_kg')).values('month', 'gornus','onum','id','jemi_bahasy_m','jemi_bahasy_d').order_by("sene")
    prpk=Sehler.objects.get(id=pk)
    seneid=Hasabat_sene.objects.all().last()
    
    if request.method == 'POST':
        form = GunDokmaForm(request.POST, request.FILES)
        form3 = TikinciAddForm(request.POST, request.FILES)
        if form.is_valid():
            # Sene insert etmek
            if seneid == None or seneid.sene.month is not datetime.now().month:
                sene_create=Hasabat_sene.objects.create(sene=timezone.now())
                sene_create.save()
                sene_create.refresh_from_db()
            else:
                pass
            
            user = form.cleaned_data['user']
            d_gornusi = form.cleaned_data['d_gornusi']
            cykrulon_kg = form.cleaned_data['cykrulon_kg']
            cykrulon_bahasy_m = form.cleaned_data['cykrulon_bahasy_m']
            cykrulon_bahasy_d = form.cleaned_data['cykrulon_bahasy_d']
            wozwrat_kg = form.cleaned_data['wozwrat_kg']
            katyska_agram = form.cleaned_data['katyska_agram']
            nirden_gelen = form.cleaned_data['nirden_gelen']
            enjam = form.cleaned_data['enjam']
            bellik = form.cleaned_data['bellik']

            seneid1=Hasabat_sene.objects.last().id

            dok=cykrulon_kg if cykrulon_kg is not None else 0
            dok_m=cykrulon_bahasy_m if cykrulon_bahasy_m is not None else 0
            dok_d=cykrulon_bahasy_d if cykrulon_bahasy_d is not None else 0
            
            # Gundelik haryt insert we Gundelik hasabat (Aydaky_halta) modele insert
            if cykrulon_bahasy_m is not None:
                ay_jem_baha_m = cykrulon_kg * cykrulon_bahasy_m
                ayhas = Aydaky_dokma.objects.create(offices=cur_user.office,sehs_id=pk,d_gornusi=d_gornusi,jemi_cyk_kg=cykrulon_kg,jemi_bahasy_m=ay_jem_baha_m)
                ayhas.save()
            elif cykrulon_bahasy_d is not None:
                ay_jem_baha_d = cykrulon_kg * cykrulon_bahasy_d
                ayhas = Aydaky_dokma.objects.create(offices=cur_user.office,sehs_id=pk,d_gornusi=d_gornusi,jemi_cyk_kg=cykrulon_kg,jemi_bahasy_d=ay_jem_baha_d)
                ayhas.save()

            guncreate = Gundelik_dokma.objects.create(user=user,has_sene=seneid1,offices=cur_user.office,sehs_id=pk,
                                                           d_gornusi=d_gornusi,cykrulon_kg=cykrulon_kg,cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,wozwrat_kg=wozwrat_kg,
                                                           katyska_agram=katyska_agram,nirden_gelen=nirden_gelen,enjam=enjam,bellik=bellik)
            guncreate.save()
                
            seneid2=list(Hasabat_sene.objects.all())[-2].id
            abj1=Gundelik_dokma.objects.filter(has_sene=seneid1)
            ay2=AydakyDokma_hasabat.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            ay3=AydakyDokma_hasabat.objects.all()
            
            sap_j=Gundelik_dokma.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('cykrulon_kg')))['total']
            wz_j=Gundelik_dokma.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('wozwrat_kg')))['total']
            ahg_j=AydakyDokma_hasabat.objects.filter(has_sene=seneid2,d_gornusi=d_gornusi).aggregate(total=Sum(F('ahyrky_galyndy')))['total']
            zak_j=Gundelik_dokma.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).aggregate(total=Sum(F('cykrulon_kg')))['total']

            a_j=sap_j if sap_j is not None else 0
            b_j=wz_j if wz_j is not None else 0
            c_j=zak_j if zak_j is not None else 0
            d_j=ahg_j if ahg_j is not None else 0

            # Aydaky hasabat insert we update
            if ay2 == 0:
                cur_ay_create = AydakyDokma_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                cur_ay_create.save()
            for x in ay3:
                if x.jemi_dok_rulon is not None and x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    ay_update = AydakyDokma_hasabat.objects.filter(has_sene=seneid1, d_gornusi=d_gornusi).update(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                elif ay2 > 0 and x.jemi_dok_rulon == None:
                    cur_ay_create = AydakyDokma_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                    cur_ay_create.save()
                continue

            #swotka sehin peydasyny cykarmaly
            swotka_count=Zakaz_DokmaSwotka.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            swotka=Zakaz_DokmaSwotka.objects.all()

            sklad_onum_count=Dokmaseh_sklad.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            sklad_onum=Dokmaseh_sklad.objects.all()

            if swotka_count == 0:
                swotka_create=Zakaz_DokmaSwotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * dok_m,jemi_baha_d=a_j * dok_d)
                swotka_create.save()
            for x in swotka:
                if x.jemi_kg is not None and x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    swotka_update = Zakaz_DokmaSwotka.objects.filter(~Q(jemi_kg=None),Q(has_sene=seneid1), Q(d_gornusi=d_gornusi)).update(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * dok_m,jemi_baha_d=a_j * dok_d)
                elif swotka_count > 0 and x.jemi_kg == None:
                    create_zak_swot=Zakaz_DokmaSwotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_kg=a_j,jemi_baha_m=a_j * dok_m,jemi_baha_d=a_j * dok_d)
                    create_zak_swot.save()
                continue

            if sklad_onum_count == 0:
                sk_onum_create=Dokmaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cykrulon_bahasy_m=dok_m,cykrulon_bahasy_d=dok_d,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                sk_onum_create.save()
            for x in sklad_onum:
                if x.jemi_dok_rulon is not None and x.has_sene == seneid1 and x.d_gornusi == d_gornusi:
                    sk_onum_update = Dokmaseh_sklad.objects.filter(~Q(jemi_dok_rulon=None),Q(has_sene=seneid1), Q(d_gornusi=d_gornusi)).update(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cykrulon_bahasy_m=dok_m,cykrulon_bahasy_d=dok_d,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                elif sklad_onum_count > 0 and x.jemi_dok_rulon == None:
                    create_sk_onum=Dokmaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,cykrulon_bahasy_m=dok_m,cykrulon_bahasy_d=dok_d,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,wozwrat=b_j,ahyrky_galyndy=d_j + a_j)
                    create_sk_onum.save()
                continue

            messages.success(request, 'Täze öndürilen dokma girizildi!')
            return redirect('dokma-seh', pk)
        
        if form3.is_valid():
            faa=form3.cleaned_data['faa']
            birth_date=form3.cleaned_data['birth_date']
            address=form3.cleaned_data['address']

            tikiciadd = Other_users.objects.create(sehs_id=pk,wez_id=1,faa=faa,birth_date=birth_date,address=address)
            tikiciadd.save()
            messages.success(request, f'{faa} täze zakazçy girizildi!')
            return redirect('dokma-seh',pk)
    else:
        form = GunDokmaForm()
        form3 = TikinciAddForm()
    
    # test2=Aydaky_dokma.objects.select_related('d_gornusi').annotate(
    #     month=TruncMonth('sene'),gornus=F('d_gornusi__name'),cur_off=F('offices')).values('month', 'gornus','cur_off').annotate(
    #         jemi_kg=Sum(F("jemi_cyk_kg"))).annotate(jemi_bahasy_m=Sum(F("jemi_bahasy_m"))).annotate(jemi_bahasy_d=Sum(F("jemi_bahasy_d")))
    pkk=prpk.pr_seh.pk
    # Paginator
    paginator = Paginator(myseh, 10)
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    paginator1 = Paginator(ay_has, 10)
    page1 = request.GET.get('page')
    try:
        ay_h = paginator1.get_page(page1)
    except PageNotAnInteger:
        ay_h = paginator1.page(1)
    except EmptyPage:
        ay_h = paginator1.page(paginator1.num_pages)

    context = {'title': page_title,'myuser':myuser, 'ay_h':ay_h,'form':form,'form3':form3,'pkk':pkk}
    return render(request, 'shu/dokmaseh.html', context)

@login_required(login_url='login')
def Dokmaseh_zakaz(request, pk):
    page_title = _('Täze zakaz girizmek')
    seneid=Hasabat_sene.objects.all().last()
    cur_user=request.user
    
    if request.method == 'POST':
        form2 = ZakazDokmaForm(request.POST, request.FILES)
        if form2.is_valid():
            if seneid == None or seneid.sene.month is not datetime.now().month:
                sene_create=Hasabat_sene.objects.create(sene=timezone.now())
                sene_create.save()
                sene_create.refresh_from_db()
            else:
                pass
            zcode=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
            
            cur_code = []
            for deg in zcode:
                c=deg.haryt_code
                cur_code.append({'c':c})

            user = form2.cleaned_data['user']
            zakaz_user = form2.cleaned_data['zakaz_user']
            d_gornusi = form2.cleaned_data['d_gornusi']
            cykrulon_kg = form2.cleaned_data['cykrulon_kg']
            cykrulon_bahasy_m = form2.cleaned_data['cykrulon_bahasy_m']
            cykrulon_bahasy_d = form2.cleaned_data['cykrulon_bahasy_d']
            wozwrat_kg = form2.cleaned_data['wozwrat_kg']
            katyska_agram = form2.cleaned_data['katyska_agram']
            nirden_gelen = form2.cleaned_data['nirden_gelen']
            enjam = form2.cleaned_data['enjam']
            bellik = form2.cleaned_data['bellik']

            seneid1=Hasabat_sene.objects.last().id
            limit=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
            
            # Gundelik haryt insert we Gundelik hasabat (Aydaky_sapak) modele insert
            for deg in limit:
                rb1=deg.algy-cykrulon_kg*deg.bahasy
                if deg.algy != 0:
                    s=deg.algy/deg.bahasy
                    if s >= cykrulon_kg:
                        zakgun = Gundelik_dokma.objects.create(has_sene=seneid1,user=user,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,sehs_id=pk,
                                                               d_gornusi=d_gornusi,cykrulon_kg=cykrulon_kg,cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,wozwrat_kg=wozwrat_kg,
                                                               katyska_agram=katyska_agram,nirden_gelen=nirden_gelen,enjam=enjam,bellik=bellik)
                        zakgun.save()

                        up=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code'])).update(algy = rb1)
                        
                        if cykrulon_bahasy_m is not None:
                            ay_jem_baha_m = cykrulon_kg * cykrulon_bahasy_m
                            ayhas = Aydaky_dokma.objects.create(sehs_id=pk,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,d_gornusi=d_gornusi,jemi_cyk_kg=cykrulon_kg,jemi_bahasy_m=ay_jem_baha_m)
                            ayhas.save()
                        elif cykrulon_bahasy_d is not None:
                            ay_jem_baha_d = cykrulon_kg * cykrulon_bahasy_d
                            ayhas = Aydaky_dokma.objects.create(sehs_id=pk,zakaz_user=zakaz_user,zakaz_code=c,offices=cur_user.office,d_gornusi=d_gornusi,jemi_cyk_kg=cykrulon_kg,jemi_bahasy_d=ay_jem_baha_d)
                            ayhas.save()

            seneid2=list(Hasabat_sene.objects.all())[-2].id
            abj1=Gundelik_dokma.objects.filter(has_sene=seneid1)
            ay2=AydakyDokma_hasabat.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).count()
            ay3=AydakyDokma_hasabat.objects.all()
            
            sap_j=Gundelik_dokma.objects.filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('cykrulon_kg',flat=True)
            wz_j=Gundelik_dokma.objects.exclude(wozwrat_kg=None).filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('wozwrat_kg',flat=True)
            ahg_j=AydakyDokma_hasabat.objects.filter(has_sene=seneid2,d_gornusi=d_gornusi).values_list('ahyrky_galyndy',flat=True)
            zak_j=Gundelik_dokma.objects.exclude(zakaz_user=None).filter(has_sene=seneid1,d_gornusi=d_gornusi).values_list('cykrulon_kg',flat=True)

            a_j=sap_j if sap_j is not None else 0
            b_j=wz_j if wz_j is not None else 0
            c_j=zak_j if zak_j is not None else 0
            d_j=ahg_j if ahg_j is not None else 0

            # Aydaky hasabat insert we update
            if ay2 == 0:
                cur_ay_create = AydakyDokma_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
                cur_ay_create.save()
            for x in ay3:
                if ay2 > 0 and x.has_sene is not seneid1 and x.d_gornusi is not d_gornusi:
                    cur_ay_create = AydakyDokma_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(d_gornusi=d_gornusi)).create(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
                    cur_ay_create.save()
                else:
                    ay_update = AydakyDokma_hasabat.objects.filter(has_sene=seneid1, d_gornusi=d_gornusi).update(cykrulon_bahasy_m=cykrulon_bahasy_m,cykrulon_bahasy_d=cykrulon_bahasy_d,zakaz_user=zakaz_user,zakaz_code=c,sehs_id=pk,has_sene=seneid1,d_gornusi=d_gornusi,jemi_dok_rulon=a_j,gecenay_galyndy=d_j,satylan_dokma_kg=c_j,wozwrat=b_j,ahyrky_galyndy=(d_j + a_j) - c_j)
                    
            sene_zak=Hasabat_sene.objects.last()
            seneid3=Hasabat_sene.objects.earliest('sene')
            zak_bal=Zakaz_balans.objects.all()
            zak_swS=Zakaz_DokmaSwotka.objects.all().count()
            zak_sw=Zakaz_DokmaSwotka.objects.all()

            senejik=list(Hasabat_sene.objects.all())[-2]
            tot_kg=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(j_kg=Sum(F("cyk_rulon_kg"))).values_list('j_kg',flat=True)
            tot_bah=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(j_baha=Sum(F("balans"))).values_list('j_baha',flat=True)
            baha_tot=Zakaz_balans.objects.filter(zakaz_sene__month=senejik.sene.month).annotate(baha_j=Sum(F("bahasy"))).values_list('baha_j',flat=True)

            # Zakazçy tarapyndan gelyan peýda we çykdaýjy hasabat (Zakaz_swotka) insert we update
            if zak_swS == 0:
                create_zak_swot=Zakaz_DokmaSwotka.objects.filter(Q(sene_id=None) | ~Q(sene_id=seneid1)).create(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
                create_zak_swot.save()
            for i in zak_sw:
                if zak_swS > 0 and i.sene_id==None and i.sene_id is not seneid1:
                    create_zak_swot=Zakaz_DokmaSwotka.objects.filter(Q(sene_id=None) | ~Q(sene_id=seneid1)).create(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
                    create_zak_swot.save()
                else:
                    up_zak_swot=Zakaz_DokmaSwotka.objects.filter(sene_id=seneid1).update(sehs_id=pk,sene_id=seneid1,jemi_kg=sum(tot_kg),bahasy=mean(baha_tot),jemi_gir_baha=sum(tot_bah))
            messages.success(request, 'Täze ZAKAZ üçin öndürilen dokma we rulon girizildi!')
            return redirect('dokma-seh',pk)
    else:
        form2 = ZakazDokmaForm()

    context = {'title': page_title,'form2': form2}
    return render(request, 'shu/dokmaseh_zakaz.html', context)

@login_required(login_url='login')
def Dokmaseh_hasabat(request,pk):
    page_title = _('Aýdaky hasabatlar')
    tt=Other_users.objects.filter(wez="1")
    sh=Sehler.objects.filter(pr_seh_id=pk).first()


    ayjem = AydakyDokma_hasabat.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_rulon')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_dokma_kg','wozwrat','ahyrky_galyndy','yerinde_bar_haryt','tapawudy','bellik').order_by("sene")
    tikinci_sany=Gundelik_dokma.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),).values('user__faa','month').distinct().annotate(sany=Sum(F('cykrulon_kg'))).order_by("month")
    zak_sw=Zakaz_DokmaSwotka.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_kg')).values('month', 'gornus','onum','id','jemi_baha_m','jemi_baha_d','cyk_summa','cyk_summa_dol','gal_pey_summa','gal_pey_summa_dol','bellik').order_by("sene")
    pkk=sh.pk
    paginator = Paginator(ayjem, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'tikinci_sany':tikinci_sany,'zak_sw':zak_sw,'pkk':pkk}
    return render(request, 'shu/dokmaseh_hasabatlar.html', context)

@login_required(login_url='login')
def AyjemiDokma_update(request, pk):
    page_title = _('Ýerinde bar bolan harydy girizmek')

    if request.method == 'POST':
        form = AyjemDokmaUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            yerinde_bar_haryt = form.cleaned_data['yerinde_bar_haryt']
            bellik = form.cleaned_data['bellik']
            obj = AydakyDokma_hasabat.objects.get(id=pk)
            obj.yerinde_bar_haryt=yerinde_bar_haryt
            if obj.ahyrky_galyndy == 0:
                obj.tapawudy = 0
            else:
                obj.tapawudy = obj.ahyrky_galyndy-yerinde_bar_haryt
            obj.bellik=bellik
            obj.sene=timezone.now()
            obj.save()
            messages.success(request, 'Aýdaky hasabata ýerinde bar bolan haryt girizildi!')
            return redirect('dokma-seh-hasabat',pk)
        else:
            messages.error(request, 'Ýalňyşlyk: ýerinde bar bolan haryt girizilmedi')
    else:
        form = AyjemDokmaUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def ZakSwotkaDokma_update(request, pk):
    page_title = _('Çykdaýjylary girizmek')

    if request.method == 'POST':
        form = ZakSwotkaDokmaUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            cyk_summa = form.cleaned_data['cyk_summa']
            cyk_summa_dol = form.cleaned_data['cyk_summa_dol']
            bellik = form.cleaned_data['bellik']
            obj = Zakaz_DokmaSwotka.objects.get(id=pk)
            if cyk_summa is not None:
                obj.cyk_summa=cyk_summa
                obj.gal_pey_summa = obj.jemi_baha_m-cyk_summa
                obj.bellik=bellik
                obj.save()
            elif cyk_summa_dol is not None:
                obj.cyk_summa_dol=cyk_summa_dol
                obj.gal_pey_summa_dol=obj.jemi_baha_d-cyk_summa_dol
                obj.bellik=bellik
                obj.save()
            messages.success(request, 'Öndürilýän önüm üçin edilýän çykdaýjy girizildi!')
            return redirect('dokma-seh-hasabat',obj.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Öndürilýän önüm üçin edilýän çykdaýjy girizilmedi')
    else:
        form = ZakSwotkaDokmaUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def DokmaSeh_tabel(request):
    page_title = _('Dokma seh aýlyk hasabaty (Tabel)')
    cur_user=request.user
    tabel=Dokma_seh_ay_tabel.objects.all()

    if request.method == 'POST':
        form = DokmaSeh_TabelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['user']
            oklady = form.cleaned_data['oklady']
            ay_isguni = form.cleaned_data['ay_isguni']
            is_gun_sagady = form.cleaned_data['is_gun_sagady']
            is_gun_sany = form.cleaned_data['is_gun_sany']
            artyk_is_sagady = form.cleaned_data['artyk_is_sagady']
            awans = form.cleaned_data['awans']
            kart_sum = form.cleaned_data['kart_sum']
            bellik = form.cleaned_data['bellik']

            aww = awans if awans is not None else 0
            kartjyk=kart_sum if kart_sum is not None else 0

            gun_dus_hak=oklady/ay_isguni
            sag_dus_hak=gun_dus_hak/is_gun_sagady
            el_al_sum=((is_gun_sany*gun_dus_hak)+(sag_dus_hak*artyk_is_sagady)-aww)-kartjyk

            t_create=Dokma_seh_ay_tabel.objects.create(user=user,oklady=oklady,ay_isguni=ay_isguni,
                                                       gune_dusyan_haky=gun_dus_hak,is_gun_sagady=is_gun_sagady,
                                                       sagat_dusyan_haky=sag_dus_hak,is_gun_sany=is_gun_sany,
                                                       artyk_is_sagady=artyk_is_sagady,awans=awans,
                                                       kart_sum=kart_sum,el_sum=el_al_sum,bellik=bellik)
            t_create.save()
            messages.success(request, 'Aýlyk zähmet hak hasabat (Tabel) girizildi!')
            return redirect('d-aylyk-tabel')
        else:
            messages.error(request, 'Ýalňyşlyk: Aýlyk zähmet hasabat (Tabel) girizilmedi!')
    else:
        form = DokmaSeh_TabelForm()
    
    
    paginator = Paginator(tabel, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form}
    return render(request, 'shu/dokmaseh_tabel.html', context)

@login_required(login_url='login')
def Dokmaseh_edit(request, pk):
    page_title = _('Dokma sehde gündelik ödürilýän önümi üýtgetmek')
    obj = Gundelik_dokma.objects.get(id=pk)
    
    if request.method == 'POST':
        form = GunDokmaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Dokma sehde gündelik ödürilýän önüm üýtgedildi!')
           return redirect('dokma-seh',pk)
    else:
        form = GunDokmaForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Aydaky_dokma_edit(request, pk):
    page_title = _('Gündelik öndürilýän önümiň hasabatyny üýtgetmek')
    obj = Aydaky_dokma.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Aydaky_dokmaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Gündelik öndürilýän önümiň hasabaty üýtgedildi!')
           return redirect('sapak-seh',pk)
    else:
        form = Aydaky_dokmaForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def AydakyDokma_hasabat_edit(request, pk):
    page_title = _('Aýdaky önümiň hasabatyny üýtgetmek')
    obj = AydakyDokma_hasabat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = AydakyDokma_hasabatForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýdaky ňnümiň hasabaty üýtgedildi!')
           return redirect('dokma-seh-hasabat',pk)
    else:
        form = AydakyDokma_hasabatForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Dokma_seh_ay_tabel_edit(request, pk):
    page_title = _('Aýlyk zähmet hak hasabatyny (tabel) üýtgetmek')
    obj = Dokma_seh_ay_tabel.objects.get(id=pk)
    
    if request.method == 'POST':
        form = DokmaSeh_TabelForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýlyk zähmet hak hasabaty (tabel) üýtgedildi!')
           return redirect('d-aylyk-tabel')
    else:
        form = DokmaSeh_TabelForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Dokmaseh_Skladjyk(request,pk):
    page_title = _('Dokma sehdäki taýýar önümleriň hasabaty')
    sh=Sehler.objects.filter(pr_seh_id=pk).first()

    sap = Dokmaseh_sklad.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_rulon')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_dokma_kg','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    pkk=sh.pk
    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'pkk':pkk}
    return render(request, 'shu/dokmaseh_skladjyk.html', context)


# Halta SEH
@login_required(login_url='login')
def Gun_tikhalta_sanaw(request,pk):
    page_title = _('Halta sehde gündelik tikilýän haltalaryň sanawy')
    cur_user=request.user

    myseh = Gundelik_halta.objects.filter(sehs_id=pk).order_by("sene")
    ay_has = Aydaky_halta.objects.filter(sehs_id=pk).annotate(month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),abat=F('abathalta_sany'),brak=F('brakhalta_sany'),ganar=F('ganarhalta_sany')).values(
        'month','gornus','olceg','abat','brak','ganar','id','abathalta_kg','brakhalta_kg','ganarhalta_kg','jemi_abat_baha_m','jemi_abat_baha_d','jemi_brak_baha_m','jemi_brak_baha_d','jemi_ganar_baha_m','jemi_ganar_baha_d').order_by("sene")
    prpk=Sehler.objects.get(id=pk)

    seneid=Hasabat_sene.objects.all().last()
    prr=prpk.pr_seh.pk
    form = GunhaltaForm(request.POST, request.FILES)
    form3 = TikinciAddForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            # Sene insert etmek
            if seneid == None or seneid.sene.month is not datetime.now().month:
                sene_create=Hasabat_sene.objects.create(sene=timezone.now())
                sene_create.save()
                sene_create.refresh_from_db()
            else:
                pass
            
            user = form.cleaned_data['user']
            h_gornusi = form.cleaned_data['h_gornusi']
            h_olceg = form.cleaned_data['h_olceg']
            abathalta_sany = form.cleaned_data['abathalta_sany']
            abathalta_bahasy_m = form.cleaned_data['abathalta_bahasy_m']
            abathalta_bahasy_d = form.cleaned_data['abathalta_bahasy_d']
            abathalta_kg = form.cleaned_data['abathalta_kg']
            brakhalta_sany = form.cleaned_data['brakhalta_sany']
            brakhalta_bahasy_m = form.cleaned_data['brakhalta_bahasy_m']
            brakhalta_bahasy_d = form.cleaned_data['brakhalta_bahasy_d']
            brakhalta_kg = form.cleaned_data['brakhalta_kg']
            ganarhalta_sany = form.cleaned_data['ganarhalta_sany']
            ganarhalta_bahasy_m = form.cleaned_data['ganarhalta_bahasy_m']
            ganarhalta_bahasy_d = form.cleaned_data['ganarhalta_bahasy_d']
            ganarhalta_kg = form.cleaned_data['ganarhalta_kg']
            sarp_sapak_kg = form.cleaned_data['sarp_sapak_kg']
            wozwrat_kg = form.cleaned_data['wozwrat_kg']
            katyska_agram = form.cleaned_data['katyska_agram']
            nirden_gelen = form.cleaned_data['nirden_gelen']
            enjam = form.cleaned_data['enjam']
            bellik = form.cleaned_data['bellik']

            seneid1=Hasabat_sene.objects.last().id
            seneid2=list(Hasabat_sene.objects.all())[-2].id

            a_kg = abathalta_kg if abathalta_kg is not None else 0
            b_kg = brakhalta_kg if brakhalta_kg is not None else 0
            c_kg = ganarhalta_kg if ganarhalta_kg is not None else 0

            a_san = abathalta_sany if abathalta_sany is not None else 0
            b_san = brakhalta_sany if brakhalta_sany is not None else 0
            c_san = ganarhalta_sany if ganarhalta_sany is not None else 0

            a_m = abathalta_bahasy_m if abathalta_bahasy_m is not None else 0
            b_m = brakhalta_bahasy_m if brakhalta_bahasy_m is not None else 0
            c_m = ganarhalta_bahasy_m if ganarhalta_bahasy_m is not None else 0

            a_d = abathalta_bahasy_d if abathalta_bahasy_d is not None else 0
            b_d = brakhalta_bahasy_d if brakhalta_bahasy_d is not None else 0
            c_d = ganarhalta_bahasy_d if ganarhalta_bahasy_d is not None else 0
            
            abatlai=Aydaky_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('abathalta_sany')))['total']
            braklai=Aydaky_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('brakhalta_sany')))['total']
            ganarlai=Aydaky_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ganarhalta_sany')))['total']

            # Gundelik haryt insert we Gundelik hasabat (Aydaky_halta) modele insert
            if abathalta_bahasy_m is not None or brakhalta_bahasy_m is not None or ganarhalta_bahasy_m is not None:
                ayhas = Aydaky_halta.objects.create(sehs_id=pk,office=cur_user.office,h_olceg=h_olceg,h_gornusi=h_gornusi,
                                                    abathalta_sany=abathalta_sany,abathalta_kg=abathalta_kg,
                                                    brakhalta_sany=brakhalta_sany,brakhalta_kg=brakhalta_kg,
                                                    ganarhalta_sany=ganarhalta_sany,ganarhalta_kg=ganarhalta_kg,
                                                    jemi_abat_sany=abatlai,jemi_brak_sany=braklai,jemi_ganar_sany=ganarlai,
                                                    jemi_abat_baha_m=a_san * a_m,jemi_brak_baha_m=b_san * b_m,jemi_ganar_baha_m=c_san*c_m)
                ayhas.save()
            elif abathalta_bahasy_d is not None or brakhalta_bahasy_d is not None or ganarhalta_bahasy_d is not None:
                ayhas = Aydaky_halta.objects.create(sehs_id=pk,office=cur_user.office,h_olceg=h_olceg,h_gornusi=h_gornusi,
                                                    abathalta_sany=abathalta_sany,abathalta_kg=abathalta_kg,
                                                    brakhalta_sany=brakhalta_sany,brakhalta_kg=brakhalta_kg,
                                                    ganarhalta_sany=ganarhalta_sany,ganarhalta_kg=ganarhalta_kg,
                                                    jemi_abat_sany=abatlai,jemi_brak_sany=braklai,jemi_ganar_sany=ganarlai,
                                                    jemi_abat_baha_d=a_san * a_d,jemi_brak_baha_d=b_san * b_d,jemi_ganar_baha_d=c_san*c_d)
                ayhas.save()

            guncreate = Gundelik_halta.objects.create(user=user,has_sene=seneid1,h_olceg=h_olceg,office=cur_user.office,sehs_id=pk,
                                                           h_gornusi=h_gornusi,abathalta_sany=abathalta_sany,abathalta_bahasy_m=abathalta_bahasy_m,abathalta_bahasy_d=abathalta_bahasy_d,abathalta_kg=abathalta_kg,
                                                           brakhalta_sany=brakhalta_sany,brakhalta_bahasy_m=brakhalta_bahasy_m,brakhalta_bahasy_d=brakhalta_bahasy_d,brakhalta_kg=brakhalta_kg,ganarhalta_sany=ganarhalta_sany,
                                                           ganarhalta_bahasy_m=ganarhalta_bahasy_m,ganarhalta_bahasy_d=ganarhalta_bahasy_d,ganarhalta_kg=ganarhalta_kg,sarp_sapak_kg=sarp_sapak_kg,wozwrat_kg=wozwrat_kg,
                                                           katyska_agram=katyska_agram,nirden_gelen=nirden_gelen,enjam=enjam,bellik=bellik)
            guncreate.save()
                
            
            abj1=Gundelik_halta.objects.filter(has_sene=seneid1)
            ay2=Aydakyhalta_hasabat.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).count()
            ay3=Aydakyhalta_hasabat.objects.all()
            
            ab_j=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('abathalta_sany')))['total']
            brak_j=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('brakhalta_sany')))['total']
            ganar_j=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ganarhalta_sany')))['total']
            abat_kg=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('abathalta_kg')))['total']
            brak_kg=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('brakhalta_kg')))['total']
            ganar_kg=Gundelik_halta.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ganarhalta_kg')))['total']
            wz_j=Gundelik_halta.objects.exclude(wozwrat_kg=None).filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('wozwrat_kg')))['total']
            abat_ahg=Aydakyhalta_hasabat.objects.filter(has_sene=seneid2,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ahyrky_galyndy_abat')))['total']
            brak_ahg=Aydakyhalta_hasabat.objects.filter(has_sene=seneid2,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ahyrky_galyndy_brak')))['total']
            ganar_ahg=Aydakyhalta_hasabat.objects.filter(has_sene=seneid2,h_gornusi=h_gornusi,h_olceg=h_olceg).aggregate(total=Sum(F('ahyrky_galyndy_ganar')))['total']
            
            abatjyk=ab_j if ab_j is not None else 0
            brakjyk=brak_j if brak_j is not None else 0
            ganarjyk=ganar_j if ganar_j is not None else 0

            abatkg=abat_kg if abat_kg is not None else 0
            brakkg=brak_kg if brak_kg is not None else 0
            ganarkg=ganar_kg if ganar_kg is not None else 0

            b_j=wz_j if wz_j is not None else 0
            ahg_bir=abat_ahg if abat_ahg is not None else 0
            ahg_iki=brak_ahg if brak_ahg is not None else 0
            ahg_uc=ganar_ahg if ganar_ahg is not None else 0

            #swotka sehin peydasyny cykarmaly
            swotka_count=Zakaz_swotka.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).count()
            swotka=Zakaz_swotka.objects.all()

            sklad_onum_count=Haltaseh_sklad.objects.filter(has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg).count()
            sklad_onum=Haltaseh_sklad.objects.all()

            if abathalta_sany is not None:
                if ay2 == 0:
                    cur_ay_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                    abathalta_sany=abatjyk,abathalta_bahasy_m=abathalta_bahasy_m,
                                                                                                                                                                    abathalta_bahasy_d=abathalta_bahasy_d,abathalta_kg=abatkg,
                                                                                                                                                                    gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy_abat=ahg_bir + abatjyk)
                    cur_ay_create.save()
                for x in ay3:
                    if x.abathalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        ay_update = Aydakyhalta_hasabat.objects.filter(~Q(abathalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi), Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        abathalta_sany=abatjyk,abathalta_bahasy_m=abathalta_bahasy_m,
                                                                                                                                                                        abathalta_bahasy_d=abathalta_bahasy_d,abathalta_kg=abatkg,
                                                                                                                                                                        gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy_abat=ahg_bir + abatjyk)
                        
                    elif ay2 > 0 and x.abathalta_sany == None:
                        hasabat_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        abathalta_sany=abatjyk,abathalta_bahasy_m=abathalta_bahasy_m,
                                                                                                                                                                        abathalta_bahasy_d=abathalta_bahasy_d,abathalta_kg=abatkg,
                                                                                                                                                                        gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy_abat=ahg_bir + abatjyk)
                        hasabat_create.save()
                    continue

                if swotka_count == 0:
                    swotka_create=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_sany=abatjyk,jemi_baha_m=abatjyk * a_m,jemi_baha_d=abatjyk * a_d)
                    swotka_create.save()
                for x in swotka:
                    if x.abathalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        swotka_update = Zakaz_swotka.objects.filter(~Q(abathalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_sany=abatjyk,jemi_baha_m=abatjyk * a_m,jemi_baha_d=abatjyk * a_d)
                    elif swotka_count > 0 and x.abathalta_sany == None:
                        create_zak_swot=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_sany=abatjyk,jemi_baha_m=abatjyk * a_m,jemi_baha_d=abatjyk * a_d)
                        create_zak_swot.save()
                    continue

                if sklad_onum_count == 0:
                    sk_onum_create=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_bahasy_m=a_m,abathalta_bahasy_d=a_d,abathalta_sany=abatjyk,gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy=ahg_bir + abatjyk)
                    sk_onum_create.save()
                for x in sklad_onum:
                    if x.abathalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        sk_onum_update = Haltaseh_sklad.objects.filter(~Q(abathalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_bahasy_m=a_m,abathalta_bahasy_d=a_d,abathalta_sany=abatjyk,gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy=ahg_bir + abatjyk)
                    elif sklad_onum_count > 0 and x.abathalta_sany == None:
                        create_sk_onum=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,abathalta_bahasy_m=a_m,abathalta_bahasy_d=a_d,abathalta_sany=abatjyk,gecenay_galyndy=ahg_bir,wozwrat=b_j,ahyrky_galyndy=ahg_bir + abatjyk)
                        create_sk_onum.save()
                    continue

            elif brakhalta_sany is not None:
                if ay2 == 0:
                    cur_ay_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        brakhalta_sany=abatjyk,brakhalta_bahasy_m=brakhalta_bahasy_m,
                                                                                                                                                                        brakhalta_bahasy_d=brakhalta_bahasy_d,brakhalta_kg=brakkg,
                                                                                                                                                                        gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy_brak=ahg_iki + brakjyk)
                    cur_ay_create.save()
                for x in ay3:
                    if x.brakhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        ay_update = Aydakyhalta_hasabat.objects.filter(~Q(brakhalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi), Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        brakhalta_sany=abatjyk,brakhalta_bahasy_m=brakhalta_bahasy_m,
                                                                                                                                                                        brakhalta_bahasy_d=brakhalta_bahasy_d,brakhalta_kg=brakkg,
                                                                                                                                                                        gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy_brak=ahg_iki + brakjyk)
                        
                    elif ay2 > 0 and x.brakhalta_sany == None:
                        hasabat_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        brakhalta_sany=abatjyk,brakhalta_bahasy_m=brakhalta_bahasy_m,
                                                                                                                                                                        brakhalta_bahasy_d=brakhalta_bahasy_d,brakhalta_kg=brakkg,
                                                                                                                                                                        gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy_brak=ahg_iki + brakjyk)
                        hasabat_create.save()
                    continue

                if swotka_count == 0:
                    swotka_create=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_sany=brakjyk,jemi_baha_m=brakjyk * b_m,jemi_baha_d=brakjyk * b_d)
                    swotka_create.save()
                for x in swotka:
                    if x.brakhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        swotka_update = Zakaz_swotka.objects.filter(~Q(brakhalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_sany=brakjyk,jemi_baha_m=brakjyk * b_m,jemi_baha_d=brakjyk * b_d)
                    elif swotka_count > 0 and x.brakhalta_sany == None:
                        create_zak_swot=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_sany=brakjyk,jemi_baha_m=brakjyk * b_m,jemi_baha_d=brakjyk * b_d)
                        create_zak_swot.save()
                    continue

                if sklad_onum_count == 0:
                    sk_onum_create=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_bahasy_m=b_m,brakhalta_bahasy_d=b_d,brakhalta_sany=brakjyk,gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy=ahg_iki + brakjyk)
                    sk_onum_create.save()
                for x in sklad_onum:
                    if x.brakhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        sk_onum_update = Haltaseh_sklad.objects.filter(~Q(brakhalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_bahasy_m=b_m,brakhalta_bahasy_d=b_d,brakhalta_sany=brakjyk,gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy=ahg_iki + brakjyk)
                    elif sklad_onum_count > 0 and x.brakhalta_sany == None:
                        create_sk_onum=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,brakhalta_bahasy_m=b_m,brakhalta_bahasy_d=b_d,brakhalta_sany=brakjyk,gecenay_galyndy=ahg_iki,wozwrat=b_j,ahyrky_galyndy=ahg_iki + brakjyk)
                        create_sk_onum.save()
                    continue

            elif ganarhalta_sany is not None:
                if ay2 == 0:
                    cur_ay_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                    ganarhalta_sany=ganarjyk,ganarhalta_bahasy_m=ganarhalta_bahasy_m,
                                                                                                                                                                    ganarhalta_bahasy_d=ganarhalta_bahasy_d,ganarhalta_kg=ganarkg,
                                                                                                                                                                    gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy_ganar=ahg_uc + ganarjyk)
                    cur_ay_create.save()
                for x in ay3:
                    if x.ganarhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        ay_update = Aydakyhalta_hasabat.objects.filter(~Q(abathalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi), Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        ganarhalta_sany=ganarjyk,ganarhalta_bahasy_m=ganarhalta_bahasy_m,
                                                                                                                                                                        ganarhalta_bahasy_d=ganarhalta_bahasy_d,ganarhalta_kg=ganarkg,
                                                                                                                                                                        gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy_ganar=ahg_uc + ganarjyk)
                        
                    elif ay2 > 0 and x.ganarhalta_sany == None:
                        hasabat_create = Aydakyhalta_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,
                                                                                                                                                                        ganarhalta_sany=ganarjyk,ganarhalta_bahasy_m=ganarhalta_bahasy_m,
                                                                                                                                                                        ganarhalta_bahasy_d=ganarhalta_bahasy_d,ganarhalta_kg=ganarkg,
                                                                                                                                                                        gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy_ganar=ahg_uc + ganarjyk)
                        hasabat_create.save()
                    continue

                if swotka_count == 0:
                    swotka_create=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_sany=ganarjyk,jemi_baha_m=ganarjyk * c_m,jemi_baha_d=ganarjyk * c_d)
                    swotka_create.save()
                for x in swotka:
                    if x.ganarhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        swotka_update = Zakaz_swotka.objects.filter(~Q(ganarhalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_sany=ganarjyk,jemi_baha_m=ganarjyk * c_m,jemi_baha_d=ganarjyk * c_d)
                    elif swotka_count > 0 and x.ganarhalta_sany == None:
                        create_zak_swot=Zakaz_swotka.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_sany=ganarjyk,jemi_baha_m=ganarjyk * c_m,jemi_baha_d=ganarjyk * c_d)
                        create_zak_swot.save()
                    continue

                if sklad_onum_count == 0:
                    sk_onum_create=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_bahasy_m=c_m,ganarhalta_bahasy_d=c_d,ganarhalta_sany=ganarjyk,gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy=ahg_uc + ganarjyk)
                    sk_onum_create.save()
                for x in sklad_onum:
                    if x.ganarhalta_sany is not None and x.has_sene == seneid1 and x.h_gornusi == h_gornusi and x.h_olceg == h_olceg:
                        sk_onum_update = Haltaseh_sklad.objects.filter(~Q(ganarhalta_sany=None),Q(has_sene=seneid1), Q(h_gornusi=h_gornusi),Q(h_olceg=h_olceg)).update(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_bahasy_m=c_m,ganarhalta_bahasy_d=c_d,ganarhalta_sany=ganarjyk,gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy=ahg_uc + ganarjyk)
                    elif sklad_onum_count > 0 and x.ganarhalta_sany == None:
                        create_sk_onum=Haltaseh_sklad.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1), ~Q(h_gornusi=h_gornusi),~Q(h_olceg=h_olceg)).create(sehs_id=pk,has_sene=seneid1,h_gornusi=h_gornusi,h_olceg=h_olceg,ganarhalta_bahasy_m=c_m,ganarhalta_bahasy_d=c_d,ganarhalta_sany=ganarjyk,gecenay_galyndy=ahg_uc,wozwrat=b_j,ahyrky_galyndy=ahg_uc + ganarjyk)
                        create_sk_onum.save()
                    continue
            
            messages.success(request, 'Täze tikilen halta girizildi!')
            return redirect('halta-seh',pk)
        
        if form3.is_valid():
            faa=form3.cleaned_data['faa']
            birth_date=form3.cleaned_data['birth_date']
            address=form3.cleaned_data['address']

            tikiciadd = Other_users.objects.create(seh_id=pk,wez_id=1,faa=faa,birth_date=birth_date,address=address)
            tikiciadd.save()
            messages.success(request, f'{faa} täze zakazçy girizildi!')
            return redirect('halta-seh',pk)
    else:
        form = GunhaltaForm()
        form3 = TikinciAddForm()

    # test2=Aydaky_halta.objects.select_related('h_gornusi').annotate(
    #     month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),cur_off=F('office')).values('month', 'gornus','olceg','cur_off').annotate(
    #         jemi_sany=Sum(F("jemi_sany"))).annotate(jemi_kg=Sum(F("jemi_kg"))).annotate(jemi_bahasy_m=Sum(F("jemi_bahasy_m"))).annotate(jemi_bahasy_d=Sum(F("jemi_bahasy_d")))

    paginator = Paginator(myseh, 10)
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    paginator1 = Paginator(ay_has, 10)
    page1 = request.GET.get('page')
    try:
        ay_h = paginator1.get_page(page1)
    except PageNotAnInteger:
        ay_h = paginator1.page(1)
    except EmptyPage:
        ay_h = paginator1.page(paginator1.num_pages)

    context = {'title': page_title,'myuser':myuser, 'ay_h':ay_h,'form':form,'form3':form3,'prr':prr}
    return render(request, 'shu/haltaseh.html', context)

@login_required(login_url='login')
def load_zakaz(request):
    zakaz_user_id = request.GET.get('zakaz_user_id')
    zak_code = Zakaz_balans.objects.filter(user_id=zakaz_user_id).filter(~Q(algy=0)).all()
    cur_code = []
    for deg in zak_code:
        c=deg.haryt_code
        cur_code.append(deg.haryt_code)
    
    # sizam=cur_code
    # print(sizam)

    context = {'zak_code': zak_code}
    return render(request, 'shu/zak_code.html', context)

@login_required(login_url='login')
def load_gornus(request):
    zakaz_code_id = request.GET.get('zakaz_code_id')
    zak_gor = Zakaz_balans.objects.filter(id=zakaz_code_id).filter(~Q(algy=0)).first()
    j_sany=zak_gor.algy/zak_gor.bahasy
    # print(z_g)
    context = {'z_g': {'id': zak_gor.h_gornusi.id, 'name': zak_gor.h_gornusi.name}, 'olceg': zak_gor.h_olceg,'j_sany':j_sany}
    return JsonResponse(context)

@login_required(login_url='login')
def Haltaseh_hasabat(request,pk):
    page_title = _('Aýdaky hasabatlar')
    tt=Other_users.objects.filter(wez="1")
    sh=Sehler.objects.filter(pr_seh_id=pk).first()

    pkk=sh.pk
    ayjem = Aydakyhalta_hasabat.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),abat=F('abathalta_sany'),brak=F('brakhalta_sany'),ganar=F('ganarhalta_sany')).values('month', 'gornus','olceg','abat','brak','ganar','id','gecenay_galyndy','satylan_halta_sany','wozwrat','ahyrky_galyndy_abat','ahyrky_galyndy_brak','ahyrky_galyndy_ganar','yerinde_bar_haryt','tapawudy').order_by("sene")
    
    # ayjem=Aydakyhalta_hasabat.objects.filter(sehs_id=pk).all()
    tikinci_sany=Gundelik_halta.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),).values('user__faa','month').distinct().annotate(abat=Sum(F('abathalta_sany')),brak=Sum(F('brakhalta_sany')),ganar=Sum(F('ganarhalta_sany'))).order_by("month")
    zak_sw=Zakaz_swotka.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),abat=F('abathalta_sany'),brak=F('brakhalta_sany'),ganar=F('ganarhalta_sany')).values('month', 'gornus','olceg','abat','brak','ganar','id','jemi_baha_m','jemi_baha_d','cyk_summa','cyk_summa_dol','gal_pey_summa','gal_pey_summa_dol','bellik').order_by("sene")

    paginator = Paginator(ayjem, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'tikinci_sany':tikinci_sany,'zak_sw':zak_sw,'pkk':pkk}
    return render(request, 'shu/haltaseh_hasabatlar.html', context)

@login_required(login_url='login')
def Ayjemi_update(request, pk):
    page_title = _('Ýerinde bar bolan harydy girizmek')

    if request.method == 'POST':
        form = AyjemUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            yerinde_bar_haryt = form.cleaned_data['yerinde_bar_haryt']
            bellik = form.cleaned_data['bellik']
            obj = Aydakyhalta_hasabat.objects.get(id=pk)
            obj.yerinde_bar_haryt=yerinde_bar_haryt
            if obj.abathalta_sany is not None:
                if obj.ahyrky_galyndy_abat == 0:
                    obj.tapawudy = 0
                else:
                    obj.tapawudy = obj.ahyrky_galyndy_abat-yerinde_bar_haryt
                obj.bellik=bellik
                obj.sene=timezone.now()
                obj.save()
            elif obj.brakhalta_sany is not None:
                if obj.ahyrky_galyndy_brak == 0:
                    obj.tapawudy = 0
                else:
                    obj.tapawudy = obj.ahyrky_galyndy_brak-yerinde_bar_haryt
                obj.bellik=bellik
                obj.sene=timezone.now()
                obj.save()
            elif obj.ganarhalta_sany is not None:
                if obj.ahyrky_galyndy_ganar == 0:
                    obj.tapawudy = 0
                else:
                    obj.tapawudy = obj.ahyrky_galyndy_ganar-yerinde_bar_haryt
                obj.bellik=bellik
                obj.sene=timezone.now()
                obj.save()
            messages.success(request, 'Aýdaky hasabata ýerinde bar bolan haryt girizildi!')
            return redirect('halta-seh-hasabat',obj.sehs.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: ýerinde bar bolan haryt girizilmedi')
    else:
        form = AyjemUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def ZakSwotka_update(request, pk):
    page_title = _('Çykdaýjylary girizmek')

    if request.method == 'POST':
        form = ZakSwotkaUpdateForm(request.POST, request.FILES)
        
        if form.is_valid():
            cyk_summa = form.cleaned_data['cyk_summa']
            cyk_summa_dol = form.cleaned_data['cyk_summa_dol']
            bellik = form.cleaned_data['bellik']
            obj = Zakaz_swotka.objects.get(id=pk)
            if cyk_summa is not None:
                obj.cyk_summa=cyk_summa
                obj.gal_pey_summa = obj.jemi_baha_m-cyk_summa
                obj.bellik=bellik
                obj.save()
            elif cyk_summa_dol is not None:
                obj.cyk_summa_dol=cyk_summa_dol
                obj.gal_pey_summa_dol=obj.jemi_baha_d-cyk_summa_dol
                obj.bellik=bellik
                obj.save()
            messages.success(request, 'Öndürilýän önüm üçin edilýän çykdaýjy girizildi!')
            return redirect('halta-seh-hasabat',obj.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Öndürilýän önüm üçin edilýän çykdaýjy girizilmedi')
    else:
        form = ZakSwotkaUpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def HaltaSeh_tabel(request):
    page_title = _('Halta seh aýlyk hasabaty (Tabel)')
    cur_user=request.user
    tabel=Halta_seh_ay_tabel.objects.all()

    if request.method == 'POST':
        form = HaltaSeh_TabelForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.cleaned_data['user']
            oklady = form.cleaned_data['oklady']
            ay_isguni = form.cleaned_data['ay_isguni']
            is_gun_sagady = form.cleaned_data['is_gun_sagady']
            is_gun_sany = form.cleaned_data['is_gun_sany']
            artyk_is_sagady = form.cleaned_data['artyk_is_sagady']
            awans = form.cleaned_data['awans']
            kart_sum = form.cleaned_data['kart_sum']
            bellik = form.cleaned_data['bellik']

            aww = awans if awans is not None else 0
            kartjyk=kart_sum if kart_sum is not None else 0

            gun_dus_hak=oklady/ay_isguni
            sag_dus_hak=gun_dus_hak/is_gun_sagady
            el_al_sum=((is_gun_sany*gun_dus_hak)+(sag_dus_hak*artyk_is_sagady)-aww)-kartjyk

            t_create=Halta_seh_ay_tabel.objects.create(user=user,oklady=oklady,ay_isguni=ay_isguni,
                                                       gune_dusyan_haky=gun_dus_hak,is_gun_sagady=is_gun_sagady,
                                                       sagat_dusyan_haky=sag_dus_hak,is_gun_sany=is_gun_sany,
                                                       artyk_is_sagady=artyk_is_sagady,awans=awans,
                                                       kart_sum=kart_sum,el_sum=el_al_sum,bellik=bellik)
            t_create.save()
            messages.success(request, 'Aýlyk zähmet hak hasabat (Tabel) girizildi!')
            return redirect('h-aylyk-tabel')
        else:
            messages.error(request, 'Ýalňyşlyk: Aýlyk zähmet hasabat (Tabel) girizilmedi!')
    else:
        form = HaltaSeh_TabelForm()
    
    
    paginator = Paginator(tabel, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form}
    return render(request, 'shu/haltaseh_tabel.html', context)

@login_required(login_url='login')
def Haltaseh_edit(request, pk):
    page_title = _('Halta sehde gündelik tikilýän haltany üýtgetmek')
    obj = Gundelik_halta.objects.get(id=pk)
    
    if request.method == 'POST':
        form = GunhaltaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Halta sehde gündelik tikilýän halta üýtgedildi!')
           return redirect('halta-seh',pk)
    else:
        form = GunhaltaForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Aydaky_halta_edit(request, pk):
    page_title = _('Gündelik tikilýän haltanyň hasabatyny üýtgetmek')
    obj = Aydaky_halta.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Aydaky_haltaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Gündelik tikilýän haltanyň hasabaty üýtgedildi!')
           return redirect('halta-seh',pk)
    else:
        form = Aydaky_haltaForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Aydakyhalta_hasabat_edit(request, pk):
    page_title = _('Aýdaky haltanyň hasabatyny üýtgetmek')
    obj = Aydakyhalta_hasabat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Aydakyhalta_hasabatForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Aýdaky haltanyň hasabaty üýtgedildi!')
           return redirect('halta-seh-hasabat',pk)
    else:
        form = Aydakyhalta_hasabatForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Halta_seh_ay_tabel_edit(request, pk):
    page_title = _('Halta sehde aýlyk zähmet hak hasabatyny (tabel) üýtgetmek')
    obj = Halta_seh_ay_tabel.objects.get(id=pk)
    
    if request.method == 'POST':
        form = HaltaSeh_TabelForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Halta sehde aýlyk zähmet hak hasabaty (tabel) üýtgedildi!')
           return redirect('h-aylyk-tabel')
    else:
        form = HaltaSeh_TabelForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Haltaseh_Skladjyk(request,pk):
    page_title = _('Halta sehdäki taýýar önümleriň hasabaty')
    sh=Sehler.objects.filter(pr_seh_id=pk).first()

    sap = Haltaseh_sklad.objects.filter(sehs_id=sh.pk).annotate(month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),abat=F('abathalta_sany'),brak=F('brakhalta_sany'),ganar=F('ganarhalta_sany')).values('month', 'gornus','olceg','abat','brak','ganar','id','gecenay_galyndy','satylan_halta_sany','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    pkk=sh.pk
    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'pkk':pkk}
    return render(request, 'shu/haltaseh_skladjyk.html', context)


# Dashboard
@login_required(login_url='login')
@group_required(['Admin','Baş hasapçy'])
def Dashboard(request):
    page_title = _('Dolandyryş paneli - Analitika')
    # Jemi algylar
    dok_jem_m=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cykrulon_bahasy_m")))['jemi']
    hal_jem_m=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("abathalta_bahasy_m")))['jemi']
    sap_jem_m=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cyksapak_bahasy_m")))['jemi']
    
    dok_jem_d=AydakyDokma_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cykrulon_bahasy_d")))['jemi']
    hal_jem_d=Aydakyhalta_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("abathalta_bahasy_d")))['jemi']
    sap_jem_d=AydakySapak_hasabat.objects.exclude(tapawudy=None).filter(zakaz_user=None).aggregate(jemi=Sum(F("tapawudy")) * Sum(F("cyksapak_bahasy_d")))['jemi']
    
    ay_pr_m_jem=Aylyk_premya.objects.filter(~Q(awans_m=None)).aggregate(jemi=Sum(F('jemi_m')))['jemi']
    ay_pr_d_jem=Aylyk_premya.objects.filter(~Q(awans_d=None)).aggregate(jemi=Sum(F('jemi_d')))['jemi']
    
    z_dok_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(algy=None).aggregate(jemi=Sum(F('algy')))['jemi']
    z_hal_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(algy=None).aggregate(jemi=Sum((F'algy')))['jemi']
    z_sap_al_jem=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(algy=None).aggregate(jemi=Sum(F('algy')))['jemi']

    zw_m=Das_isleyan_zawodlar.objects.aggregate(tap_m=Sum('tapawut_m'))['tap_m']
    zw_d=Das_isleyan_zawodlar.objects.aggregate(tap_d=Sum('tapawut_d'))['tap_d']
    
    a_karz_m=Das_karz_alynanpul.objects.aggregate(tap_m=Sum('jemi_m'))['tap_m']
    a_karz_d=Das_karz_alynanpul.objects.aggregate(tap_d=Sum('jemi_d'))['tap_d']
    
    gpz_m=Sklad_swotkalar.objects.aggregate(tap_m=Sum('galyndy_bahasy_m'))['tap_m']
    gpz_d=Sklad_swotkalar.objects.aggregate(tap_d=Sum('galyndy_bahasy_d'))['tap_d']
    
    bank_m=Bank.objects.filter(wal=1).aggregate(tap=Sum('galyndy'))['tap']
    bank_d=Bank.objects.filter(wal=2).aggregate(tap=Sum('galyndy'))['tap']
    
    a_algy_m=dok_jem_m if dok_jem_m is not None else 0
    b_algy_m=hal_jem_m if hal_jem_m is not None else 0
    c_algy_m=sap_jem_m if sap_jem_m is not None else 0
    d_algy_m=ay_pr_m_jem if ay_pr_m_jem is not None else 0
    g_algy=z_dok_al_jem if z_dok_al_jem is not None else 0
    t_algy=z_hal_al_jem if z_hal_al_jem is not None else 0
    j_algy=z_sap_al_jem if z_sap_al_jem is not None else 0
    p_algy_m=zw_m if zw_m is not None else 0
    s_algy_m=a_karz_m if a_karz_m is not None else 0
    k_algy_m=gpz_m if gpz_m is not None else 0
    w_algy_m=bank_m if bank_m is not None else 0

    a_algy_d=dok_jem_d if dok_jem_d is not None else 0
    b_algy_d=hal_jem_d if hal_jem_d is not None else 0
    c_algy_d=sap_jem_d if sap_jem_d is not None else 0
    d_algy_d=ay_pr_d_jem if ay_pr_d_jem is not None else 0
    p_algy_d=zw_d if zw_d is not None else 0
    s_algy_d=a_karz_d if a_karz_d is not None else 0
    k_algy_d=gpz_d if gpz_d is not None else 0
    w_algy_d=bank_d if bank_d is not None else 0


    ajem_m=sum(list(chain([a_algy_m,b_algy_m,c_algy_m,d_algy_m,g_algy,t_algy,j_algy,p_algy_m,s_algy_m,k_algy_m,w_algy_m])))
    ajem_d=sum(list(chain([a_algy_d,b_algy_d,c_algy_d,d_algy_d,p_algy_d,s_algy_d,k_algy_d,w_algy_d])))


    # Jemi bergiler
    beray_pr_m_jem=Aylyk_premya.objects.filter(~Q(awans_m=None)).aggregate(jemi=Sum(F('awans_m')))['jemi']
    beray_pr_d_jem=Aylyk_premya.objects.filter(~Q(awans_d=None)).aggregate(jemi=Sum(F('awans_d')))['jemi']
    z_dok_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=3).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']
    z_hal_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=2).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']
    z_sap_ber_jem=Zakaz_balans.objects.filter(seh__pr_seh=1).exclude(bergi=None).aggregate(jemi=Sum(F('bergi')))['jemi']

    a_bergi_m=beray_pr_m_jem if beray_pr_m_jem is not None else 0
    c_bergi=z_dok_ber_jem if z_dok_ber_jem is not None else 0
    d_bergi=z_hal_ber_jem if z_hal_ber_jem is not None else 0
    e_bergi=z_sap_ber_jem if z_sap_ber_jem is not None else 0
    
    a_bergi_d=beray_pr_d_jem if beray_pr_d_jem is not None else 0

    ajem_mtest=list(chain([a_algy_m,b_algy_m,c_algy_m,d_algy_m,g_algy,t_algy,j_algy,p_algy_m,s_algy_m,k_algy_m,w_algy_m]))
    ajem_dtest=list(chain([a_algy_d,b_algy_d,c_algy_d,d_algy_d,p_algy_d,s_algy_d,k_algy_d,w_algy_d]))

    fr_m=[]
    for x in ajem_mtest:
        if x < 0:
            fr_m.append(x)
    
    fr_d=[]
    for x in ajem_dtest:
        if x < 0:
            fr_m.append(x)

    bjem_m=sum(list(chain(fr_m,[a_bergi_m,c_bergi,d_bergi,e_bergi])))
    bjem_d=sum(list(chain(fr_d,[a_bergi_d])))


    # Jemi inwentar
    inwen_m=Inwentar.objects.aggregate(jemi=Sum(F('bahasy_m')))['jemi']
    inwen_d=Inwentar.objects.aggregate(jemi=Sum(F('bahasy_d')))['jemi']
    # print(inwen_m)

    # Jemi GPZ
    cig_m=World_cygmal.objects.aggregate(jemi=Sum(F('j_bahasy_m')))['jemi']
    cig_d=World_cygmal.objects.aggregate(jemi=Sum(F('j_bahasy_d')))['jemi']


    # Jemi bolek hasaplar
    bgal_d=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji_dollar')) - Sum(F('cykdajy_dollar')))['total']
    bgal_m=Bolek_hasaplar.objects.aggregate(total=Sum(F('girdeji')) - Sum(F('cykdajy')))['total']
    
    inw_m=inwen_m if inwen_m is not None else 0
    inw_d=inwen_d if inwen_d is not None else 0
    c_m=cig_m if cig_m is not None else 0
    c_d=cig_d if cig_d is not None else 0
    g_m=bgal_m if bgal_m is not None else 0
    g_d=bgal_d if bgal_d is not None else 0

    # Jemi sehler
    sapak_m=Sapakseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cyksapak_bahasy_m')))['jemi']
    sapak_d=Sapakseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cyksapak_bahasy_d')))['jemi']

    dokma_m=Dokmaseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cykrulon_bahasy_m')))['jemi']
    dokma_d=Dokmaseh_sklad.objects.aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('cykrulon_bahasy_d')))['jemi']

    halta_abat_m=Haltaseh_sklad.objects.filter(~Q(abathalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('abathalta_bahasy_m')))['jemi']
    halta_abat_d=Haltaseh_sklad.objects.filter(~Q(abathalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('abathalta_bahasy_d')))['jemi']

    halta_brak_m=Haltaseh_sklad.objects.filter(~Q(brakhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('brakhalta_bahasy_m')))['jemi']
    halta_brak_d=Haltaseh_sklad.objects.filter(~Q(brakhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('brakhalta_bahasy_d')))['jemi']
    
    halta_ganar_m=Haltaseh_sklad.objects.filter(~Q(ganarhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('ganarhalta_bahasy_m')))['jemi']
    halta_ganar_d=Haltaseh_sklad.objects.filter(~Q(ganarhalta_sany=None)).aggregate(jemi=Sum(F('ahyrky_galyndy')) * Sum(F('ganarhalta_bahasy_d')))['jemi']


    s_m=sapak_m if sapak_m is not None else 0
    d_m=dokma_m if dokma_m is not None else 0
    h_m=halta_abat_m if halta_abat_m is not None else 0
    hbrak_m=halta_brak_m if halta_brak_m is not None else 0
    hganar_m=halta_ganar_m if halta_ganar_m is not None else 0

    s_d=sapak_d if sapak_d is not None else 0
    d_d=dokma_d if dokma_d is not None else 0
    h_d=halta_abat_d if halta_abat_d is not None else 0
    hbrak_d=halta_brak_d if halta_brak_d is not None else 0
    hganar_d=halta_ganar_d if halta_ganar_d is not None else 0

    seh_jem_m = sum(list(chain([s_m,d_m,h_m,hbrak_m,hganar_m])))
    seh_jem_d = sum(list(chain([s_d,d_d,h_d,hbrak_d,hganar_d])))

    # Umumy jemleri Balansdaky
    jemleri_m=sum(list(chain([ajem_m,bjem_m, inw_m,c_m,g_m,seh_jem_m])))
    jemleri_d=sum(list(chain([ajem_d,bjem_d, inw_d,c_d,g_d,seh_jem_d])))

    bjem_mchart=list(chain(fr_m,[a_bergi_m,c_bergi,d_bergi,e_bergi]))

    sklad=Sklad_swotkalar.objects.all()
    # print(imp)

    
    # paginator = Paginator(gun, 5)
    # page = request.GET.get('page')
    # try:
    #     myuser = paginator.get_page(page)
    # except PageNotAnInteger:
    #     myuser = paginator.page(1)
    # except EmptyPage:
    #     myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'ajem_m':ajem_m,'ajem_d':ajem_d,
               'bjem_m':bjem_m,'bjem_d':bjem_d, 'inw_m':inw_m,'inw_d':inw_d,
               'c_m':c_m,'c_d':c_d, 'g_m':g_m,'g_d':g_d, 'seh_jem_m':seh_jem_m,'seh_jem_d':seh_jem_d,
               'jemleri_m':jemleri_m,'jemleri_d':jemleri_d,'ajem_mtest':ajem_mtest,'bjem_mchart':bjem_mchart,
               'sklad':sklad}
    return render(request, 'shu/dashboard.html', context)


# Offices
@login_required(login_url='login')
def OfficeSeh_sanaw(request):
    page_title = _('Sehleriň sanawy')
    cur_user=request.user

    seh = Sehler.objects.all()
    off_seh = Office.objects.all()
    off=Office.objects.all()

    if request.method == 'POST':
        form = InwentarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Täze inwentar girizildi!')
            return redirect('inwentar')
        else:
            messages.error(request, 'Ýalňyşlyk: inwentar girizilmedi!')
    else:
        form = InwentarForm()
    
    
    paginator = Paginator(off, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form,'off':off}
    return render(request, 'shu/office-seh.html', context)

@login_required(login_url='login')
def Seh_office(request):
    page_title = _('Sehleriň sanawy')
    cur_user=request.user
    primary_sehs=Primary_Seh.objects.all()

    if request.method == 'POST':
        form = InwentarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Täze inwentar girizildi!')
            return redirect('inwentar')
        else:
            messages.error(request, 'Ýalňyşlyk: inwentar girizilmedi!')
    else:
        form = InwentarForm()
    
    
    context = {'title': page_title,'form': form,'primary_sehs':primary_sehs}
    return render(request, 'shu/sehler.html', context)


# Dasyndan gelen cigmal (10 bolum)
@login_required(login_url='login')
def Cigmal_zawodlar(request):
    page_title = _('Satyn alynan we sklada gelen çigmallar')
    z_cig=World_cygmal.objects.all()
    s_cig=World_sklad.objects.all()
    swotka=Sklad_swotkalar.objects.all()

    if request.method == 'POST':
        form = Cigmal_zawodForm(request.POST, request.FILES)
        if form.is_valid():
            zawod = form.cleaned_data['zawod']
            kontrak_nomer = form.cleaned_data['kontrak_nomer']
            markasy = form.cleaned_data['markasy']
            tony = form.cleaned_data['tony']
            bahasy_m = form.cleaned_data['bahasy_m']
            bahasy_d = form.cleaned_data['bahasy_d']
            paddon_kg = form.cleaned_data['paddon_kg']
            bigbag_kg = form.cleaned_data['bigbag_kg']
            bellik = form.cleaned_data['bellik']

            cigmal_create=World_cygmal.objects.create(zawod=zawod,kontrak_nomer=kontrak_nomer,
                                                            markasy=markasy,tony=tony,bahasy_m=bahasy_m,
                                                            bahasy_d=bahasy_d,paddon_kg=paddon_kg,bigbag_kg=bigbag_kg,bellik=bellik,
                                                            j_bahasy_m=tony*bahasy_m if bahasy_m is not None else 0.0,
                                                            j_bahasy_d=tony*bahasy_d if bahasy_d is not None else 0.0)
            cigmal_create.save()
            messages.success(request, 'Täze satyn alynan çigmal girizildi!')
            return redirect('cigmal-zawotdan')
        else:
            messages.error(request, 'Ýalňyşlyk: satyn alynan çigmal girizilmedi')
    else:
        form = Cigmal_zawodForm()

    paginator = Paginator(z_cig, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'s_cig':s_cig,'form':form,'swotka':swotka}
    return render(request, 'shu/dasyndan_alnan_cigmal.html', context)

@login_required(login_url='login')
def Cigmal_sendSklad(request,pk):
    page_title = _('Satyn alynan çigmaly sehe geçirmek')
    z_cig=World_cygmal.objects.all()

    if request.method == 'POST':
        form = Zawod_gelen_cigmalForm(request.POST, request.FILES)
        if form.is_valid():
            kime_dusdi = form.cleaned_data['kime_dusdi']
            bellik = form.cleaned_data['bellik']
            tony = form.cleaned_data['tony']
            
            for x in z_cig:
                if x.pk == pk:

                    s_cig_create=World_sklad.objects.create(kime_dusdi=kime_dusdi,zawod=x.zawod,kontrak_nomer=x.kontrak_nomer,
                                                            markasy=x.markasy,tony=tony,bahasy_m=x.bahasy_m,
                                                            bahasy_d=x.bahasy_d,paddon_kg=x.paddon_kg,bigbag_kg=x.bigbag_kg,bellik=bellik,
                                                            j_bahasy_m=tony*x.bahasy_m if x.bahasy_m is not None else 0.0,
                                                            j_bahasy_d=tony*x.bahasy_d if x.bahasy_d is not None else 0.0)
                    s_cig_create.save()
                    cig_swotka=Sklad_swotkalar.objects.create(kimden=x.zawod,kime=kime_dusdi,kontrak_nomer=x.kontrak_nomer,
                                                              markasy=x.markasy,gelen_tony=x.tony,giden_tony=tony,
                                                              bahasy_m=x.bahasy_m,bahasy_d=x.bahasy_d,paddon_kg=x.paddon_kg,bigbag_kg=x.bigbag_kg,
                                                              j_bahasy_m=x.tony*x.bahasy_m if x.bahasy_m is not None else 0.0,
                                                              j_bahasy_d=x.tony*x.bahasy_d if x.bahasy_d is not None else 0.0,
                                                              j_gel_bah_m=tony*x.bahasy_m if x.bahasy_m is not None else 0.0,
                                                              j_gel_bah_d=tony*x.bahasy_d if x.bahasy_d is not None else 0.0,
                                                              galyndy_bahasy_m=(x.tony*x.bahasy_m if x.bahasy_m is not None else 0.0)-(tony*x.bahasy_m if x.bahasy_m is not None else 0.0),
                                                              galyndy_bahasy_d=(x.tony*x.bahasy_d if x.bahasy_d is not None else 0.0)-(tony*x.bahasy_d if x.bahasy_d is not None else 0.0),
                                                              galyndy_tony=x.tony-tony,gel_sene=x.sene)
                    cig_swotka.save()
            messages.success(request, 'Satyn alynan çigmal sehe geçirildi!')
            return redirect('cigmal-zawotdan')
        else:
            messages.error(request, 'Ýalňyşlyk: Satyn alynan çigmal sehe geçirildi')
    else:
        form = Zawod_gelen_cigmalForm()

    context = {'title': page_title,'form':form}
    return render(request, 'shu/cigmal_send.html', context)

@login_required(login_url='login')
def World_cygmal_edit(request, pk):
    page_title = _('Zawotdan satyn alynan çigmaly üýtgetmek')
    obj = World_cygmal.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Cigmal_zawod_editForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Zawotdan satyn alynan çigmaly üýtgedildi!')
           return redirect('cigmal-zawotdan')
    else:
        form = Cigmal_zawod_editForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def World_sklad_edit(request, pk):
    page_title = _('Daşyndan sklada gelen çigmaly üýtgetmek')
    obj = World_sklad.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Cigmal_skladForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşyndan sklada gelen çigmaly üýtgedildi!')
           return redirect('cigmal-zawotdan')
    else:
        form = Cigmal_skladForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


# SKLAD
@login_required(login_url='login')
def Sklad(request):
    page_title = _('Sklada alynan we sklada gelen çigmallar')
    gel_sklad=Gelen_sklat.objects.all()
    ay_has=AydakySklad_hasabat.objects.all()
    seneid1=Hasabat_sene.objects.last().id

    jemler=AydakySklad_hasabat.objects.aggregate(san_m=Sum(F('ahyrky_galyndy_sany')) * Sum(F('oz_bahasy_m')),san_d=Sum(F('ahyrky_galyndy_sany')) * Sum(F('oz_bahasy_d')),
                                                 kg_m=Sum(F('ahyrky_galyndy_kg')) * Sum(F('oz_bahasy_m')),kg_d=Sum(F('ahyrky_galyndy_kg')) * Sum(F('oz_bahasy_d')))
    if request.method == 'POST':
        form = GelenHaryt_skladForm(request.POST, request.FILES)
        if form.is_valid():
            harydyn_ady=form.cleaned_data['harydyn_ady']
            nirden_gelen=form.cleaned_data['nirden_gelen']
            modeli=form.cleaned_data['modeli']
            sany=form.cleaned_data['sany']
            haryt_kg=form.cleaned_data['haryt_kg']
            oz_bahasy_m=form.cleaned_data['oz_bahasy_m']
            oz_bahasy_dol=form.cleaned_data['oz_bahasy_dol']
            satlyk_bahasy_m=form.cleaned_data['satlyk_bahasy_m']
            satlyk_bahasy_dol=form.cleaned_data['satlyk_bahasy_dol']
            bellik=form.cleaned_data['bellik']
            
            if sany is not None:
                gel_create=Gelen_sklat.objects.create(has_sene=seneid1,harydyn_ady=harydyn_ady,modeli=modeli,
                                                      nirden_gelen=nirden_gelen,sany=sany,
                                                      oz_bahasy_m=oz_bahasy_m,oz_bahasy_dol=oz_bahasy_dol,
                                                      satlyk_bahasy_m=satlyk_bahasy_m,
                                                      satlyk_bahasy_dol=satlyk_bahasy_dol,bellik=bellik,
                                                      jemi_bahasy_m=sany*oz_bahasy_m if oz_bahasy_m is not None else 0,
                                                      jemi_bahasy_d=sany*oz_bahasy_dol if oz_bahasy_dol is not None else 0)
                gel_create.save()
            elif haryt_kg is not None:
                gel_create=Gelen_sklat.objects.create(has_sene=seneid1,harydyn_ady=harydyn_ady,modeli=modeli,
                                                      nirden_gelen=nirden_gelen,haryt_kg=haryt_kg,
                                                      oz_bahasy_m=oz_bahasy_m,oz_bahasy_dol=oz_bahasy_dol,
                                                      satlyk_bahasy_m=satlyk_bahasy_m,
                                                      satlyk_bahasy_dol=satlyk_bahasy_dol,bellik=bellik,
                                                      jemi_bahasy_m=haryt_kg*oz_bahasy_m if oz_bahasy_m is not None else 0,
                                                      jemi_bahasy_d=haryt_kg*oz_bahasy_dol if oz_bahasy_dol is not None else 0)
                gel_create.save()

            messages.success(request, 'Sklada täze gelen haryt girizildi!')
            return redirect('sklad')
        else:
            messages.error(request, 'Ýalňyşlyk: Skladan giden haryt girizilmedi')
    else:
        form = GelenHaryt_skladForm()

    paginator = Paginator(gel_sklad, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form':form,'ay_has':ay_has,'jemler':jemler}
    return render(request, 'shu/sklad.html', context)

@login_required(login_url='login')
def Sklad_update(request, pk):
    page_title = _('Sklatdan giden harytlary girizmek')

    seneid1=Hasabat_sene.objects.last().id
    if request.method == 'POST':
        form = GidenHaryt_skladForm(request.POST, request.FILES)
        if form.is_valid():
            nira_gitdi=form.cleaned_data['nira_gitdi']
            g_sany=form.cleaned_data['g_sany']
            g_haryt_kg=form.cleaned_data['g_haryt_kg']
            g_bellik = form.cleaned_data['g_bellik']

            obj = Gelen_sklat.objects.get(id=pk)
            if g_sany is not None:
                obj.nira_gitdi=nira_gitdi
                obj.g_sany=g_sany
                obj.g_jemi_bahasy_m=g_sany * obj.oz_bahasy_m if obj.oz_bahasy_m is not None else 0
                obj.g_jemi_bahasy_d=g_sany * obj.oz_bahasy_dol if obj.oz_bahasy_dol is not None else 0
                obj.g_bellik=g_bellik
                obj.g_sene=timezone.now()
                obj.save()
            elif g_haryt_kg is not None:
                obj.nira_gitdi=nira_gitdi
                obj.g_haryt_kg=g_haryt_kg
                obj.g_jemi_bahasy_m=g_haryt_kg * obj.oz_bahasy_m if obj.oz_bahasy_m is not None else 0
                obj.g_jemi_bahasy_d=g_haryt_kg * obj.oz_bahasy_dol if obj.oz_bahasy_dol is not None else 0
                obj.g_bellik=g_bellik
                obj.g_sene=timezone.now()
                obj.save()
            
            sklad_sw=AydakySklad_hasabat.objects.all().count()
            sk_sw=AydakySklad_hasabat.objects.all()

            seneid2=list(Hasabat_sene.objects.all())[-2].id
            ay2=AydakySklad_hasabat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).count()
            ay3=AydakySklad_hasabat.objects.all()

            sany_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('sany')))['total']
            gsany_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('g_sany')))['total']
            kg_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('haryt_kg')))['total']
            gkg_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('g_haryt_kg')))['total']
            bah_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('jemi_bahasy_m')))['total']
            bah_jd=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('jemi_bahasy_d')))['total']
            gbah_j=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('g_jemi_bahasy_m')))['total']
            gbah_jd=Gelen_sklat.objects.filter(has_sene=seneid1,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('g_jemi_bahasy_d')))['total']
            
            ahg_j_s=AydakySklad_hasabat.objects.filter(has_sene=seneid2,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('ahyrky_galyndy_sany')))['total']
            ahg_j_k=AydakySklad_hasabat.objects.filter(has_sene=seneid2,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('ahyrky_galyndy_kg')))['total']
            ahg_j_m=AydakySklad_hasabat.objects.filter(has_sene=seneid2,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('gecenay_galyndy_m')))['total']
            ahg_j_d=AydakySklad_hasabat.objects.filter(has_sene=seneid2,harydyn_ady=obj.harydyn_ady,modeli=obj.modeli).aggregate(total=Sum(F('gecenay_galyndy_d')))['total']

            # Aydaky hasabat insert we update
            if ay2 == 0:
                cur_ay_create = AydakySklad_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1),
                                                                    ~Q(harydyn_ady=obj.harydyn_ady),
                                                                    ~Q(modeli=obj.modeli)).create(has_sene=seneid1,
                                                                                              harydyn_ady=obj.harydyn_ady,oz_bahasy_m=obj.oz_bahasy_m,oz_bahasy_d=obj.oz_bahasy_dol,
                                                                                              modeli=obj.modeli,jemi_sany=sany_j if sany_j is not None else 0,haryt_kg=kg_j if kg_j is not None else 0,
                                                                                              gecenay_galyndy_sany=ahg_j_s if ahg_j_s is not None else 0,gecenay_galyndy_kg=ahg_j_k if ahg_j_k is not None else 0,
                                                                                              gecenay_galyndy_m=ahg_j_m if ahg_j_m is not None else 0,
                                                                                              gecenay_galyndy_d=ahg_j_d if ahg_j_d is not None else 0,jemi_gelen_m=bah_j if bah_j is not None else 0,
                                                                                              jemi_giden_m=gbah_j if gbah_j is not None else 0,jemi_gelen_d=bah_jd if bah_jd is not None else 0,
                                                                                              jemi_giden_d=gbah_jd if gbah_jd is not None else 0,
                                                                                              ahyrky_galyndy_sany=sany_j - gsany_j if gsany_j is not None else 0,
                                                                                              ahyrky_galyndy_kg=kg_j - gkg_j if gkg_j is not None else 0,
                                                                                              ahyrky_galyndy_m=bah_j - gbah_j if gbah_j is not None else 0, 
                                                                                              ahyrky_galyndy_d=bah_jd - gbah_jd if gbah_jd is not None else 0)
                cur_ay_create.save()
            for x in ay3:
                if ay2 > 0 and x.has_sene is not seneid1 and x.harydyn_ady is not obj.harydyn_ady and x.modeli is not obj.modeli:
                    cur_ay_create = AydakySklad_hasabat.objects.filter(Q(has_sene=None) | ~Q(has_sene=seneid1),
                                                                        ~Q(harydyn_ady=obj.harydyn_ady),
                                                                        ~Q(modeli=obj.modeli)).create(has_sene=seneid1,
                                                                                              harydyn_ady=obj.harydyn_ady,oz_bahasy_m=obj.oz_bahasy_m,oz_bahasy_d=obj.oz_bahasy_dol,
                                                                                              modeli=obj.modeli,jemi_sany=sany_j if sany_j is not None else 0,haryt_kg=kg_j if kg_j is not None else 0,
                                                                                              gecenay_galyndy_sany=ahg_j_s if ahg_j_s is not None else 0,gecenay_galyndy_kg=ahg_j_k if ahg_j_k is not None else 0,
                                                                                              gecenay_galyndy_m=ahg_j_m if ahg_j_m is not None else 0,
                                                                                              gecenay_galyndy_d=ahg_j_d if ahg_j_d is not None else 0,jemi_gelen_m=bah_j if bah_j is not None else 0,
                                                                                              jemi_giden_m=gbah_j if gbah_j is not None else 0,jemi_gelen_d=bah_jd if bah_jd is not None else 0,
                                                                                              jemi_giden_d=gbah_jd if gbah_jd is not None else 0,
                                                                                              ahyrky_galyndy_sany=sany_j - gsany_j if gsany_j is not None else 0,
                                                                                              ahyrky_galyndy_kg=kg_j - gkg_j if gkg_j is not None else 0,
                                                                                              ahyrky_galyndy_m=bah_j - gbah_j if gbah_j is not None else 0, 
                                                                                              ahyrky_galyndy_d=bah_jd - gbah_jd if gbah_jd is not None else 0)
                    cur_ay_create.save()
                else:
                    ay_update = AydakySklad_hasabat.objects.filter(has_sene=seneid1,
                                                                   harydyn_ady=obj.harydyn_ady,
                                                                   modeli=obj.modeli).update(has_sene=seneid1,
                                                                                              harydyn_ady=obj.harydyn_ady,oz_bahasy_m=obj.oz_bahasy_m,oz_bahasy_d=obj.oz_bahasy_dol,
                                                                                              modeli=obj.modeli,jemi_sany=sany_j if sany_j is not None else 0,haryt_kg=kg_j if kg_j is not None else 0,
                                                                                              gecenay_galyndy_sany=ahg_j_s if ahg_j_s is not None else 0,gecenay_galyndy_kg=ahg_j_k if ahg_j_k is not None else 0,
                                                                                              gecenay_galyndy_m=ahg_j_m if ahg_j_m is not None else 0,
                                                                                              gecenay_galyndy_d=ahg_j_d if ahg_j_d is not None else 0,jemi_gelen_m=bah_j if bah_j is not None else 0,
                                                                                              jemi_giden_m=gbah_j if gbah_j is not None else 0,jemi_gelen_d=bah_jd if bah_jd is not None else 0,
                                                                                              jemi_giden_d=gbah_jd if gbah_jd is not None else 0,
                                                                                              ahyrky_galyndy_sany=sany_j - gsany_j if gsany_j is not None else 0,
                                                                                              ahyrky_galyndy_kg=kg_j - gkg_j if gkg_j is not None else 0,
                                                                                              ahyrky_galyndy_m=bah_j - gbah_j if gbah_j is not None else 0, 
                                                                                              ahyrky_galyndy_d=bah_jd - gbah_jd if gbah_jd is not None else 0)
                
            messages.success(request, 'Aýdaky hasabata ýerinde bar bolan haryt girizildi!')
            return redirect('sklad')
        else:
            messages.error(request, 'Ýalňyşlyk: ýerinde bar bolan haryt girizilmedi')
    else:
        form = GidenHaryt_skladForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def AyjemiSklad_update(request, pk):
    page_title = _('Ýerinde bar bolan harydy girizmek')

    if request.method == 'POST':
        form = Ayjem_Sklad_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            yerinde_bar_haryt_sany = form.cleaned_data['yerinde_bar_haryt_sany']
            yerinde_bar_haryt_kg = form.cleaned_data['yerinde_bar_haryt_kg']
            wozwrat_sany = form.cleaned_data['wozwrat_sany']
            wozwrat_kg = form.cleaned_data['wozwrat_kg']
            bellik = form.cleaned_data['bellik']
            obj = AydakySklad_hasabat.objects.get(id=pk)
            if yerinde_bar_haryt_sany is not None:
                obj.yerinde_bar_haryt_sany=yerinde_bar_haryt_sany
                obj.wozwrat_sany=wozwrat_sany
                if wozwrat_sany == None:
                    tap=obj.ahyrky_galyndy_sany - yerinde_bar_haryt_sany
                    obj.tapawudy_sany = tap
                else:
                    tap=obj.ahyrky_galyndy_sany - yerinde_bar_haryt_sany
                    obj.tapawudy_sany = tap - wozwrat_sany
                obj.bellik=bellik
                obj.save()
            elif yerinde_bar_haryt_kg is not None:
                obj.yerinde_bar_haryt_kg=yerinde_bar_haryt_kg
                obj.wozwrat_kg=wozwrat_kg
                if wozwrat_kg == None:
                    tap=obj.ahyrky_galyndy_kg - yerinde_bar_haryt_kg
                    obj.tapawudy_kg = tap
                else:
                    tap=obj.ahyrky_galyndy_kg - yerinde_bar_haryt_kg
                    obj.tapawudy_kg = tap - wozwrat_kg
                obj.bellik=bellik
                obj.save()
            messages.success(request, 'Aýdaky hasabata ýerinde bar bolan haryt girizildi!')
            return redirect('sklad')
        else:
            messages.error(request, 'Ýalňyşlyk: ýerinde bar bolan haryt girizilmedi')
    else:
        form = Ayjem_Sklad_UpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sklad_sapakseh(request):
    page_title = _('Sapak sehdäki taýýar önümleriň hasabaty')
    cur_user=request.user
    sap = Sapakseh_sklad.objects.annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_sapak')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_sapak_kg','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    satylan = Sapakseh_sklad_satylan.objects.all().order_by("sene")

    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'satylan':satylan}
    return render(request, 'shu/sklad_sapakseh.html', context)

@login_required(login_url='login')
def Sklad_sapakseh_update(request, pk):
    page_title = _('Sapak sehdäki taýýar önümleri satmak')
    if request.method == 'POST':
        form = Sklad_sapakseh_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            zakaz_user = form.cleaned_data['zakaz_user']
            satylan_sapak_kg = form.cleaned_data['satylan_sapak_kg']
            bellik = form.cleaned_data['bellik']
            seneid1=Hasabat_sene.objects.last().id
            obj = Sapakseh_sklad.objects.get(id=pk)

            if zakaz_user is not None:
                zcode=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
                cur_code = []
                for deg in zcode:
                    c=deg.haryt_code
                    cur_code.append({'c':c})

                for deg in zcode:
                    rb1=deg.algy-satylan_sapak_kg*deg.bahasy
                    if deg.algy != 0:
                        s=deg.algy/deg.bahasy
                        if s >= satylan_sapak_kg:
                            sat_create=Sapakseh_sklad_satylan.objects.create(zakaz_user=zakaz_user,zakaz_code=c,gel_sklad_id=pk,sehs_id=obj.sehs.pk,
                                                                             d_gornusi=obj.d_gornusi,jemi_dok_sapak=obj.jemi_dok_sapak,
                                                                             satylan_sapak_kg=satylan_sapak_kg,bellik=bellik,has_sene=seneid1)
                            sat_create.save()

                            up=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code'])).update(algy = rb1)

                            obj.satylan_sapak_kg = satylan_sapak_kg
                            obj.ahyrky_galyndy = obj.ahyrky_galyndy - satylan_sapak_kg
                            obj.save()
                    break
            else:
                sat_create=Sapakseh_sklad_satylan.objects.create(gel_sklad_id=pk,sehs_id=obj.sehs.pk,d_gornusi=obj.d_gornusi,
                                                                 jemi_dok_sapak=obj.jemi_dok_sapak,satylan_sapak_kg=satylan_sapak_kg,
                                                                 bellik=bellik,has_sene=seneid1)
                sat_create.save()
                obj.satylan_sapak_kg = satylan_sapak_kg
                obj.ahyrky_galyndy = obj.ahyrky_galyndy - satylan_sapak_kg
                obj.save()
            messages.success(request, 'Satylan haryt girizildi!')
            return redirect('sklad-sapak-seh')
        else:
            messages.error(request, 'Ýalňyşlyk: satylan haryt girizilmedi')
    else:
        form = Sklad_sapakseh_UpdateForm()

    context = {'title':page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sklad_dokmaseh(request):
    page_title = _('Dokma sehdäki taýýar önümleriň hasabaty')
    cur_user=request.user
    sap = Dokmaseh_sklad.objects.annotate(month=TruncMonth('sene'),gornus=F('d_gornusi__name'),onum=F('jemi_dok_rulon')).values('month', 'gornus','onum','id','gecenay_galyndy','satylan_dokma_kg','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    satylan = Dokmaseh_sklad_satylan.objects.all().order_by("sene")

    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'satylan':satylan}
    return render(request, 'shu/sklad_dokmaseh.html', context)

@login_required(login_url='login')
def Sklad_dokmaseh_update(request, pk):
    page_title = _('Dokma sehdäki taýýar önümleri satmak')
    if request.method == 'POST':
        form = Sklad_dokmaseh_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            zakaz_user = form.cleaned_data['zakaz_user']
            satylan_dokma_kg = form.cleaned_data['satylan_dokma_kg']
            bellik = form.cleaned_data['bellik']
            seneid1=Hasabat_sene.objects.last().id
            obj = Dokmaseh_sklad.objects.get(id=pk)

            if zakaz_user is not None:
                zcode=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
                cur_code = []
                for deg in zcode:
                    c=deg.haryt_code
                    cur_code.append({'c':c})

                for deg in zcode:
                    rb1=deg.algy-satylan_dokma_kg*deg.bahasy
                    if deg.algy != 0:
                        s=deg.algy/deg.bahasy
                        if s >= satylan_dokma_kg:
                            sat_create=Dokmaseh_sklad_satylan.objects.create(zakaz_user=zakaz_user,zakaz_code=c,gel_sklad_id=pk,sehs_id=obj.sehs.pk,
                                                                             d_gornusi=obj.d_gornusi,jemi_dok_rulon=obj.jemi_dok_rulon,
                                                                             satylan_dokma_kg=satylan_dokma_kg,bellik=bellik,has_sene=seneid1)
                            sat_create.save()

                            up=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code'])).update(algy = rb1)

                            obj.satylan_dokma_kg = satylan_dokma_kg
                            obj.ahyrky_galyndy = obj.ahyrky_galyndy - satylan_dokma_kg
                            obj.save()
                    break
            else:
                sat_create=Dokmaseh_sklad_satylan.objects.create(gel_sklad_id=pk,sehs_id=obj.sehs.pk,d_gornusi=obj.d_gornusi,
                                                                 jemi_dok_rulon=obj.jemi_dok_rulon,satylan_dokma_kg=satylan_dokma_kg,
                                                                 bellik=bellik,has_sene=seneid1)
                sat_create.save()
                obj.satylan_dokma_kg = satylan_dokma_kg
                obj.ahyrky_galyndy = obj.ahyrky_galyndy - satylan_dokma_kg
                obj.save()

            messages.success(request, 'Satylan haryt girizildi!')
            return redirect('sklad-dokma-seh')
        else:
            messages.error(request, 'Ýalňyşlyk: satylan haryt girizilmedi')
    else:
        form = Sklad_dokmaseh_UpdateForm()

    context = {'title':page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sklad_haltaseh(request):
    page_title = _('Halta sehdäki taýýar önümleriň hasabaty')
    cur_user=request.user
    sap = Haltaseh_sklad.objects.annotate(month=TruncMonth('sene'),gornus=F('h_gornusi__name'),olceg=F('h_olceg'),abat=F('abathalta_sany'),brak=F('brakhalta_sany'),ganar=F('ganarhalta_sany')).values('month', 'gornus','olceg','abat','brak','ganar','id','gecenay_galyndy','satylan_halta_sany','wozwrat','ahyrky_galyndy','bellik').order_by("sene")
    satylan = Haltaseh_sklad_satylan.objects.all().order_by("sene")

    paginator = Paginator(sap, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'satylan':satylan}
    return render(request, 'shu/sklad_haltaseh.html', context)

@login_required(login_url='login')
def Sklad_haltaseh_update(request, pk):
    page_title = _('Halta sehdäki taýýar önümleri satmak')
    if request.method == 'POST':
        form = Sklad_haltaseh_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            zakaz_user = form.cleaned_data['zakaz_user']
            satylan_halta_sany = form.cleaned_data['satylan_halta_sany']
            bellik = form.cleaned_data['bellik']
            obj = Haltaseh_sklad.objects.get(id=pk)
            seneid1=Hasabat_sene.objects.last().id
            
            if zakaz_user is not None:
                zcode=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code']))
                cur_code = []
                for deg in zcode:
                    c=deg.haryt_code
                    cur_code.append({'c':c})

                for deg in zcode:
                    rb1=deg.algy-satylan_halta_sany*deg.bahasy
                    if deg.algy != 0:
                        s=deg.algy/deg.bahasy
                        if s >= satylan_halta_sany:
                            sat_create=Haltaseh_sklad_satylan.objects.create(zakaz_user=zakaz_user,zakaz_code=c,gel_sklad_id=pk,sehs_id=obj.sehs.pk,
                                                                             h_gornusi=obj.h_gornusi,h_olceg=obj.h_olceg,has_sene=seneid1,
                                                                             abathalta_sany=obj.abathalta_sany,brakhalta_sany=obj.brakhalta_sany,
                                                                             ganarhalta_sany=obj.ganarhalta_sany,satylan_halta_sany=satylan_halta_sany,
                                                                             bellik=bellik)
                            sat_create.save()

                            up=Zakaz_balans.objects.filter(id=(request.POST['zakaz_code'])).update(algy = rb1)

                            obj.satylan_halta_sany=satylan_halta_sany
                            obj.ahyrky_galyndy=obj.ahyrky_galyndy-satylan_halta_sany
                            obj.save()
                    break
            else:
                sat_create=Haltaseh_sklad_satylan.objects.create(gel_sklad_id=pk,sehs_id=obj.sehs.pk,
                                                                 h_gornusi=obj.h_gornusi,h_olceg=obj.h_olceg,has_sene=seneid1,
                                                                 abathalta_sany=obj.abathalta_sany,brakhalta_sany=obj.brakhalta_sany,
                                                                 ganarhalta_sany=obj.ganarhalta_sany,satylan_halta_sany=satylan_halta_sany,
                                                                 bellik=bellik)
                sat_create.save()
                obj.satylan_halta_sany=satylan_halta_sany
                obj.ahyrky_galyndy=obj.ahyrky_galyndy-satylan_halta_sany
                obj.save()
            messages.success(request, 'Satylan haryt girizildi!')
            return redirect('sklad-halta-seh')
        else:
            messages.error(request, 'Ýalňyşlyk: satylan haryt girizilmedi')
    else:
        form = Sklad_haltaseh_UpdateForm()

    context = {'title':page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sklad_das_zawod(request):
    page_title = _('Daşyndan işleşilýän zawotdaki taýýar önümleriň hasabaty')
    zaw=Das_isleyan_zawodlar.objects.all().order_by("sene")
    alynan = Das_is_zawod_Alynan.objects.all().order_by("sene")
    paginator = Paginator(zaw, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'alynan':alynan}
    return render(request, 'shu/sklad_daszawod.html', context)

@login_required(login_url='login')
def Sklad_daszawod_update(request, pk):
    page_title = _('Daşyndan işleşilýän zawotdaki taýýar önümleri satmak')
    if request.method == 'POST':
        form = Sklad_daszawod_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            satylan_haryt_sany = form.cleaned_data['satylan_haryt_sany']
            satylan_haryt_kg = form.cleaned_data['satylan_haryt_kg']
            obj = Das_isleyan_zawodlar.objects.get(id=pk)
            if satylan_haryt_sany is not None:
                obj.satylan_haryt_sany = satylan_haryt_sany
                obj.t_haryt_sany = obj.t_haryt_sany - satylan_haryt_sany
                obj.save()
            elif satylan_haryt_kg is not None:
                obj.satylan_haryt_kg = satylan_haryt_kg
                obj.t_haryt_kg = obj.t_haryt_kg - satylan_haryt_kg
                obj.save()
            messages.success(request, 'Satylan haryt girizildi!')
            return redirect('sklad-das-zawod')
        else:
            messages.error(request, 'Ýalňyşlyk: satylan haryt girizilmedi')
    else:
        form = Sklad_daszawod_UpdateForm()

    context = {'title':page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Gelen_sklat_edit(request, pk):
    page_title = _('Sklada gelen harydy üýtgetmek')
    obj = Gelen_sklat.objects.get(id=pk)
    
    if request.method == 'POST':
        form = GelenHaryt_skladForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklada gelen haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = GelenHaryt_skladForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sapakseh_sklad_edit(request, pk):
    page_title = _('Sklada gelen harydy üýtgetmek')
    obj = Sapakseh_sklad.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Sapakseh_skladForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklada gelen haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Sapakseh_skladForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Sapakseh_sklad_satylan_edit(request, pk):
    page_title = _('Sklatdan satylan harydy üýtgetmek')
    obj = Sapakseh_sklad_satylan.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Sapakseh_sklad_satylanForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklatdan satyan haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Sapakseh_sklad_satylanForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Dokmaseh_sklad_edit(request, pk):
    page_title = _('Sklada gelen harydy üýtgetmek')
    obj = Dokmaseh_sklad.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Dokmaseh_skladForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklada gelen haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Dokmaseh_skladForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Dokmaseh_sklad_satylan_edit(request, pk):
    page_title = _('Sklatdan satylan harydy üýtgetmek')
    obj = Dokmaseh_sklad_satylan.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Dokmaseh_sklad_satylanForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklatdan satyan haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Dokmaseh_sklad_satylanForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Haltaseh_sklad_edit(request, pk):
    page_title = _('Sklada gelen harydy üýtgetmek')
    obj = Haltaseh_sklad.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Haltaseh_skladForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklada gelen haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Haltaseh_skladForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Haltaseh_sklad_satylan_edit(request, pk):
    page_title = _('Sklatdan satylan harydy üýtgetmek')
    obj = Haltaseh_sklad_satylan.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Haltaseh_sklad_satylanForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Sklatdan satyan haryt üýtgedildi!')
           return redirect('sklad')
    else:
        form = Haltaseh_sklad_satylanForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)




@login_required(login_url='login')
def All_sehs(request,pk):
    page_title = _('Sehler')
    sub_s=Sehler.objects.filter(pr_seh=pk)
    pkk=pk

    if request.method == 'POST':
        form = SehlerForm(request.POST, request.FILES)
        if form.is_valid():
            office=form.cleaned_data['office']
            name=form.cleaned_data['name']
            tel=form.cleaned_data['tel']
            address=form.cleaned_data['address']
            obj=Sehler.objects.create(pr_seh=pk,office=office,name=name,tel=tel,address=address)
            obj.save()
            messages.success(request, 'Täze Sapak seh girizildi!')
            return redirect('sub-seh-sapak')
        else:
            messages.error(request, 'Ýalňyşlyk: Sapak seh girizilmedi!')
    else:
        form = SehlerForm()
    
    
    paginator = Paginator(sub_s, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form,'pkk':pkk}
    return render(request, 'shu/all_sehs_name.html', context)

@login_required(login_url='login')
def Yollonma(request,pk):
    page_title = _('Giren sehiňize intek maglumat girizilmedik! Öz sehiňizi saýlap giriň!')
    nol=Gundelik_sapak.objects.filter(sehs_id=pk)
    bir=Gundelik_dokma.objects.filter(sehs_id=pk)
    iki=Gundelik_halta.objects.filter(sehs_id=pk)
    pkk=pk

    if nol:
        return redirect('sapak-seh', pk)
    elif bir:
        return redirect('dokma-seh', pk)
    elif iki:
        return redirect('halta-seh', pk)
    
    context = {'title': page_title,'pkk':pkk}
    return render(request, 'shu/yolla.html', context)


# Daşyndan işleşilýän zawodlar
@login_required(login_url='login')
def Das_Zawodlar(request):
    page_title = _('Daşyndan işleşilýän zawodlar')
    zaw=Das_zawod.objects.all()

    if request.method == 'POST':
        form = Das_ZawodForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Täze daşyndan işleşilýän zawod girizildi!')
            return redirect('das-zawod')
        else:
            messages.error(request, 'Ýalňyşlyk: Daşyndan işleşilýän zawod girizilmedi!')
    else:
        form = Das_ZawodForm()
    
    paginator = Paginator(zaw, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser, 'form': form}
    return render(request, 'shu/das_zawod.html', context)

@login_required(login_url='login')
def Zawod_detail(request, pk):
    page_title = _('Daşyndan işleşilýän zawoda berilen alynan harytlar')
    zaw = Das_isleyan_zawodlar.objects.filter(zawod_id=pk)
    alynan = Das_is_zawod_Alynan.objects.filter(zawod_id=pk)

    seneid1=Hasabat_sene.objects.last().id

    if request.method == 'POST':
        form = Das_isleyan_zawodForm(request.POST, request.FILES)
        if form.is_valid():
            harydyn_ady = form.cleaned_data['harydyn_ady']
            b_haryt_sany = form.cleaned_data['b_haryt_sany']
            b_haryt_kg = form.cleaned_data['b_haryt_kg']
            b_bahasy_m = form.cleaned_data['b_bahasy_m']
            b_bahasy_d = form.cleaned_data['b_bahasy_d']

            haryt_s=b_haryt_sany if b_haryt_sany is not None else 0
            haryt_kg=b_haryt_kg if b_haryt_kg is not None else 0
            baha_m=b_bahasy_m if b_bahasy_m is not None else 0
            baha_d=b_bahasy_d if b_bahasy_d is not None else 0
            
            if b_haryt_sany is not None:
                obj = Das_isleyan_zawodlar.objects.create(zawod_id=pk,has_sene=seneid1,harydyn_ady=harydyn_ady,b_haryt_sany=b_haryt_sany,
                                                         b_bahasy_m=b_bahasy_m,b_bahasy_d=b_bahasy_d,
                                                         b_jemi_bahasy_m=haryt_s * baha_m,
                                                         b_jemi_bahasy_d=haryt_s * baha_d)
                obj.save()
            elif b_haryt_kg is not None:
                obj = Das_isleyan_zawodlar.objects.create(zawod_id=pk,has_sene=seneid1,harydyn_ady=harydyn_ady,
                                                         b_haryt_kg=b_haryt_kg,b_bahasy_m=b_bahasy_m,b_bahasy_d=b_bahasy_d,
                                                         b_jemi_bahasy_m=haryt_kg * baha_m,
                                                         b_jemi_bahasy_d=haryt_kg * baha_d)
                obj.save()
            
            messages.success(request, 'Zakaza berilen haryt girizildi!')
            return redirect('das-zawod-detail', pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Zakaza berilen haryt girizilmedi')
    else:
        form = Das_isleyan_zawodForm()
    
    paginator = Paginator(zaw, 10) 
    page = request.GET.get('page')
    try:
        myuser = paginator.get_page(page)
    except PageNotAnInteger:
        myuser = paginator.page(1)
    except EmptyPage:
        myuser = paginator.page(paginator.num_pages)

    context = {'title': page_title,'myuser':myuser,'form': form,'alynan':alynan}
    return render(request, 'shu/das_islesilyan_zawodlar.html', context)

@login_required(login_url='login')
def Zawod_detail_update(request, pk):
    page_title = _('Alynan harytlary girizmek')

    if request.method == 'POST':
        form = Das_isleyan_zawod_UpdateForm(request.POST, request.FILES)
        if form.is_valid():
            a_haryt_sany = form.cleaned_data['a_haryt_sany']
            a_haryt_kg = form.cleaned_data['a_haryt_kg']
            bellik = form.cleaned_data['bellik']
            seneid1=Hasabat_sene.objects.last().id
            obj = Das_isleyan_zawodlar.objects.get(id=pk)

            if a_haryt_sany is not None:
                jemi_m = a_haryt_sany * obj.b_bahasy_m if obj.b_bahasy_m is not None else 0
                jemi_d = a_haryt_sany * obj.b_bahasy_d if obj.b_bahasy_d is not None else 0
                
                alynan_create=Das_is_zawod_Alynan.objects.create(zak_berilen_id=obj.pk,zawod=obj.zawod,harydyn_ady=obj.harydyn_ady,
                                                                 has_sene=seneid1,a_haryt_sany=a_haryt_sany,a_jemi_bahasy_m=jemi_m,
                                                                 a_jemi_bahasy_d=jemi_d,bellik=bellik)
                alynan_create.save()

                obj.tapawut_m = obj.b_jemi_bahasy_m - jemi_m
                obj.tapawut_d = obj.b_jemi_bahasy_d - jemi_d
                giden_h=obj.b_haryt_sany - a_haryt_sany
                obj.g_haryt_sany = giden_h
                obj.save()
            elif a_haryt_kg is not None:
                jemi_m = a_haryt_kg * obj.b_bahasy_m if obj.b_bahasy_m is not None else 0
                jemi_d = a_haryt_kg * obj.b_bahasy_d if obj.b_bahasy_d is not None else 0

                alynan_create=Das_is_zawod_Alynan.objects.create(zak_berilen_id=obj.pk,zawod=obj.zawod,harydyn_ady=obj.harydyn_ady,
                                                                 has_sene=seneid1,a_haryt_kg=a_haryt_kg,a_jemi_bahasy_m=jemi_m,
                                                                 a_jemi_bahasy_d=jemi_d,bellik=bellik)
                alynan_create.save()

                obj.tapawut_m = obj.b_jemi_bahasy_m - jemi_m
                obj.tapawut_d = obj.b_jemi_bahasy_d - jemi_d
                giden_h=obj.b_haryt_kg - a_haryt_kg
                obj.g_haryt_kg = giden_h
                obj.save()
            messages.success(request, 'Alynan harytlar girizildi!')
            return redirect('das-zawod-detail', obj.zawod.pk)
        else:
            messages.error(request, 'Ýalňyşlyk: Alynan harytlar girizilmedi')
    else:
        form = Das_isleyan_zawod_UpdateForm()

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Das_zawod_edit(request, pk):
    page_title = _('Daşyndan işleşilýän zawoda berilen alynan harydy üýtgetmek')
    obj = Das_isleyan_zawodlar.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Das_isleyan_zawod_editForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşyndan işleşilýän zawoda berilen alynan haryt üýtgedildi!')
           return redirect('das-zawod-detail', pk)
    else:
        form = Das_isleyan_zawod_editForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)

@login_required(login_url='login')
def Das_is_zawod_Alynan_edit(request, pk):
    page_title = _('Daşyndan işleşilýän zawoda alynan harydy üýtgetmek')
    obj = Das_is_zawod_Alynan.objects.get(id=pk)
    
    if request.method == 'POST':
        form = Das_is_zawod_AlynanForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
           form.save()
           messages.success(request, 'Daşyndan işleşilýän zawoda berilen alynan haryt üýtgedildi!')
           return redirect('das-zawod-detail', pk)
    else:
        form = Das_is_zawod_AlynanForm(instance=obj)

    context = {'title': page_title,'form': form}
    return render(request, 'shu/sehler_satylan_update.html', context)


# Delete
@login_required(login_url='login')
def delete_karzPul(request, pk):
    record = Das_karz_alynanpul.objects.get(pk=pk)
    record.delete()
    return redirect('karz-pul')

@login_required(login_url='login')
def delete_cigmalAlynan(request, pk):
    record = World_cygmal.objects.get(pk=pk)
    record.delete()
    return redirect('cigmal-zawotdan')

@login_required(login_url='login')
def delete_cigmalSklad(request, pk):
    record = World_sklad.objects.get(pk=pk)
    record.delete()
    return redirect('cigmal-zawotdan')

@login_required(login_url='login')
def delete_SkladaGelen(request, pk):
    record = Gelen_sklat.objects.get(pk=pk)
    record.delete()
    return redirect('sklad')

@login_required(login_url='login')
def delete_SkladHasabat(request, pk):
    record = AydakySklad_hasabat.objects.get(pk=pk)
    record.delete()
    return redirect('sklad')

@login_required(login_url='login')
def delete_export(request, pk):
    record = Export_yukler.objects.get(pk=pk)
    record.delete()
    return redirect('export')

@login_required(login_url='login')
def delete_import(request, pk):
    record = Import_yukpul.objects.get(pk=pk)
    record.delete()
    return redirect('import')

@login_required(login_url='login')
def delete_dasZawAdy(request, pk):
    record = Das_zawod.objects.get(pk=pk)
    record.delete()
    return redirect('das-zawod')

@login_required(login_url='login')
def delete_dasZawod(request, pk):
    record = Das_isleyan_zawodlar.objects.get(pk=pk)
    record.delete()
    return redirect('das-zawod-detail',record.pk)

@login_required(login_url='login')
def delete_Manager_user(request, pk):
    record = Manager_user.objects.get(pk=pk)
    record.delete()
    return redirect('manager')

@login_required(login_url='login')
def delete_dasKlient(request, pk):
    record = Das_yurt_klientler.objects.get(pk=pk)
    record.delete()
    return redirect('manager-detail',record.pk)

@login_required(login_url='login')
def delete_Bolek_hasaplar(request, pk):
    record = Bolek_hasaplar.objects.get(pk=pk)
    record.delete()
    return redirect('hasaphana-admin')

@login_required(login_url='login')
def delete_Ojidanie(request, pk):
    record = Ojidanie.objects.get(pk=pk)
    record.delete()
    return redirect('hasaphana',record.pk)

@login_required(login_url='login')
def delete_Inwentar(request, pk):
    record = Inwentar.objects.get(pk=pk)
    record.delete()
    return redirect('inwentar')

@login_required(login_url='login')
def delete_Inwen_spisat(request, pk):
    record = Inwen_spisat.objects.get(pk=pk)
    record.delete()
    return redirect('inwentar')

@login_required(login_url='login')
def delete_Aylyk_premya(request, pk):
    record = Aylyk_premya.objects.get(pk=pk)
    record.delete()
    return redirect('aylyk-premya')

@login_required(login_url='login')
def delete_Bank_user(request, pk):
    record = Bank_user.objects.get(pk=pk)
    record.delete()
    return redirect('bank-users',record.pk)

@login_required(login_url='login')
def delete_Bank(request, pk):
    record = Bank.objects.get(pk=pk)
    record.delete()
    return redirect('bank-hereket',record.pk)

#Sapak seh
@login_required(login_url='login')
def delete_Sapakseh(request, pk):
    record = Gundelik_sapak.objects.get(pk=pk)
    record.delete()
    return redirect('sapak-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_Aydaky_sapak(request, pk):
    record = Aydaky_sapak.objects.get(pk=pk)
    record.delete()
    return redirect('sapak-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_AydakySapak_hasabat(request, pk):
    record = AydakySapak_hasabat.objects.get(pk=pk)
    record.delete()
    return redirect('sapak-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Zakaz_SapakSwotka(request, pk):
    record = Zakaz_SapakSwotka.objects.get(pk=pk)
    record.delete()
    return redirect('sapak-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Sapak_seh_ay_tabel(request, pk):
    record = Sapak_seh_ay_tabel.objects.get(pk=pk)
    record.delete()
    return redirect('s-aylyk-tabel')

# Dokma Seh
@login_required(login_url='login')
def delete_DokmaSeh(request, pk):
    record = Gundelik_dokma.objects.get(pk=pk)
    record.delete()
    return redirect('dokma-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_Aydaky_dokma(request, pk):
    record = Aydaky_dokma.objects.get(pk=pk)
    record.delete()
    return redirect('dokma-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_AydakyDokma_hasabat(request, pk):
    record = AydakyDokma_hasabat.objects.get(pk=pk)
    record.delete()
    return redirect('dokma-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Zakaz_DokmaSwotka(request, pk):
    record = Zakaz_DokmaSwotka.objects.get(pk=pk)
    record.delete()
    return redirect('dokma-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Dokma_seh_ay_tabel(request, pk):
    record = Dokma_seh_ay_tabel.objects.get(pk=pk)
    record.delete()
    return redirect('d-aylyk-tabel')

# Halta seh
@login_required(login_url='login')
def delete_HaltaSeh(request, pk):
    record = Gundelik_halta.objects.get(pk=pk)
    record.delete()
    return redirect('halta-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_Aydaky_halta(request, pk):
    record = Aydaky_halta.objects.get(pk=pk)
    record.delete()
    return redirect('halta-seh',record.sehs.pk)

@login_required(login_url='login')
def delete_Aydakyhalta_hasabat(request, pk):
    record = Aydakyhalta_hasabat.objects.get(pk=pk)
    record.delete()
    return redirect('halta-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Zakaz_swotka(request, pk):
    record = Zakaz_swotka.objects.get(pk=pk)
    record.delete()
    return redirect('halta-seh-hasabat',record.sehs.pk)

@login_required(login_url='login')
def delete_Halta_seh_ay_tabel(request, pk):
    record = Halta_seh_ay_tabel.objects.get(pk=pk)
    record.delete()
    return redirect('h-aylyk-tabel')

# Zakazcy balans
@login_required(login_url='login')
def delete_Other_users(request, pk):
    record = Other_users.objects.get(pk=pk)
    record.delete()
    return redirect('zakaz-users')

@login_required(login_url='login')
def delete_Zakaz_balans(request, pk):
    record = Zakaz_balans.objects.get(pk=pk)
    record.delete()
    return redirect('zakazusers-detail',record.user.pk)

#Sklad
@login_required(login_url='login')
def delete_Sapakseh_sklad(request, pk):
    record = Sapakseh_sklad.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-sapak-seh')

@login_required(login_url='login')
def delete_Sapakseh_sklad_satylan(request, pk):
    record = Sapakseh_sklad_satylan.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-sapak-seh')

@login_required(login_url='login')
def delete_Dokmaseh_sklad(request, pk):
    record = Dokmaseh_sklad.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-dokma-seh')

@login_required(login_url='login')
def delete_Dokmaseh_sklad_satylan(request, pk):
    record = Dokmaseh_sklad_satylan.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-dokma-seh')

@login_required(login_url='login')
def delete_Haltaseh_sklad(request, pk):
    record = Haltaseh_sklad.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-halta-seh')

@login_required(login_url='login')
def delete_Haltaseh_sklad_satylan(request, pk):
    record = Haltaseh_sklad_satylan.objects.get(pk=pk)
    record.delete()
    return redirect('sklad-halta-seh')

# Dasary yurt klient
@login_required(login_url='login')
def delete_Das_yurt_klient_cykdajy(request, pk):
    record = Das_yurt_klient_cykdajy.objects.get(pk=pk)
    record.delete()
    return redirect('manager-detail',record.gir_klient.pk)

@login_required(login_url='login')
def delete_Das_is_zawod_Alynan(request, pk):
    record = Das_is_zawod_Alynan.objects.get(pk=pk)
    record.delete()
    return redirect('das-zawod-detail',record.zak_berilen.pk)

@login_required(login_url='login')
def delete_Karz_yzyna_berilen(request, pk):
    record = Karz_yzyna_berilen.objects.get(pk=pk)
    record.delete()
    return redirect('karz-pul')

