from django import forms
from django.forms import Textarea

from .models import HitCount


class HitcountAdminForm(forms.ModelForm):
    class Meta:
        model = HitCount
        fields = '__all__'

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
