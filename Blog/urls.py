from django.conf.urls import include, url
from Blog.views import IndexView, ArticalListView, ArticalView, TagListView, StatusListView, AboutMeView
from django.conf import settings

urlpatterns = [
      url(r'^$', IndexView.as_view(), name='index_view' ),
      url(r'^(?P<page>\d+)/', IndexView.as_view() ),
      url(r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
      url(r'^artical/(?P<info>\w*)$', ArticalListView.as_view(), name='artical_list_view' ),
      url(r'^artical/(?P<info>\w*)/(?P<page>\d+)/$', ArticalListView.as_view()),
      url(r'^status/(?P<status>\w*)$', StatusListView.as_view(), name='artical_list_view' ),
      url(r'^status/(?P<status>\w*)/(?P<page>\d+)/$', StatusListView.as_view()),
      url(r'^tag/(?P<info>\w*)$', TagListView.as_view(), name='Tag_list_view' ),
      url(r'^tag/(?P<info>\w*)/(?P<page>\d+)/$', TagListView.as_view()),
      url(r'^content/(?P<slug>.*)$', ArticalView.as_view(), name='artical'),
      url(r'^aboutme/', AboutMeView, name='aboutme_view' ),
]
