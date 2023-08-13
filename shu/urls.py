from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from users import views as user_views
from shu.views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('hasaphana_admin/', views.Hasaphana_admin, name='hasaphana-admin'),
    path('hasaphana/<int:pk>/', views.Hasaphana, name='hasaphana'),
    path('aylykpremya/', views.AylykPeydaPremya, name='aylyk-premya'),
    path('ojidanie_update/<int:pk>/', views.Ojidanie_update, name='ojidanie-update'),
    path('office_kadr/', views.KadrPanel, name='office-kadr'),
    path('kadr_office/<int:pk>/', views.Kadr_office, name='kadr-office'),
    path('kadr_detail/<int:pk>/', views.Kadr_detail, name='kadr-detail'),
    path('inwentar_sanaw/', views.Inwentar_sanaw, name='inwentar'),
    path('inwentar_spisat/<int:pk>/', views.Inwentar_update, name='inwentar-spisat'),
    path('karz_pul/', views.Karz_pul, name='karz-pul'),
    path('karz_pul_update/<int:pk>/', views.Karaz_pul_update, name='karz-pul-update'),
    path('export/', views.ExportYuk, name='export'),
    path('import/', views.Import_pulYuk, name='import'),
    path('import_update/<int:pk>/', views.Import_update, name='import-update'),
    path('managers/', views.Managers, name='managers'),
    path('manager_detail/<int:pk>/', views.Manager_detail, name='manager-detail'),
    path('manager_detail_update/<int:pk>/', views.Mangr_detail_update, name='manager-detail-update'),
    path('walyuta_bolum/', views.Walyuta_bolum, name='walyuta-bolum'),
    path('bank_users/<int:pk>/', views.Bank_Users, name='bank-users'),
    path('bank_hereket/<int:pk>/', views.Bank_hereket, name='bank-hereket'),
    path('algylar/', views.Algy, name='algylar'),
    path('bergiler/', views.Bergi, name='bergiler'),
    path('balans/', views.Balans_view, name='balans'),
    
    path('halta_seh/<int:pk>/', views.Gun_tikhalta_sanaw, name='halta-seh'),
    # path('halta_seh_zakaz/<int:pk>/', views.Haltaseh_zakaz, name='haltaseh-zakaz'),
    path('halta_seh_hasabat/<int:pk>/', views.Haltaseh_hasabat, name='halta-seh-hasabat'),
    path('ayjemi_update/<int:pk>/', views.Ayjemi_update, name='ayjemi-update'),
    path('zakswotka_update/<int:pk>/', views.ZakSwotka_update, name='zakazswotka-update'),
    path('h_aylyk_tabel/', views.HaltaSeh_tabel, name='h-aylyk-tabel'),
    path('h_tayyar_onum/<int:pk>/', views.Haltaseh_Skladjyk, name='h-tayar=onum'),
    
    path('sapak_seh/<int:pk>/', views.Gun_ondSapak_sanaw, name='sapak-seh'),
    #path('sapak_seh_zakaz/<int:pk>/', views.Sapakseh_zakaz, name='sapakseh-zakaz'),
    path('sapak_seh_hasabat/<int:pk>/', views.Sapakseh_hasabat, name='sapak-seh-hasabat'),
    path('ayjemisapak_update/<int:pk>', views.AyjemiSapak_update, name='ayjemisap-update'),
    path('zakswotkasapak_update/<int:pk>', views.ZakSwotkaSapak_update, name='zakazswotkasap-update'),
    path('s_aylyk_tabel/', views.SapakSeh_tabel, name='s-aylyk-tabel'),
    path('s_tayyar_onum/<int:pk>/', views.Sapakseh_Skladjyk, name='s-tayar=onum'),
    
    path('dokma_seh/<int:pk>/', views.Gun_ondDokma_sanaw, name='dokma-seh'),
    #path('dokma_seh_zakaz/<int:pk>/', views.Dokmaseh_zakaz, name='dokmaseh-zakaz'),
    path('dokma_seh_hasabat/<int:pk>/', views.Dokmaseh_hasabat, name='dokma-seh-hasabat'),
    path('ayjemidokma_update/<int:pk>', views.AyjemiDokma_update, name='ayjemi-dokma-update'),
    path('zakswotkadokma_update/<int:pk>', views.ZakSwotkaDokma_update, name='zakazswotka-dokma-update'),
    path('d_aylyk_tabel/', views.DokmaSeh_tabel, name='d-aylyk-tabel'),
    path('d_tayyar_onum/<int:pk>/', views.Dokmaseh_Skladjyk, name='d-tayar=onum'),

    path('office_seh/', views.OfficeSeh_sanaw, name='office_seh'),
    path('sehler/', views.Seh_office, name='sehler'),
    path('all_sehs/<int:pk>/', views.All_sehs, name='all-sehs'),
    path('yollanma/<int:pk>/', views.Yollonma, name='yollanma'),

    path('sklad/', views.Sklad, name='sklad'),
    path('sklad_update/<int:pk>/', views.Sklad_update, name='sklad-update'),
    path('ayjemisklad_update/<int:pk>/', views.AyjemiSklad_update, name='ayjemi-sklad-update'),
    path('sklad_sapakseh/', views.Sklad_sapakseh, name='sklad-sapak-seh'),
    path('sklad_dokmaseh/', views.Sklad_dokmaseh, name='sklad-dokma-seh'),
    path('sklad_haltaseh/', views.Sklad_haltaseh, name='sklad-halta-seh'),
    path('sklad_daszawod/', views.Sklad_das_zawod, name='sklad-das-zawod'),
    path('sklad_sapak_satmak/<int:pk>/', views.Sklad_sapakseh_update, name='sklad-satylan-sapak'),
    path('sklad_dokma_satmak/<int:pk>/', views.Sklad_dokmaseh_update, name='sklad-satylan-dokma'),
    path('sklad_halta_satmak/<int:pk>/', views.Sklad_haltaseh_update, name='sklad-satylan-halta'),
    path('sklad_zawod_satmak/<int:pk>/', views.Sklad_daszawod_update, name='sklad-satylan-zawod'),


    path('cigmal_zawotdan/', views.Cigmal_zawodlar, name='cigmal-zawotdan'),
    path('cigmal_send_sklad/<int:pk>/', views.Cigmal_sendSklad, name='cigmal-send-sklad'),

    path('user_delete/<int:pk>/', views.delete_myuser, name='user-delete'),
    # path('user_edit/<int:pk>', views.update_myuser, name='user-update'),
    path('load_zak_code/', views.load_zakaz, name='load_zak_code'),
    path('load_zak_gornus/', views.load_gornus, name='load_zak_gornus'),

    # Daşyndan işleşilýän zawodlar
    path('das_zawod/', views.Das_Zawodlar, name='das-zawod'),
    path('das_zawod_detail/<int:pk>/', views.Zawod_detail, name='das-zawod-detail'),
    path('das_zaw_detail_update/<int:pk>/', views.Zawod_detail_update, name='das-zaw-detail-update'),

    # edit
    path('bolek_hasap_edit/<int:pk>/', views.Bolek_hasaplar_edit, name='bolek-hasap-edit'),
    path('inwentar_edit/<int:pk>/', views.Inwentar_edit, name='inwentar-edit'),
    path('world_cigmal_edit/<int:pk>/', views.World_cygmal_edit, name='world-cigmal-edit'),
    path('world_sklad_edit/<int:pk>/', views.World_sklad_edit, name='world-sklad-edit'),
    path('gelen_sklad_edit/<int:pk>/', views.Gelen_sklat_edit, name='gelen-sklad-edit'),
    path('export_edit/<int:pk>/', views.Export_yukler_edit, name='export-edit'),
    path('import_edit/<int:pk>/', views.Import_pulYuk_edit, name='import-edit'),
    path('das_zawod_edit/<int:pk>/', views.Das_zawod_edit, name='das-zawod-edit'),
    path('das_karz_edit/<int:pk>/', views.Das_karz_edit, name='das-karz-edit'),
    path('ay_premya_edit/<int:pk>/', views.Aylyk_premya_edit, name='ay-premya-edit'),
    path('das_klient_edit/<int:pk>/', views.Das_klient_edit, name='das-klient-edit'),
    path('bank_edit/<int:pk>/', views.Bank_edit, name='bank-edit'),
    # taze
    path('karz_yzyna_bermek_edit/<int:pk>/', views.Karz_yzyna_berilen_edit, name='karz-yzyna-bermek-edit'),
    path('klient_cykdajy_edit/<int:pk>/', views.Das_yurt_klient_cykdajy_edit, name='klient-cykdajy-edit'),
    path('sapakseh_sklad_edit/<int:pk>/', views.Sapakseh_sklad_edit, name='sapakseh-sklad-edit'),
    path('sapakseh_sklad_satylan_edit/<int:pk>/', views.Sapakseh_sklad_satylan_edit, name='sapakseh-sklad-satylan-edit'),
    path('dokmakseh_sklad_edit/<int:pk>/', views.Dokmaseh_sklad_edit, name='dokmaseh-sklad-edit'),
    path('dokmakseh_sklad_satylan_edit/<int:pk>/', views.Dokmaseh_sklad_satylan_edit, name='dokmaseh-sklad-satylan-edit'),
    path('haltaseh_sklad_edit/<int:pk>/', views.Haltaseh_sklad_edit, name='haltaseh-sklad-edit'),
    path('haltaseh_sklad_satylan_edit/<int:pk>/', views.Haltaseh_sklad_satylan_edit, name='haltaseh-sklad-satylan-edit'),
    path('das_zawod_alynan_edit/<int:pk>/', views.Das_is_zawod_Alynan_edit, name='das-zawod-alynan-edit'),

    path('haltaseh_edit/<int:pk>/', views.Haltaseh_edit, name='haltaseh-edit'),
    path('aydaky_halta_edit/<int:pk>/', views.Aydaky_halta_edit, name='aydaky-halta-edit'),
    path('ay_halta_hasabat_edit/<int:pk>/', views.Aydakyhalta_hasabat_edit, name='ay-hasabat-halta-edit'),
    path('tabel_halta_edit/<int:pk>/', views.Halta_seh_ay_tabel_edit, name='tabel-halta-edit'),
    
    path('sapakseh_edit/<int:pk>/', views.Sapakseh_edit, name='sapakseh-edit'),
    path('aydaky_sapak_edit/<int:pk>/', views.Aydaky_sapak_edit, name='aydaky-sapak-edit'),
    path('ay_sapak_hasabat_edit/<int:pk>/', views.AydakySapak_hasabat_edit, name='ay-hasabat-sapak-edit'),
    path('tabel_sapak_edit/<int:pk>/', views.Sapak_seh_ay_tabel_edit, name='tabel-sapak-edit'),
    
    path('dokmaseh_edit/<int:pk>/', views.Dokmaseh_edit, name='dokmaseh-edit'),
    path('aydaky_dokma_edit/<int:pk>/', views.Aydaky_dokma_edit, name='aydaky-dokma-edit'),
    path('ay_dokma_hasabat_edit/<int:pk>/', views.AydakyDokma_hasabat_edit, name='ay-hasabat-dokma-edit'),
    path('tabel_dokma_edit/<int:pk>/', views.Dokma_seh_ay_tabel_edit, name='tabel-dokma-edit'),
    

    # delete
    path('inwentar/<int:pk>/delete/', views.delete_Inwentar, name='inwentar-delete'),
    path('inwentar_spisat/<int:pk>/delete/', views.delete_Inwen_spisat, name='inwentar-spisat-delete'),
    path('bolek_hasap/<int:pk>/delete/', views.delete_Bolek_hasaplar, name='bolek-hasap-delete'),
    path('world_cigmal/<int:pk>/delete/', views.World_cygmal_edit, name='world-cigmal-delete'),
    path('world_sklad/<int:pk>/delete/', views.World_sklad_edit, name='world-sklad-delete'),
    path('gelen_sklad/<int:pk>/delete/', views.delete_SkladaGelen, name='gelen-sklad-delete'),
    path('sklad_hasabat/<int:pk>/delete/', views.delete_SkladHasabat, name='sklad-hasabat-delete'),
    path('export/<int:pk>/delete/', views.delete_export, name='export-delete'),
    path('import/<int:pk>/delete/', views.delete_import, name='import-delete'),
    path('das_zawod/<int:pk>/delete/', views.delete_dasZawod, name='das-zawod-delete'),
    path('das_karz/<int:pk>/delete/', views.delete_karzPul, name='das-karz-delete'),
    path('ay_premya/<int:pk>/delete/', views.delete_Aylyk_premya, name='ay-premya-delete'),
    path('das_klient/<int:pk>/delete/', views.delete_dasKlient, name='das-klient-delete'),
    path('bank/<int:pk>/delete/', views.delete_Bank, name='bank-delete'),
    # taze
    path('karz_yzyna_bermek/<int:pk>/delete/', views.delete_Karz_yzyna_berilen, name='karz-yzyna-bermek-delete'),
    path('klient_cykdajy/<int:pk>/delete/', views.delete_Das_yurt_klient_cykdajy, name='klient-cykdajy-delete'),
    path('sapakseh_sklad/<int:pk>/delete/', views.delete_Sapakseh_sklad, name='sapakseh-sklad-delete'),
    path('sapakseh_sklad_satylan/<int:pk>/delete/', views.delete_Sapakseh_sklad_satylan, name='sapakseh-sklad-satylan-delete'),
    path('dokmaseh_sklad/<int:pk>/delete/', views.delete_Dokmaseh_sklad, name='dokmaseh-sklad-delete'),
    path('dokmaseh_sklad_satylan/<int:pk>/delete/', views.delete_Dokmaseh_sklad_satylan, name='dokmaseh-sklad-satylan-delete'),
    path('haltaseh_sklad/<int:pk>/delete/', views.delete_Haltaseh_sklad, name='haltaseh-sklad-delete'),
    path('haltaseh_sklad_satylan/<int:pk>/delete/', views.delete_Haltaseh_sklad_satylan, name='haltaseh-sklad-satylan-delete'),
    path('das_zawod_alynan/<int:pk>/delete/', views.delete_Das_is_zawod_Alynan, name='das-zawod-alynan-delete'),

    # halta seh delete
    path('halta_seh/<int:pk>/delete/', views.delete_HaltaSeh, name='haltaseh-delete'),
    path('aydaky_halta/<int:pk>/delete/', views.delete_Aydaky_halta, name='aydaky-halta-delete'),
    path('ay_halta_hasabat/<int:pk>/delete/', views.delete_Aydakyhalta_hasabat, name='ay-halta-hasabat-delete'),
    path('tabel_halta/<int:pk>/delete/', views.delete_Halta_seh_ay_tabel, name='tabel-halta-delete'),

    # sapak seh delete
    path('sapak_seh/<int:pk>/delete/', views.delete_Sapakseh, name='sapakseh-delete'),
    path('aydaky_sapak/<int:pk>/delete/', views.delete_Aydaky_sapak, name='aydaky-sapak-delete'),
    path('ay_sapak_hasabat/<int:pk>/delete/', views.delete_AydakySapak_hasabat, name='ay-sapak-hasabat-delete'),
    path('tabel_sapak/<int:pk>/delete/', views.delete_Sapak_seh_ay_tabel, name='tabel-sapak-delete'),

    # Dokma seh delete
    path('dokma_seh/<int:pk>/delete/', views.delete_DokmaSeh, name='dokmaseh-delete'),
    path('aydaky_dokma/<int:pk>/delete/', views.delete_Aydaky_dokma, name='aydaky-dokma-delete'),
    path('ay_dokma_hasabat/<int:pk>/delete/', views.delete_AydakyDokma_hasabat, name='ay-dokma-hasabat-delete'),
    path('tabel_dokma/<int:pk>/delete/', views.delete_Dokma_seh_ay_tabel, name='tabel-dokma-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)