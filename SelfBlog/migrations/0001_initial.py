# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='博客', max_length=100)),
                ('slug', models.SlugField(verbose_name='简短标题')),
                ('img', models.ImageField(verbose_name='blog图片', default='blog/blog-default.jpg', upload_to='blog')),
                ('summary', models.TextField(verbose_name='摘要', max_length=200, null=True, blank=True)),
                ('markdown_content', models.TextField(verbose_name='Markdown内容')),
                ('html_content', models.TextField(verbose_name='转换Html内容', editable=False)),
                ('status', models.IntegerField(verbose_name='发布状态', choices=[(1, '草稿状态'), (2, '待批准状态'), (3, '已发布状态'), (4, '已存档')], default=1)),
                ('created', models.DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)),
                ('modified', models.DateTimeField(verbose_name='修改时间', default=datetime.datetime.now)),
                ('read_times', models.PositiveIntegerField(verbose_name='阅读次数', default=0)),
                ('zan_times', models.PositiveIntegerField(verbose_name='打赏次数', null=True, default=0)),
                ('top', models.BooleanField(verbose_name='是否推荐', default=False)),
            ],
            options={
                'verbose_name': '博客',
                'verbose_name_plural': '博客',
                'ordering': ['-modified', '-created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(max_length=50, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='标签', max_length=20)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(verbose_name='分类', to='SelfBlog.Category'),
        ),
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(verbose_name='发布者', related_name='self_blog_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(verbose_name='标签', to='SelfBlog.Tag'),
        ),
    ]
