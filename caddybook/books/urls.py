from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
admin.autodiscover()

from caddybook.books.views import AboutView

urlpatterns = patterns('caddybook.books.views',
    url(r'^$', 'index', name='books-index'),
    url(_(r'^about/$'), AboutView.as_view(), name='books-about'),
    url(_(r'^courses/(?P<slug>[-\w]+)/$'), 'course', name='books-course'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/$'),
        'hole', name='books-hole'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/$'),
        'hole_edit', name='books-hole-edit'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/position/$'),
        'hole_edit_position', name='books-hole-edit-position'),
    url(_(r'^courses/(?P<slug>[-\w]+)/holes/(?P<position>\d+)/edit/gallery/$'),
        'hole_edit_gallery', name='books-hole-edit-gallery'),

    url(_(r'^profile/$'), 'profile', name='books-profile'),

    # Enable admin site
    url(r'^admin/', include(admin.site.urls)),

    # Enable views from registration app
    url(_(r'^accounts/'), include('caddybook.books.registration_urls')),

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
