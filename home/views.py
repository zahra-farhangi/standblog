from django.shortcuts import render,redirect
from article.models import *
from django.contrib.auth.decorators import login_required
from article.forms import MessageForm


def home(request):
    articles = Article.objects.filter(published=True)
    return render(request, 'home/index.html', {'articles': articles})



def sidebar(request):
    context = {'name': 'programming'}
    return render(request, 'includes/sidebar.html', context)

@login_required(login_url='account:login')
def dashboard(request):
    user = request.user
    articles = Article.objects.filter(author=user)
    form = MessageForm()  # ایجاد نمونه فرم

    context ={
        'user': user,
        'articles': articles,
        'form': form,
    }

    return render(request, 'home/dashboard.html', context)