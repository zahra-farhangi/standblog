from datetime import timedelta

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.timezone import now
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(status=True)


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='articles',
                               verbose_name='نویسنده')
    category = models.ManyToManyField(Category, related_name='articles', verbose_name='دسته بندی')
    title = models.CharField(max_length=70, blank=True, null=True, verbose_name='عنوان')
    body = models.TextField(blank=True, null=True, verbose_name='متن')
    image = models.ImageField(upload_to="images/articles", blank=True, null=True, verbose_name='عکس')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ انتشار')
    updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='تاریخ بروز رسانی')
    myfile = models.FileField(upload_to='test', null=True, verbose_name='فایل من')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    objects = models.Manager()
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True, verbose_name='اسلاگ')
    custom_manager = ArticleManager()
    published = models.BooleanField(default=True, verbose_name='وضعیت انتشار')
    reading_time = models.PositiveIntegerField(default=0, verbose_name='تایم مطالعه')
    pub_date = models.DateTimeField(default=now, verbose_name='تاریخ بروز رسانی')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    # def save(
    #     self,
    #     *args,
    #     force_insert=False,
    #     force_update=False,
    #     using=None,
    #     update_fields=None,
    # ):
    #     self.slug = slugify(self.title)
    #     super(Article, self).save()

    def get_absolute_url(self):
        return reverse('article:article_detail', kwargs={'slug': self.slug, 'id': self.id})

    def show_image(self):
        if self.image:
            return format_html(f'<img src="{self.image.url}" width="60px" height="50px">')
        return format_html('<h3 style="color: red">بدون تصویر</h3>')

    show_image.short_description = "عکس مقاله"

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='نویسنده')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True,
                               verbose_name='زیر مجموعه')
    body = models.TextField(verbose_name='متن کامنت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    def __str__(self):
        return f"{self.body[:50]}"

    # متد جدید برای نمایش نام کاربر
    def get_user_name(self):
        return self.user.get_full_name() or self.user.username
    get_user_name.short_description = 'نام کاربر'  # عنوان دلخواه

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    email = models.EmailField(verbose_name='ایمیل')
    text = models.TextField(verbose_name='متن پیام')
    # age = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    # date = models.DateTimeField(default=timezone.now())

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'



class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes', verbose_name='مقاله')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.article.title}"


    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
        ordering = ('-created_at',)
