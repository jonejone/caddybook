from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from geoposition.fields import GeopositionField
from geopy import distance, Point


class Course(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    slug = models.SlugField()
    url = models.URLField(_('URL'), blank=True, null=True)
    active = models.BooleanField(_('Active'))
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


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
