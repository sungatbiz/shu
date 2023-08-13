from django.contrib import admin
from .models import *


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class BolumAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class WezAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class Wez_otherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class Other_usersAdmin(admin.ModelAdmin):
    list_display = ('id', 'faa')
    list_display_links = ('id', 'faa')
    search_fields = ('faa',)

class SehlerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Cigmal_ZawodlarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class Manager_userAdmin(admin.ModelAdmin):
    list_display = ('id', 'faa')
    list_display_links = ('id', 'faa')
    search_fields = ('faa',)

class Primary_SehAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(AllUsers)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Bolum, BolumAdmin)
admin.site.register(Wez, WezAdmin)
admin.site.register(Wez_other, Wez_otherAdmin)
admin.site.register(Other_users, Other_usersAdmin)
admin.site.register(Sehler, SehlerAdmin)
admin.site.register(Cigmal_Zawodlar, Cigmal_ZawodlarAdmin)
admin.site.register(Manager_user, Manager_userAdmin)
admin.site.register(Primary_Seh, Primary_SehAdmin)
