from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm


#  login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home:main')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, username=form.cleaned_data.get('username'))
            login(request, user)
            return redirect("home:main")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # user = authenticate(request, username=username, password=password)
    # if user is not None:
    #     login(request, user)
    #     return redirect('home:main')
    # else:
    #     messages.warning(request, 'Invalid username or password')
    #     return redirect("account:login")


def register_view(request):
    # context = {"errors": []}
    if request.user.is_authenticated:
        return redirect('home:main')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Account was created successfully!')
            return redirect('home:main')

        return render(request, 'account/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})


#     username = request.POST.get('username')
#     email = request.POST.get('email')
#     password1 = request.POST.get('password1')
#     password2 = request.POST.get('password2')
#     if password1 != password2:
#         context['errors'].append("passwords don't match")
#         return render(request, 'account/register.html', context)
#
#     user =User.objects.create(username=username, email=email, password=password1)
#     login(request, user)
#     return redirect('home:main')
# return render(request, 'account/register.html', {})


def logout_view(request):
    logout(request)
    return redirect("home:main")
