from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from markdown import markdown
from markdown import markdown
import datetime

# Create your models here.

VIEWABLE_STATUS = [3,4]
# 实例化manager对象
class ViewableManager(models.Manager):
    def get_queryset(self):
        #  调用父类的方法，在原来返回的QuerySet的基础上返回新的QuerySet
        default_queryset = super(ViewableManager, self).get_queryset()
        return default_queryset.filter(status__in = VIEWABLE_STATUS)


# —————————————————Tag——————————————————
class Tag(models.Model):
    label = models.CharField(max_length=20, verbose_name=u'标签' )
    slug = models.SlugField()

    class Meta:
        verbose_name_plural = verbose_name = u'标签'

    def __str__(self):
        return self.label


# —————————————————Category——————————————————
class Category(models.Model):
    label = models.CharField(blank=True, max_length=50)
    slug = models.SlugField()
    html_title = models.CharField(blank=True, null=True, max_length=20)
    html_description = models.CharField(blank=True, null=True, max_length=80)
    html_keywords = models.CharField(blank=True, null=True, max_length=40)

    class Meta:
        verbose_name_plural = verbose_name =  '分类'

    def __str__(self):
        return self.label


# —————————————————Blog——————————————————
class Blog(models.Model):
    #A hunk of content for our site, generally corresponding to a page

    #编辑Blog状态
    STATUS_CHOICES = (
        (1, '草稿状态'),
        (2, '待批准状态'),
        (3, '已发布状态'),
        (4, '已存档'),
    )


    # 浏览器的标题栏和渲染页面上显示的标题
    title = models.CharField(max_length=100, verbose_name=u'博客')
    # 页面在url里的唯一的名字
    slug = models.SlugField(verbose_name=u'简短标题')
    # 文章的类别，指向Category的一对多的外键
    category =models.ForeignKey(Category, verbose_name=u'分类')
    # 设置Blog图片
    img = models.ImageField(upload_to='blog', verbose_name=u'blog图片', default='blog/blog-default.jpg')
    # 文章内容摘要
    summary = models.TextField(blank=True, null=True, verbose_name=u'摘要',max_length=200)
    # Markdown格式的页面正文
    markdown_content = models.TextField(verbose_name=u'Markdown内容')
    # HTML格式的页面文本，编辑时自动渲染，为了避免和Markdown编辑混淆，禁止编辑
    html_content = models.TextField(editable=False, verbose_name=u'转换Html内容')
    # 拥有这个内容的admin用户：指向User的一对多的外键
    owner = models.ForeignKey(User, verbose_name=u'发布者', related_name=u'self_blog_user')
    # 编辑Blog状态，默认为待编辑状态
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name=u'发布状态')
    # Blog创建的时间，自动设置当前时间
    created = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'创建时间')
    # Blog最后一次修改的时间
    modified = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'修改时间')
    # Blog阅读次数
    read_times = models.PositiveIntegerField(verbose_name=u'阅读次数', default=0)
    # Blog打赏次数
    zan_times = models.PositiveIntegerField(verbose_name=u'打赏次数', default=0, null=True)
    # Blog设置推荐
    top = models.BooleanField(verbose_name=u'是否推荐', default=False)
    # 文章标签
    tags = models.ManyToManyField(Tag, verbose_name=u'标签')

    def save(self, *args, **kwargs):
        self.html_content = markdown(self.markdown_content)
        self.modified = datetime.datetime.now()
        super(Blog, self).save( *args, **kwargs)


    class Meta:
        ordering = ['-modified','-created']
        verbose_name_plural = verbose_name = '博客'


    def get_absolute_url(self):
        return reverse('blog', args=(self.slug,))

    admin_objects = models.Manager() # 默认管理器
    objects = ViewableManager()

    def __str__(self):
        return self.title


