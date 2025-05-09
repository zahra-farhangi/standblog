# Generated by Django 5.1.2 on 2025-02-13 17:52

import django.utils.timezone
import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ انتشار'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=django_jalali.db.models.jDateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ بروز رسانی'),
        ),
        migrations.AlterField(
            model_name='article',
            name='updated',
            field=django_jalali.db.models.jDateTimeField(auto_now=True, null=True, verbose_name='تاریخ بروز رسانی'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='created_at',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ'),
        ),
    ]
