from django.shortcuts import render,redirect
from article.models import Article



def home(request):
    # articles = Article.custom_manager.all()
    articles = Article.objects.all()
    return render(request, 'home/index.html', {'articles': articles})



def sidebar(request):
    context = {'name': 'Atusa Fa'}
    return render(request, 'includes/sidebar.html', context)