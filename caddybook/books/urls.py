from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('caddybook.books.views',
    url(r'^$', 'index', name='books-index'),
    url(r'^courses/(?P<slug>[-\w]+)/$', 'course', name='books-course'),
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/$',
        'hole', name='books-hole'),
    url(r'^admin/', include(admin.site.urls)),
)
