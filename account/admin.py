from django.contrib import admin
from .models import Profile
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'join_date')
    raw_id_fields = ('user',)
    list_filter = [('join_date', JDateFieldListFilter)]



# admin.site.site_header = "مدیریت وبلاگ"