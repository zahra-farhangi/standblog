from tkinter.font import names
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import CustomPasswordChangeForm
from django.urls import reverse_lazy

app_name = 'account'
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('edit_profile/', views.user_edit, name='edit_profile'),
    path('messages/', views.MessageListView.as_view(), name='message_list'),
    path(
        'password_change/',
        auth_views.PasswordChangeView.as_view(
            template_name='account/password_change.html',
            form_class=CustomPasswordChangeForm,
            success_url=reverse_lazy('account:password_change_done'),
        ),
        name='password_change'
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='account/password_change_done.html'
        ),
        name='password_change_done'
    ),
]
