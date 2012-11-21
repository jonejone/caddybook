from django.forms import ModelForm
from caddybook.books.models import Hole, HoleGalleryImage

class HoleGalleryImageForm(ModelForm):
    class Meta:
        model = HoleGalleryImage
        exclude = ('hole',)

class HoleForm(ModelForm):
    class Meta:
        model = Hole


class HolePositionForm(ModelForm):
    class Meta:
        model = Hole
        fields = ('tee_pos', 'basket_pos')
