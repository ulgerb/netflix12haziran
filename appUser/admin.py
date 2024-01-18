from django.contrib import admin
from appUser.models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

   list_display = ('user','title', 'isview','id', 'isnew', 'islogin')
   list_editable = ('isview','isnew','islogin') # liste görünümünde değiştilmesine izin verir
   # list_filter = ('',) Filtreleme
   readonly_fields = ('title',) # Adminde Değiştilemesin
   search_fields = ('user__username',) # arama yap
   # date_hierarchy = '' Tarih Çizelgesi
   # ordering = ('',) Sıralama


