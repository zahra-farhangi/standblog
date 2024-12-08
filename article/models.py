from datetime import timedelta
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(status=True)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='articles')
    category = models.ManyToManyField(Category, related_name='articles')
    title = models.CharField(max_length=70, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/articles", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    myfile = models.FileField(upload_to='test' ,null=True)
    status = models.BooleanField(default=True)
    objects = models.Manager()
    slug = models.SlugField(blank=True, unique=True, allow_unicode=True)
    custom_manager = ArticleManager()
    published = models.BooleanField(default=True)


    class Meta:
        ordering = ('-created',)



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


    def __str__(self):
        return f"{self.title} - {self.body[:30]}"


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[:50]
