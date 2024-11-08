from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


#  login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect("login_view")
    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect("/")