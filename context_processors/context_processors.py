from article.models import Article, Category


def recent_articles(request):
    recent_articles = Article.objects.order_by('-created')[:3]

    return {'recent_articles': recent_articles}


def category(request):
    categories = Category.objects.all()
    return {'categories': categories}