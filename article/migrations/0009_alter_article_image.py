# Generated by Django 5.1.2 on 2025-02-16 05:23

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_alter_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[500, 500], upload_to='images/articles', verbose_name='عکس'),
        ),
    ]
