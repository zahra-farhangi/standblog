from django.shortcuts import render, get_object_or_404
from article.models import Article


def post_detail(request, pk):
    article = get_object_or_404(Article, id=pk)
    return render(request, "article/article_details.html", {'article': article})
