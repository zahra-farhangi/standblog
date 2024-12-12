from tkinter.font import names

from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('edit_profile/', views.user_edit, name='edit_profile')

]