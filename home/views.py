from django.shortcuts import render,redirect
from article.models import *
from django.contrib.auth.decorators import login_required


def home(request):
    # articles = Article.custom_manager.all()
    articles = Article.objects.all()
    return render(request, 'home/index.html', {'articles': articles})



def sidebar(request):
    context = {'name': 'Atusa Fa'}
    return render(request, 'includes/sidebar.html', context)

@login_required(login_url='account:login')
def dashboard(request):
    user = request.user
    articles = Article.objects.filter(author=user)

    context ={
        'user': user,
        'articles': articles,
    }

    return render(request, 'home/dashboard.html', context)