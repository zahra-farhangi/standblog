from django.urls import path
from . import views


app_name = 'article'
urlpatterns = [
    path('detail/<int:pk>', views.post_detail, name='article_detail')
]