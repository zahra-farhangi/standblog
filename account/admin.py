from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'join_date')
    raw_id_fields = ('user',)



# admin.site.site_header = "مدیریت وبلاگ"