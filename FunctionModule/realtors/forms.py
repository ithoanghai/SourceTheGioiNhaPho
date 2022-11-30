from django import forms
from django.forms import Textarea

from ..realtors.models import Realtor


class RealtorAdminForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = '__all__'

        widgets = {
            'story': Textarea(attrs={'class': '???', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImportRealtorForm(forms.Form):
    file = forms.FileField(required=True)
