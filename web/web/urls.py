from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', login, {"template_name":"admin/login.html", 'extra_context':{"title":"login"}}, name="login"),
    url(r'^logout/$', logout, {"next_page":"/login"}, name='logout'),
    url(r'^index/$', 'monitor.views.index'),
    url(r'^detail/(.+)/$', 'monitor.views.details'),
    url(r'^high/$', 'monitor.views.high'),
    url(r'^get_runtime/(.+)/$', 'monitor.views.get_runtime')
)
