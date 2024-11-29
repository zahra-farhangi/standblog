from django.shortcuts import render
from article.models import Article, New

def home(request):
    # articles = Article.objects.all()
    articles = Article.custom_manager.all()
    return render(request, 'home/index.html', {'articles': articles})


#  lazy evaluation