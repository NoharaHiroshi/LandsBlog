# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='博客')),
                ('slug', models.SlugField(verbose_name='简短标题')),
                ('img', models.ImageField(upload_to='blog', default='blog/blog-default.jpg', verbose_name='blog图片')),
                ('summary', models.TextField(null=True, verbose_name='摘要', max_length=200, blank=True)),
                ('markdown_content', models.TextField(verbose_name='Markdown内容')),
                ('html_content', models.TextField(verbose_name='转换Html内容', editable=False)),
                ('status', models.IntegerField(choices=[(1, '草稿状态'), (2, '待批准状态'), (3, '已发布状态'), (4, '已存档')], default=1, verbose_name='发布状态')),
                ('blog_in_status', models.IntegerField(choices=[(1, '博客板块'), (2, '每日热点'), (3, '订阅内容'), (4, '每日热评'), (5, '业界动态'), (6, '推荐新闻'), (7, '轮播新闻'), (8, '热文')], default=1, verbose_name='Blog所属板块')),
                ('created', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('modified', models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间')),
                ('read_times', models.PositiveIntegerField(default=0, verbose_name='阅读次数')),
                ('top', models.BooleanField(default=False, verbose_name='是否推荐')),
            ],
            options={
                'ordering': ['-modified', '-created'],
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('slug', models.SlugField(verbose_name='简短标题')),
                ('summary', models.TextField(null=True, verbose_name='摘要', max_length=100, blank=True)),
                ('img', models.ImageField(upload_to='carousel', max_length=200, default='/carousel/default_slide.jpg', verbose_name='轮播图片')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('blog', models.ForeignKey(to='Blog.Blog', verbose_name='轮播文章')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=50, blank=True)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': '分类',
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='HotSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('summary', models.TextField(null=True, verbose_name='摘要', max_length=200, blank=True)),
                ('img', models.ImageField(upload_to='hotspot', max_length=200, default='/hotspot/default_hotspot.jpg', verbose_name='热点图片')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
                ('blog', models.ForeignKey(to='Blog.Blog', verbose_name='热点文章')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '热点新闻',
                'verbose_name_plural': '热点新闻',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=40, verbose_name='导航条内容')),
                ('url', models.CharField(null=True, verbose_name='指向地址', max_length=200, blank=True)),
                ('used', models.BooleanField(default=False, verbose_name='是否启用导航条')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='导航条排序')),
                ('create_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '导航条',
                'verbose_name_plural': '导航条',
            },
        ),
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('signature', models.CharField(max_length=32, default='这个家伙很懒，什么都没有留下', verbose_name='签名')),
                ('img', models.ImageField(upload_to='user', default='/user/default_user.jpg', verbose_name='头像')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=20, verbose_name='标签')),
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
            field=models.ForeignKey(to='Blog.Category', verbose_name='分类'),
        ),
        migrations.AddField(
            model_name='blog',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='发布者'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(to='Blog.Tag', verbose_name='标签'),
        ),
    ]
