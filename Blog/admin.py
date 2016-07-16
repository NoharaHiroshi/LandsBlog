from django.contrib import admin
from .models import Blog, Category, Nav, Carousel, SiteUser, HotSpot, Tag
from django_markdown.admin import MarkdownModelAdmin


# Register your models here.

# —————————————————BlogAdmin——————————————————
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'blog_in_status', 'created', 'modified','read_times','top', 'id')
    search_fields = ('title', 'markdown_content')
    # 状态选择器
    list_filter = ('status', 'blog_in_status', 'owner', 'created', 'modified',)
    filter_horizontal = ('tags',)
    # 关联字段，slug会将title字段中的英文字符自动填充到slug字段
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_blog_public', 'change_blog_daily_status', 'change_blog_popular_status', 'change_blog_industry_status']

    def make_blog_public(self, request, queryset):
        # queryset参数为选中的Blog对象
        rows_updated = queryset.update(status=3)
        message_bit = "%s 篇文章" % rows_updated
        self.message_user(request, "%s 已成功标记为已发布状态." % message_bit)
    make_blog_public.short_description = u'修改选中文章为已发布状态'

    def change_blog_daily_status(self, request, queryset):
        # queryset参数为选中的Blog对象
        rows_updated = queryset.update(blog_in_status = 2)
        message_bit = "%s 篇文章" % rows_updated
        self.message_user(request, "%s 已成功移至每日热点" % message_bit)
    change_blog_daily_status.short_description = u'将选中文章移至每日热点'

    def change_blog_popular_status(self, request, queryset):
        # queryset参数为选中的Blog对象
        rows_updated = queryset.update(blog_in_status = 4)
        message_bit = "%s 篇文章" % rows_updated
        self.message_user(request, "%s 已成功移至每日热评" % message_bit)
    change_blog_popular_status.short_description = u'将选中文章移至每日热评'

    def change_blog_industry_status(self, request, queryset):
        # queryset参数为选中的Blog对象
        rows_updated = queryset.update(blog_in_status = 5)
        message_bit = "%s 篇文章" % rows_updated
        self.message_user(request, "%s 已成功移至业界动态" % message_bit)
    change_blog_industry_status.short_description = u'将选中文章移至业界动态'


# —————————————————CategoryAdmin——————————————————
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}
    list_display = ('label','slug')


# —————————————————TagAdmin——————————————————
class TagAdmin(admin.ModelAdmin):
    list_display = ('label',)
    prepopulated_fields = {'slug': ('label',)}


# —————————————————NavAdmin——————————————————
class NavAdmin(admin.ModelAdmin):
    search = ('name',)
    list_display = ('name', 'url','order', 'used',  'create_time')
    # 显示在admin中可以编辑的字段
    fields = ('name', 'url','order', 'used', 'create_time')


# —————————————————CarouselAdmin——————————————————
class CarouselAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'blog', 'img', 'create_time')
    list_filter = ('create_time',)
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug','blog', 'img', 'summary', 'create_time')

# —————————————————HotSpotAdmin——————————————————
class HotSpotAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'blog', 'img', 'create_time')
    list_filter = ('create_time',)
    fields = ('title', 'blog', 'img', 'summary', 'create_time')

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Nav, NavAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(HotSpot, HotSpotAdmin)
