from django.contrib import admin
from . models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Message)

