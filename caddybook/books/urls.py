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
                                        EditCourseView,
                                        EditHolePositionView)
from caddybook.books.views import AboutView


urlpatterns = patterns('caddybook.books.views',
    url(r'^$', 'index', name='books-index'),
    url(_(r'^about/$'), AboutView.as_view(), name='books-about'),
    url(_(r'^profile/$'), 'profile', name='books-profile'),

    # Enable admin site
    url(r'^admin/', include(admin.site.urls)),

    # Enable views from registration app
    url(_(r'^accounts/'), include('caddybook.books.registration_urls')),

    # Add our own account views
    url(_(r'^accounts/create-course/$'),
        'create_course', name='books-createcourse'),
)

# Course management views

course_base = _('courses/(?P<slug>[-\w]+)/')
hole_base = _('holes/(?P<position>\d+)/')
course_and_hole = '%s%s' % (unicode(course_base), unicode(hole_base))

urlpatterns += patterns('',
    url(r'^%s$' % unicode(course_base),
        CourseView.as_view(), name='books-course'),

    url(r'^%s%s$' % (unicode(course_base), _('edit/')),
        EditCourseView.as_view(), name='books-course-edit'),

    url(r'^%s$' % (course_and_hole),
        HoleView.as_view(), name='books-hole'),

    url(r'^%s%s$' % (course_and_hole, _('edit/')),
        EditHoleView.as_view(), name='books-hole-edit'),

    url(r'^%s%s$' % (course_and_hole, _('edit/position/')),
        EditHolePositionView.as_view(), name='books-hole-edit-position'),

    url(r'^%s%s$' % (course_and_hole, _('edit/gallery/')),
        EditHoleGalleryView.as_view(), name='books-hole-edit-gallery'),
)

# User views
user_base = _('users/(?P<username>[-\w]+)/')

user_course_base = ''.join([
    unicode(user_base), unicode(course_base)])

user_course_hole_base = ''.join([
    user_course_base, unicode(hole_base)])

urlpatterns += patterns('caddybook.books.userviews',
    url(r'^%s$' % (user_course_base),
        CourseView.as_view(), name='books-user-course'),

    url(r'^%s%s$' % (user_course_base, _('edit/')),
        EditCourseView.as_view(), name='books-user-course-edit'),

    url(r'^%s$' % (user_course_hole_base), HoleView.as_view(),
        name='books-user-hole'),

    url(r'^%s%s$' % (user_course_hole_base, _('edit/')),
        EditHoleView.as_view(), name='books-user-hole-edit'),

    url(r'^%s%s$' % (user_course_hole_base, _('edit/gallery/')),
        EditHoleGalleryView.as_view(),
        name='books-user-hole-edit-gallery'),

    url(r'^%s%s$' % (user_course_hole_base, _('edit/position/')),
        EditHolePositionView.as_view(),
        name='books-user-hole-edit-position'),
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
