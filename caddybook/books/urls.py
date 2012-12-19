from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
admin.autodiscover()

from caddybook.books.classviews import (CourseView,
                                        HoleView,
                                        EditHoleView,
                                        EditHoleGalleryView,
                                        EditHolePositionView)
from caddybook.books.views import AboutView


urlpatterns = patterns('caddybook.books.views',
    url(r'^$', 'index', name='books-index'),
    url(_(r'^about/$'), AboutView.as_view(), name='books-about'),
    url(_(r'^courses/(?P<slug>[-\w]+)/$'), CourseView.as_view(), name='books-course'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/$'),
        HoleView.as_view(), name='books-hole'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/$'),
        EditHoleView.as_view(), name='books-hole-edit'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/position/$'),
        EditHolePositionView.as_view(), name='books-hole-edit-position'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/gallery/$'),
        EditHoleGalleryView.as_view(), name='books-hole-edit-gallery'),

    url(_(r'^profile/$'), 'profile', name='books-profile'),

    # Enable admin site
    url(r'^admin/', include(admin.site.urls)),

    # Enable views from registration app
    url(_(r'^accounts/'), include('caddybook.books.registration_urls')),

    # Add our own account views
    url(_(r'^accounts/create-course/$'),
        'create_course', name='books-createcourse'),
)

# User views
urlpatterns += patterns('caddybook.books.userviews',
    url(_(r'^users/(?P<username>[-\w]+)/courses/(?P<slug>[-\w]+)/$'),
        CourseView.as_view(), name='books-user-course'),

    url(_(r'^users/(?P<username>[-\w]+)/courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/$'),
        HoleView.as_view(), name='books-user-hole'),

    url(_(r'^users/(?P<username>[-\w]+)/courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/$'),
        EditHoleView.as_view(), name='books-user-hole-edit'),

    url(_(r'^users/(?P<username>[-\w]+)/courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/gallery/$'),
        EditHoleGalleryView.as_view(), name='books-user-hole-edit-gallery'),

    url(_(r'^users/(?P<username>[-\w]+)/courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/position/$'),
        EditHolePositionView.as_view(), name='books-user-hole-edit-position'),
)

# AJAX views
urlpatterns += patterns('caddybook.books.ajaxviews',
    url(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/ajax/set-hole-geoposition/$',
        'set_hole_geoposition', name='books-ajax-set-hole-geoposition'),
)

# Turn on static file serving while on devserver
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                        'document_root': settings.MEDIA_ROOT,
                        'show_indexes': True}))
