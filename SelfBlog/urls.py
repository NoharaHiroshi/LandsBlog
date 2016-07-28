from django.conf.urls import include, url
from SelfBlog.views import IndexView, BlogView, TagListView, CategoryListView
from django.conf import settings

urlpatterns = [
      url(r'^$', IndexView.as_view(), name='blog'),
      url(r'(?P<page>\d+)$', IndexView.as_view()),
      url(r'upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
      url(r'content/(?P<slug>.*)$', BlogView.as_view(), name='blog'),
      url(r'tag/(?P<tag>\w*)$', TagListView.as_view(), name='Tag_list_view' ),
      url(r'tag/(?P<tag>\w*)/(?P<page>\d+)/$', TagListView.as_view()),
      url(r'category/(?P<category>\w*)$', CategoryListView.as_view(), name='Category_list_view' ),
      url(r'category/(?P<category>\w*)/(?P<page>\d+)/$', CategoryListView.as_view()),
]
