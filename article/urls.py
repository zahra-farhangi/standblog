from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    # path('detail/<slug>/<int:id>/', views.article_detail, name='article_detail'),
    path('list/', views.ArticleListView.as_view(), name='articles_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search_articles'),
    path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('red/<slug>/<int:id>/', views.HomePageRedirect.as_view(), name='redirect'),
    path('detail/<slug>/<int:id>/', views.ArticleDetailView.as_view(), name='article_detail'),

]
