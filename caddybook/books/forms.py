from django import forms
from geoposition.fields import GeopositionField
from geoposition import Geoposition
from caddybook.books.models import Hole, HoleGalleryImage, Course
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('published', 'user', 'slug')


class CreateCourseForm(forms.ModelForm):
    hole_count = forms.IntegerField(
        label=_('Hole count'), initial=18)

    class Meta:
        model = Course
        fields = ('name',)



class HoleGalleryImageForm(forms.ModelForm):
    class Meta:
        model = HoleGalleryImage
        exclude = ('hole',)


class HoleForm(forms.ModelForm):
    class Meta:
        model = Hole
        exclude = ('tee_pos', 'basket_pos', 'course')


class HolePositionForm(forms.ModelForm):
    class Meta:
        model = Hole
        fields = ('tee_pos', 'basket_pos')


class HolePositionFormAjax(forms.Form):
    lat = forms.CharField()
    lon = forms.CharField()
    field_id = forms.CharField()

    def __init__(self, *kargs, **kwargs):
        if kwargs.get('hole'):
            self.hole = kwargs.get('hole')
            del kwargs['hole']

        super(HolePositionFormAjax, self).__init__(*kargs, **kwargs)

    def save(self):
        data = self.cleaned_data

        if data['field_id'] not in ['basket_pos', 'tee_pos']:
            raise Exception(
                'Field %s not in accepted fields' % data['field_id'])

        pos = Geoposition(data['lat'], data['lon'])
        setattr(self.hole, data['field_id'], pos)
        self.hole.save()

        return self.hole
