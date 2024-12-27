from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    # path('detail/<slug>/<int:id>/', views.article_detail, name='article_detail'),
    path('list/', views.ArticleListView.as_view(), name='articles_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search_articles'),
    # path('contact_us/', views.ContactUsView.as_view(), name='contact_us'),
    path('contact_us/', views.MessageView.as_view(), name='contact_us'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('red/<slug>/<int:id>/', views.HomePageRedirect.as_view(), name='redirect'),
    path('detail/<slug>/<int:id>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path('message/edit/<int:pk>', views.MessageUpdateView.as_view(), name='message_edit'),
    path('messaage/delete/<int:pk>', views.MessageDeleteView.as_view(), name='message_delete'),
    path('archive/', views.ArchiveIndexArticleView.as_view(), name='archive'),
    path('archive/<int:year>/', views.YearArchiveArticleView.as_view(), name='year_archive'),

]
