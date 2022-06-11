from django import forms

from ..realtors.models import Realtor


class RealtorAdminForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = '__all__'

        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImportRealtorForm(forms.Form):
    file = forms.FileField(required=True)
