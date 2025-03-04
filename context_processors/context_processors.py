from article.models import Article, Category


def recent_articles(request):
    return {
        'recent_articles': Article.objects.filter(published=True).order_by('-created')[:3]
    }

def category(request):
    categories = Category.objects.all()
    return {'categories': categories}