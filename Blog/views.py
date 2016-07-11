from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.contenttypes.models import ContentType
from Blog.models import Blog, Nav, Carousel, Category, HotSpot, Tag
import logging
import django_comments

# logger
logger = logging.getLogger(__name__)

# —————————————————BaseMixiin——————————————————
class BaseMixin(object):
    # 重写get_context_data()，调用object的get_context_data(**kwarga)
    def get_context_data(self, *args, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            # 设置站点名称
            context['website_title'] = settings.WEBSITE_TITLE
            # 设置导航条
            context['nav_list'] = Nav.objects.filter(used=True)
            # 设置每日热点
            context['daily_list'] = Blog.objects.filter(blog_in_status=2).order_by('-created')[0:3]
            # 设置订阅内容
            context['rss_list'] = Blog.objects.filter(blog_in_status=3).order_by('-created')[0:6]
            # 设置每日热评
            context['daily_comment_list'] = Blog.objects.filter(blog_in_status=4).order_by('-created')[0:6]
            # 设置热点新闻
            context['hotspot'] = HotSpot.objects.all()[0:1]
            # 设置业界动态
            context['industry_news_list'] = Blog.objects.filter(blog_in_status=5).order_by('-created')[0:3]
            # 设置业界动态
            context['popular_list'] = Blog.objects.filter(blog_in_status=8).order_by('-created')[0:6]
            # 设置排行榜
            context['ranking_list'] = Blog.objects.all().order_by('-read_times')[0:10]
            # 设置分类列表
            context['category_list'] = Category.objects.all()
        except Exception as e:
            logger.error(u'加载基本信息(BaseMixin)出错')

        return context


# —————————————————IndexView——————————————————
class IndexView(BaseMixin, ListView):
    # 模板名称，默认为:应用名/类名_detail.html（即 app/modelname_list.html）对应t
    template_name = 'index.html'
    # 设置object_list别名blog_list
    context_object_name = 'blog_list'

    # 设置index.html的展示内容：站点名称、站点欢迎语、导航条、推荐列表、轮播图

    def get_context_data(self, **kwargs):
        kwargs['carousel_list'] = Carousel.objects.all()
        return super(IndexView, self).get_context_data(**kwargs)

    # 设置获取数据库对象story_list
    def get_queryset(self):
        # 获取Blog所有对象，以blog_list表示，用以template，原始的方式是queryset = Blog.objects.all()，以这种方式获取的Blog
        # 对象，会隐式的用object_list表示Blog对象列表，而context_object_name赋予object有意义的名字
        blog_list = Blog.objects.filter(top=True)
        return blog_list


# —————————————————ArticalListView——————————————————
class ArticalListView(BaseMixin, ListView):
    template_name = 'artical/artical_list.html'
    context_object_name = 'artical_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        category = self.kwargs.get('info','')
        page_num = self.kwargs.get('page','')
        artical_list_all = Category.objects.get(slug=category).blog_set.all().order_by('-created')
        paginator = Paginator(artical_list_all, self.paginate_by)
        try:
            kwargs['artical_category_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['artical_category_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['artical_category_list'] = paginator.page(paginator.num_pages)
        kwargs['category_name'] = Category.objects.get(slug = self.kwargs.get('info'))
        return super(ArticalListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        category = self.kwargs.get('info','')
        artical_list = Category.objects.get(slug=category).blog_set.all()
        return artical_list


# —————————————————TagListView——————————————————
class TagListView(BaseMixin, ListView):
    template_name = 'artical/tag_list.html'
    context_object_name = 'artical_list'
    paginate_by = settings.PAGE_NUM

    def get_context_data(self, **kwargs):
        tag = self.kwargs.get('info','')
        page_num = self.kwargs.get('page','')
        artical_list_all = Tag.objects.get(slug=tag).blog_set.all().order_by('-created')
        paginator = Paginator(artical_list_all, self.paginate_by)
        try:
            kwargs['artical_tag_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['artical_tag_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['artical_tag_list'] = paginator.page(paginator.num_pages)
        kwargs['tag_name'] = Tag.objects.get(slug = self.kwargs.get('info'))
        return super(TagListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        tag = self.kwargs.get('info','')
        artical_list = Tag.objects.get(slug=tag).blog_set.all()
        return artical_list


# —————————————————StatusListView——————————————————
class StatusListView(BaseMixin, ListView):
    template_name = 'artical/status_list.html'
    context_object_name = 'status_list'
    paginate_by = settings.PAGE_NUM

    status_id = {
        'rss' : 3,
        'daily_comment' : 4,
        'popular' : 8,
    }

    def get_context_data(self, **kwargs):
        status = self.kwargs.get('status','')
        status_id = self.status_id[status]
        page_num = self.kwargs.get('page','')
        artical_list_all =Blog.objects.filter(blog_in_status=status_id).order_by('-created')
        paginator = Paginator(artical_list_all, self.paginate_by)
        try:
            kwargs['artical_status_list'] = paginator.page(page_num)
        except PageNotAnInteger:
            kwargs['artical_status_list'] = paginator.page(1)
        except EmptyPage:
            kwargs['artical_status_list'] = paginator.page(paginator.num_pages)
        kwargs['status_name'] = {3 : '订阅内容', 4 :  '每日热评', 8 : '热文'}[status_id]
        return super(StatusListView, self).get_context_data(**kwargs)

    def get_queryset(self):
        status = self.kwargs.get('status')
        artical_list = Blog.objects.all()
        return artical_list


# —————————————————ArticalView——————————————————
class ArticalView(BaseMixin, DetailView):
    template_name = 'artical/artical.html'
    context_object_name = 'artical'
    slug_field = 'slug'
    queryset = Blog.objects.all()

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        try:
            artical = self.queryset.get(slug=slug)
        except Blog.DoesNotExist:
            logger.error(u'ArticalView访问不存在的文章：[%s]' %slug)
            raise Http404
        artical.read_times += 1
        artical.save()
        return super(ArticalView, self).get(request, *args, **kwargs)


# —————————————————sub_comment——————————————————
def sub_comment(request):
    if request.method == 'POST':
        artical_id = request.POST.get('artical_id')
        comment_content = request.POST.get('comment_content')
        slug =  request.POST.get('artical_slug')
        name = request.POST.get('artical_name')
        content_type_id = ContentType.objects.get(id=8)
        django_comments.models.Comment.objects.create(
                content_type = content_type_id,
                site_id = 1,
                object_pk = artical_id,
                comment = comment_content,
                user_name = name,
        )
        return HttpResponseRedirect('/content/%s' %slug)
