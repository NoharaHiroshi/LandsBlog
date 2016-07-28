# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SelfBlog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='html_description',
            field=models.CharField(max_length=80, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='html_keywords',
            field=models.CharField(max_length=40, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='html_title',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
    ]
