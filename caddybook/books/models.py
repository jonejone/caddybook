from django.db import models
from django.utils.translation import ugettext_lazy as _


class Course(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    url = models.URLField(blank=True, null=True)
    active = models.BooleanField()

    def __unicode__(self):
        return self.name


class Hole(models.Model):
    course = models.ForeignKey(Course)
    position = models.PositiveSmallIntegerField()

    name = models.CharField(max_length=100,
        blank=True, null=True)

    # Coordinates for the Teebox
    tee_lat = models.FloatField(_('Latitude'),
        blank=True, null=True)

    tee_lon = models.FloatField(_('Longitude'),
        blank=True, null=True)

    # Coordinates for the basket
    basket_lat = models.FloatField(_('Latitude'),
        blank=True, null=True)

    basket_lon = models.FloatField(_('Longitude'),
        blank=True, null=True)

    # Misc
    length = models.PositiveSmallIntegerField(
        blank=True, null=True)

    par = models.PositiveSmallIntegerField(
        blank=True, null=True)

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
