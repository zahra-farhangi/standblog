from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="نام کاربر ")
    Bio = models.TextField(verbose_name='بیوگرافی ', blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='شماره همراه ')
    birthday = jmodels.jDateField(blank=True, null=True, verbose_name='تاریخ تولد ')
    join_date = jmodels.jDateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='تاریخ عضویت')
    image = models.ImageField(upload_to='profiles/image', blank=True, null=True, verbose_name="عکس ")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'حساب کاربری'
        verbose_name_plural = 'حساب های کاربری'
