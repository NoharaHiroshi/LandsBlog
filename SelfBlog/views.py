from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
from SelfBlog.models import Blog, Category, Tag
from Blog.models import Nav
import logging
import django_comments

logger = logging.getLogger(__name__)

# —————————————————BaseMixiin——————————————————
class BaseMixin(object):
    # 重写get_context_data()，调用object的get_context_data(**kwarga)
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 设置站点域名
            context['website_url'] = settings.WEBSITE_URL
            # 设置导航列表
            context['nav_list'] = Nav.objects.all()
            # 设置博客列表
            context['blog_list'] = Blog.objects.all().order_by('-created')
            # 设置阅读排行
            context['read_list'] = Blog.objects.all().order_by('-read_times')[0:5]
            # 设置推荐阅读
            context['recommend'] = Blog.objects.filter(top=True ).order_by('-created')[0:5]
            # 设置博客列表
            context['category'] = Category.objects.all()
            # 设置博客云标签
            context['tag'] = Tag.objects.all()
        except Exception as e:
            logger.error(u'加载基本信息(BaseMixin)出错')

        return context


# —————————————————IndexView——————————————————
class IndexView(BaseMixin, ListView):
    template_name = 'blog_index.html'
    context_object_name = 'blog_list'
    paginate_by = settings.PAGE_NUM

    def get_queryset(self):
        blog_list = Blog.objects.all()
        return blog_list

    def get_context_data(self, **kwargs):
        page_num = self.kwargs.get('page','')
        blog_list_all = Blog.objects.all().order_by('-created')
        paginator = Paginator(blog_list_all, self.paginate_by)
        try:
            kwargs['blog_all_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['blog_all_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['blog_all_list'] = paginator.page(paginator.num_pages)
        return super(IndexView, self).get_context_data(**kwargs)

# —————————————————BlogView——————————————————
class BlogView(BaseMixin, DetailView):
    template_name = 'blog/blog.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            blog = self.queryset.get(slug=slug)
        except Blog.DoesNotExist:
            logger.error(u'BlogView访问不存在的文章：[%s]' %slug)
            raise Http404
        blog.read_times += 1
        blog.save()
        return super(BlogView, self).get(request, *args, **kwargs)


# —————————————————TagListView——————————————————
class TagListView(BaseMixin, ListView):
    template_name = 'blog/blog_tag_list.html'
    context_object_name = 'blog_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        tag = self.kwargs.get('tag','')
        page_num = self.kwargs.get('page','')
        blog_list_all = Tag.objects.get(slug=tag).blog_set.all().order_by('-created')
        paginator = Paginator(blog_list_all, self.paginate_by)
        try:
            kwargs['blog_tag_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['blog_tag_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['blog_tag_list'] = paginator.page(paginator.num_pages)
        kwargs['tag_name'] = Tag.objects.get(slug = self.kwargs.get('tag'))
        return super(TagListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        tag = self.kwargs.get('tag','')
        blog_list = Tag.objects.get(slug=tag).blog_set.all()
        return blog_list

# —————————————————CategoryListView——————————————————
class CategoryListView(BaseMixin, ListView):
    template_name = 'blog/blog_category_list.html'
    context_object_name = 'blog_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        category = self.kwargs.get('category','')
        page_num = self.kwargs.get('page','')
        blog_category_all = Category.objects.get(slug=category).blog_set.all().order_by('-created')
        paginator = Paginator(blog_category_all, self.paginate_by)
        try:
            kwargs['blog_category_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['blog_category_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['blog_category_list'] = paginator.page(paginator.num_pages)
        kwargs['category_name'] = Category.objects.get(slug = self.kwargs.get('category'))
        return super(CategoryListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        tag = self.kwargs.get('category','')
        blog_list = Category.objects.get(slug=tag).blog_set.all()
        return blog_list
