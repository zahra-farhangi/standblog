from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.forms.widgets import ClearableFileInput
from datetime import date
from django.contrib.auth.forms import PasswordChangeForm
import re


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'رمز عبور'}))

    def clean_password(self):
        user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
        if user is not None:
            return self.cleaned_data.get('password')
        raise ValidationError('نام کاربری یا رمز عبور اشتباه است', code='invalid_info')


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'input100', 'placeholder': 'نام کاربری'}),
                               label='Username')
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input100', 'placeholder': 'ایمیل'}), label='Email')
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'رمز عبور'}),
                                label='Password')
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'تکرار رمز عبور',}),
                                label='Confirm password')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check Username len
        if len(username) < 5:
            raise ValidationError('نام کاربری باید حداقل 5 کاراکتر باشد', code='Invalid_Username')

        # Check Username Unique
        if User.objects.filter(username=username).exists():
            raise ValidationError('نام کاربری از قبل وجود دارد', code='Username_Exists')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('ایمیل از قبل وجود دارد', code='Email_Exists')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Check Match Password
        if password1 and password2 and password1 != password2:
            self.add_error('password2', r"!پسورد یکسان نیست")

        # Check Characters Password
        if password1:
            if len(password1) < 8:
                self.add_error('password1', 'پسورد باید حداقل 8 کاراکتر باشد')
            if not re.search(r'[A-Z]', password1):
                self.add_error('password1', 'پسورد باید حداقل شامل یک حرف بزرگ انگلیسی باشد')
            if not re.search(r'[a-z]', password1):
                self.add_error('password1', 'پسورد باید حداقل شامل یک حرف کوچک انگلیسی باشد')
            if not re.search(r'[0-9]', password1):
                self.add_error('password1', 'پسورد باید حداقل شامل یک حرف عدد باشد')
        return cleaned_data

class UserProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'نام'}),
        label='نام'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'نام خانوادگی'}),
        label='نام خانوادگی'
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'formbold-form-input', 'placeholder': 'آدرس ایمیل'}),
        label='آدرس ایمیل'
    )
    bio = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'بیوگرافی'}),
        label='بیوگرافی'
    )
    phone_number = forms.CharField(
        max_length=11,
        required=False,
        widget=forms.TextInput(attrs={'class': 'formbold-form-input', 'placeholder': 'شماره همراه'}),
        label='شماره همراه'
    )
    birthday = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'formbold-form-input'}),
        label='تاریخ تولد'
    )
    image = forms.ImageField(
        required=False,
        widget=ClearableFileInput(attrs={'class': 'formbold-form-file'}),
        label='عکس پروفایل'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        profile_instance = kwargs.pop('profile_instance', None)
        super().__init__(*args, **kwargs)
        if profile_instance:
            self.fields['bio'].initial = profile_instance.Bio
            self.fields['phone_number'].initial = profile_instance.phone_number
            self.fields['birthday'].initial = profile_instance.birthday
            self.fields['image'].initial = profile_instance.image

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("ایمیل اجباری است.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number:
            raise forms.ValidationError("شماره همراه اجباری است.")
        if not phone_number.isdigit() or len(phone_number) != 11:
            raise forms.ValidationError("شماره همراه باید شامل 11 رقم باشد.")
        return phone_number

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday:
            if birthday >= date.today():
                raise ValidationError("تاریخ تولد باید قبل تر از تاریخ امروز باشد.")
        return birthday


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'formbold-form-input',
            'placeholder': 'رمز عبور فعلی',
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'formbold-form-input',
            'placeholder': 'رمز عبور جدید',
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'formbold-form-input',
            'placeholder': 'تأیید رمز عبور جدید',
        })
    )