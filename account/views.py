from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

#  login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:main')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:main')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect("account:login")
    return render(request, 'account/login.html')


def register_view(request):
    context = {"errors": []}
    if request.user.is_authenticated:
        return redirect('home:main')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            context['errors'].append("passwords don't match")
            return render(request, 'account/register.html', context)

        user =User.objects.create(username=username, email=email, password=password1)
        login(request, user)
        return redirect('home:main')
    return render(request, 'account/register.html', {})


def logout_view(request):
    logout(request)
    return redirect("home:main")