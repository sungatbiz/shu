from django.contrib import admin
from .models import *


class Gir_ostatokAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Bolek_hasaplarAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class OjidanieAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene', 'sebap')
    list_display_links = ('id', 'sene', 'sebap')
    search_fields = ('sene','sebap',)

class InwentarAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

class Gelen_sklatAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

class Gundelik_haltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Equ_moneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Equ_moneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class World_cygmalAdmin(admin.ModelAdmin):
    list_display = ('id', 'kontrak_nomer')
    list_display_links = ('id', 'kontrak_nomer')
    search_fields = ('kontrak_nomer',)

class World_skladAdmin(admin.ModelAdmin):
    list_display = ('id', 'kontrak_nomer')
    list_display_links = ('id', 'kontrak_nomer')
    search_fields = ('kontrak_nomer',)

class Halta_gornusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Sehe_paylamakAdmin(admin.ModelAdmin):
    list_display = ('id', 'karhana')
    list_display_links = ('id', 'karhana')
    search_fields = ('karhana',)

class Aydaky_haltaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Inwen_spisatAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

class Walyuta_hasapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Hasap_detailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Aylyk_premyaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Aydakyhalta_hasabatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Halta_seh_ay_tabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Zakaz_balansAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz_sene')
    list_display_links = ('id', 'zakaz_sene')
    search_fields = ('zakaz_sene',)

class Hasabat_seneAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Bank_userAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'wal')
    list_display_links = ('id', 'user')
    search_fields = ('user',)


# Dokma SEH

class Gundelik_dokmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Aydaky_dokmaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class AydakyDokma_hasabatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Zakaz_DokmaSwotkaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Dokma_seh_ay_tabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)


# Sapak SEH

class Gundelik_sapakAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Aydaky_sapakAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class AydakySapak_hasabatAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Zakaz_SapakSwotkaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Sapak_seh_ay_tabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

# Dasyndan isleyan zawodlar
class Das_zawodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Das_isleyan_zawodlarAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

class Das_is_zawod_AlynanAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

# Dasary yurt klientler
class Das_yurt_klientlerAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)

class Das_yurt_klient_cykdajyAdmin(admin.ModelAdmin):
    list_display = ('id', 'harydyn_ady')
    list_display_links = ('id', 'harydyn_ady')
    search_fields = ('harydyn_ady',)


# Sklad sklada giden we satylan onumler
class Haltaseh_skladAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Haltaseh_sklad_satylanAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Sapakseh_skladAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Sapakseh_sklad_satylanAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Dokmaseh_skladAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)

class Dokmaseh_sklad_satylanAdmin(admin.ModelAdmin):
    list_display = ('id', 'sene')
    list_display_links = ('id', 'sene')
    search_fields = ('sene',)


# Dasyndan karz alynan pullar
class Das_karz_alynanpulAdmin(admin.ModelAdmin):
    list_display = ('id', 'karzcy')
    list_display_links = ('id', 'karzcy')
    search_fields = ('karzcy',)

class Karz_yzyna_berilenpulAdmin(admin.ModelAdmin):
    list_display = ('id', 'karzcy')
    list_display_links = ('id', 'karzcy')
    search_fields = ('karzcy',)




# Dasyndan karz alynan pullar
admin.site.register(Das_karz_alynanpul, Das_karz_alynanpulAdmin)
admin.site.register(Karz_yzyna_berilen, Karz_yzyna_berilenpulAdmin)

# Sklad sklada giden we satylan onumler
admin.site.register(Haltaseh_sklad, Haltaseh_skladAdmin)
admin.site.register(Haltaseh_sklad_satylan, Haltaseh_sklad_satylanAdmin)
admin.site.register(Sapakseh_sklad, Sapakseh_skladAdmin)
admin.site.register(Sapakseh_sklad_satylan, Sapakseh_sklad_satylanAdmin)
admin.site.register(Dokmaseh_sklad, Dokmaseh_skladAdmin)
admin.site.register(Dokmaseh_sklad_satylan, Dokmaseh_sklad_satylanAdmin)

# Dasyndan isleyan zawodlar
admin.site.register(Das_zawod, Das_zawodAdmin)
admin.site.register(Das_isleyan_zawodlar, Das_isleyan_zawodlarAdmin)
admin.site.register(Das_is_zawod_Alynan, Das_is_zawod_AlynanAdmin)

# Dasary yurt klientler
admin.site.register(Das_yurt_klientler, Das_yurt_klientlerAdmin)
admin.site.register(Das_yurt_klient_cykdajy, Das_yurt_klient_cykdajyAdmin)

# Dokma SEH
admin.site.register(Sapak_seh_ay_tabel, Sapak_seh_ay_tabelAdmin)
admin.site.register(Zakaz_SapakSwotka, Zakaz_SapakSwotkaAdmin)
admin.site.register(AydakySapak_hasabat, AydakySapak_hasabatAdmin)
admin.site.register(Aydaky_sapak, Aydaky_sapakAdmin)
admin.site.register(Gundelik_sapak, Gundelik_sapakAdmin)

# Dokma SEH
admin.site.register(Dokma_seh_ay_tabel, Dokma_seh_ay_tabelAdmin)
admin.site.register(Zakaz_DokmaSwotka, Zakaz_DokmaSwotkaAdmin)
admin.site.register(AydakyDokma_hasabat, AydakyDokma_hasabatAdmin)
admin.site.register(Aydaky_dokma, Aydaky_dokmaAdmin)
admin.site.register(Gundelik_dokma, Gundelik_dokmaAdmin)

admin.site.register(Hasabat_sene, Hasabat_seneAdmin)
admin.site.register(Zakaz_balans, Zakaz_balansAdmin)
admin.site.register(Halta_seh_ay_tabel, Halta_seh_ay_tabelAdmin)
admin.site.register(Aydakyhalta_hasabat, Aydakyhalta_hasabatAdmin)
admin.site.register(Aylyk_premya, Aylyk_premyaAdmin)
admin.site.register(Walyuta_hasap, Walyuta_hasapAdmin)
admin.site.register(Hasap_detail, Hasap_detailAdmin)
admin.site.register(Gir_ostatok, Gir_ostatokAdmin)
admin.site.register(Bolek_hasaplar, Bolek_hasaplarAdmin)
admin.site.register(Ojidanie, OjidanieAdmin)
admin.site.register(Inwentar, InwentarAdmin)
admin.site.register(Gelen_sklat, Gelen_sklatAdmin)
admin.site.register(Gundelik_halta, Gundelik_haltaAdmin)
admin.site.register(Equ_money, Equ_moneyAdmin)
admin.site.register(World_cygmal, World_cygmalAdmin)
admin.site.register(World_sklad, World_skladAdmin)
admin.site.register(Halta_gornus, Halta_gornusAdmin)
admin.site.register(Sehe_paylamak, Sehe_paylamakAdmin)
admin.site.register(Aydaky_halta, Aydaky_haltaAdmin)
admin.site.register(Inwen_spisat, Inwen_spisatAdmin)
admin.site.register(Bank_user, Bank_userAdmin)
admin.site.register(Bank, BankAdmin)