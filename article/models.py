from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(status=True)

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ManyToManyField(Category)
    title = models.CharField(max_length=70, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images/articles", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    myfile = models.FileField(upload_to='test' ,null=True)
    status = models.BooleanField(default=True)
    objects = models.Manager()
    custom_manager = ArticleManager()
    published = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title} - {self.body[:30]}"


class New(models.Model):
    title = models.CharField(max_length=30)
    des = models.TextField()


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.replace(' ', '-')
        super(New, self).save(args, kwargs)
