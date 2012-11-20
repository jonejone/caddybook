from django.forms import ModelForm
from caddybook.books.models import Hole

class HoleForm(ModelForm):
    class Meta:
        model = Hole
