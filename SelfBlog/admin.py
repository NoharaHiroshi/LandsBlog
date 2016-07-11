from django.contrib import admin
from .models import Blog, Category, Tag

# Register your models here.

# —————————————————BlogAdmin——————————————————
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'created', 'modified','read_times','top', 'id')
    search_fields = ('title', 'markdown_content')
    # 状态选择器
    list_filter = ('status', 'category', 'tags', 'created', 'modified', 'created')
    # 关联字段，slug会将title字段中的英文字符自动填充到slug字段
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_blog_public']

    def make_blog_public(self, request, queryset):
        # queryset参数为选中的Story对象
        rows_updated = queryset.update(status=3)
        message_bit = "%s 篇博客" % rows_updated
        self.message_user(request, "%s 已成功标记为已发布状态." % message_bit)
    make_blog_public.short_description = u'修改选中博客为已发布状态'


# —————————————————CategoryAdmin——————————————————
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('label',)}
    list_display = ('label','slug')


# —————————————————TagAdmin——————————————————
class TagAdmin(admin.ModelAdmin):
    list_display = ('label',)
    prepopulated_fields = {'slug': ('label',)}


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)