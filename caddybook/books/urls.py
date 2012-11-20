from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('caddybook.books.views',
    url(r'^$', 'index', name='books-index'),
    url(r'^courses/(?P<slug>[-\w]+)/$', 'course', name='books-course'),
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/$',
        'hole', name='books-hole'),
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/$',
        'hole_edit', name='books-hole-edit'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': settings.MEDIA_ROOT,
                        'show_indexes': True}))
