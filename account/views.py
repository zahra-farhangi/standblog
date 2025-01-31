from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required

from .models import Profile


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
            # اطلاعات کاربر از فرم ثبت‌نام
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            # ایجاد کاربر جدید
            user = User.objects.create_user(username=username, email=email, password=password)
            # ایجاد پروفایل مرتبط با کاربر
            Profile.objects.create(user=user)

            # لاگین کاربر
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

@login_required(login_url='account:login')
def user_edit(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, request.FILES, instance=user, profile_instance=profile)
        if form.is_valid():
            # ذخیره داده‌های کاربر
            user_form = form.save(commit=False)
            user_form.save()

            # ذخیره داده‌های پروفایل
            profile.Bio = form.cleaned_data.get('bio')
            profile.phone_number = form.cleaned_data.get('phone_number')
            profile.birthday = form.cleaned_data.get('birthday')

            # ذخیره عکس
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد.')
            return redirect('account:edit_profile')
        else:
            messages.error(request, 'مشکلی در ذخیره اطلاعات وجود دارد!')
    else:
        form = UserProfileEditForm(instance=user, profile_instance=profile)

    return render(request, 'account/edit_profile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect("home:main")
