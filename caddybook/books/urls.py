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
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/position/$',
        'hole_edit_position', name='books-hole-edit-position'),
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/gallery/$',
        'hole_edit_gallery', name='books-hole-edit-gallery'),


    # Enable admin site
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('caddybook.books.ajaxviews',
    # AJAX views
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/ajax/set-hole-geoposition/$',
        'set_hole_geoposition', name='books-ajax-set-hole-geoposition'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': settings.MEDIA_ROOT,
                        'show_indexes': True}))
