from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from article.models import Article, Category, Comment, Message
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ContactUsForm, MessageForm

def article_detail(request, slug, id=None):
    article = get_object_or_404(Article, slug=slug, id=id)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')
        Comment.objects.create(body=body, article=article, user=request.user, parent_id=parent_id)
    return render(request, "article/article_details.html", {'article': article})


def article_list(request):
    articles = Article.objects.all()
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 1)
    try:
        objects_list = paginator.page(page_number)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        raise Http404("صفحه مورد نظر پیدا نشد")
    return render(request, 'article/articles_list.html', {'articles': objects_list})


def category_detail(request, pk=None):
    category = get_object_or_404(Category, id=pk)
    articles = category.articles.all()
    return render(request, "article/articles_list.html", {'articles': articles})



def search(request):
    q = request.GET.get('q')
    articles = Article.objects.filter(title__icontains=q)
    page_number = request.GET.get('page')
    paginator = Paginator(articles, 1)
    try:
        objects_list = paginator.page(page_number)
    except PageNotAnInteger:
        objects_list = paginator.page(1)
    except EmptyPage:
        raise Http404("صفحه مورد نظر پیدا نشد")
    return render(request, "article/articles_list.html", {'articles': objects_list})


def contactus(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # title = form.cleaned_data['title']
            # text = form.cleaned_data['text']
            # email = form.cleaned_data['email']
            # Message.objects.create(title=title, text=text, email=email)
            instance = form.save(commit=False)
            instance.age += 5
            instance.save()
    else:
        form = MessageForm()
    return render(request, "article/contact_us.html", {'form': form})










