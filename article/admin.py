from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin

class FilterByTitle(admin.SimpleListFilter):
    title = 'کلید های پر تکرار'
    parameter_name = 'title'

    def lookups(self, request, model_admin):
        return (
            ('django', 'جنگو'),
            ('python', 'پایتون'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(title__icontains=self.value())


class CommentInline(admin.StackedInline):
    model = Comment
    fields = ['body', 'user', 'article', 'created_at']
    readonly_fields = ['created_at']
    extra = 1
    show_change_link = True





@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'published', 'show_image', 'created')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('author',)
    list_filter = (('published', JDateFieldListFilter), ('updated', JDateFieldListFilter), FilterByTitle)
    search_fields = ('title__icontains', 'body__icontains')
    # inlines = (CommentInline,)
    # fields = ('body', 'slug', 'title')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')



class CommentAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'body', 'created_at')
    search_fields = ['body', 'user__username']


class LikeAdmin(admin.ModelAdmin):
    list_filter = (('created_at', JDateFieldListFilter),)
    list_display = ('article', 'created_at')
    search_fields = ['article']

admin.site.register(Comment, CommentAdmin)


admin.site.register(Message, MessageAdmin)
admin.site.register(Category)
# admin.site.register(Comment)
admin.site.register(Like, LikeAdmin)
