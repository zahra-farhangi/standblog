from django import template
from ..models import Article, Comment

register = template.Library()

@register.simple_tag()
def total_articles():
    return Article.objects.count()


@register.simple_tag()
def total_comments(article_id):
    return Comment.objects.filter(article_id=article_id).count()