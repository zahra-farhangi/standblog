from django.contrib import admin
from . models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created')
    prepopulated_fields = {'slug': ('title',)}


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Category)
admin.site.register(Comment)


