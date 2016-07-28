from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'LandsBlog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^login_admin/', include(admin.site.urls)),
    url(r'', include('Blog.urls')),
    url(r'blog/', include('SelfBlog.urls')),
]
