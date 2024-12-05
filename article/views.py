from django.http import Http404
from django.shortcuts import render, get_object_or_404
from article.models import Article, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def article_detail(request, slug, id=None):
    article = get_object_or_404(Article, slug=slug, id=id)
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