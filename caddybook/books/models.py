from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from sorl.thumbnail import ImageField
from geoposition.fields import GeopositionField
from geoposition import Geoposition
from geopy import distance, Point


class Course(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField()
    url = models.URLField(_('URL'), blank=True, null=True)
    active = models.BooleanField(_('Active'))
    description = models.TextField(_('Description'),
        blank=True, null=True)
    user = models.ForeignKey(User)
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def get_edit_url(self):
        if self.published:
            return reverse('books-course-edit', args=[
                self.slug])
        else:
            return reverse('books-user-course-edit', args=[
                self.user.username, self.slug])

    def get_absolute_url(self):
        if self.published:
            return reverse('books-course', args=[
                self.slug])
        else:
            return reverse('books-user-course', args=[
                self.user.username, self.slug])

    def create_holes(self, count):
        for x in range(1, count+1, 1):
            h = Hole()
            h.course = self
            h.par = 3
            h.position = x
            h.save()

    def has_map(self):
        if hasattr(self, '_has_map'):
            return self._has_map

        for h in self.hole_set.all():
            if not h.has_positions():
                return False

        return True

    @staticmethod
    def slugify_unique(slug):
        s = Course.objects.filter(slug=slug)
        if len(s) > 0:
            return Course.slugify_unique('%s-' % slug)

        return slug

class Hole(models.Model):
    course = models.ForeignKey(Course)
    position = models.PositiveSmallIntegerField(_('Position'))

    name = models.CharField(_('Name'), max_length=100,
        blank=True, null=True)

    # Coordinates fields for Tee and Basket
    tee_pos = GeopositionField(_('Tee position'))
    basket_pos = GeopositionField(_('Basket position'))

    # Misc
    distance = models.PositiveSmallIntegerField(
        _('Distance'), blank=True, null=True,
        help_text=_('Distance to basket in meters'))

    par = models.PositiveSmallIntegerField(
        _('Par'), blank=True, null=True)

    image = ImageField(upload_to='upload/hole-mainimages/',
        verbose_name=_('Image'), blank=True, null=True)

    description = models.TextField(
        _('Description'), blank=True, null=True)

    class Meta:
        ordering = ['position',]

    def get_absolute_url(self):
        if self.course.published:
            return reverse('books-hole',
                args=[self.course.slug,
                    self.position])
        else:
            return reverse('books-user-hole',
                args=[self.course.user.username,
                    self.course.slug,
                    self.position])

    def get_url_by_key(self, key):
        if self.course.published:
            url = 'books-%s' % key
            args = [self.course.slug, self.position]
        else:
            url = 'books-user-%s' % key
            args = [self.course.user.username,
                self.course.slug, self.position]

        return reverse(url, args=args)

    def get_edit_url(self):
        return self.get_url_by_key('hole-edit')

    def get_edit_position_url(self):
        return self.get_url_by_key('hole-edit-position')

    def get_edit_gallery_url(self):
        return self.get_url_by_key('hole-edit-gallery')

    def has_positions(self):
        if self.tee_pos.latitude != 0:
            if self.basket_pos.latitude != 0:
                return True

        return False

    def get_tee_lat(self):
        return '%s' % self.tee_pos.latitude

    def get_tee_lon(self):
        return '%s' % self.tee_pos.longitude

    def get_basket_lat(self):
        return '%s' % self.basket_pos.latitude

    def get_basket_lon(self):
        return '%s' % self.basket_pos.longitude

    def __unicode__(self):
        if self.name:
            return self.name

        return _('Unnamed')

    def has_next(self):
        if self.position < self.course.hole_set.count():
            return True

        return False

    def has_previous(self):
        if self.position > 1:
            return True

        return False

    def next_hole_position(self):
        return self.position + 1

    def next_hole_url(self):
        next_pos = self.next_hole_position()
        hole = self.course.hole_set.get(position=next_pos)
        return hole.get_absolute_url()

    def previous_hole_url(self):
        prev_pos = self.previous_hole_position()
        hole = self.course.hole_set.get(position=prev_pos)
        return hole.get_absolute_url()

    def previous_hole_position(self):
        return self.position - 1

    def gps_distance(self):
        if self.tee_pos.latitude is 0 or self.basket_pos.latitude == 0:
            return False

        p1 = Point(self.tee_pos.latitude, self.tee_pos.longitude)
        p2 = Point(self.basket_pos.latitude, self.basket_pos.longitude)
        d = distance.distance(p1, p2)

        return '%i' % d.meters


class HoleGalleryImage(models.Model):
    hole = models.ForeignKey(Hole)
    image = ImageField(upload_to='upload/hole-gallery/',
        verbose_name=_('Image'))
    description = models.CharField(_('Description'),
        max_length=255, blank=True, null=True)
