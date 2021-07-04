from django import forms

from FunctionModule.cadastral.constants import district_data, ward_data
from .fields import EmptyChoiceField
from .models import Listing

district_default_choices = [(d['code'], d['name']) for d in district_data['01']]
ward_default_choices = [(d['code'], d['name']) for d in ward_data['008']]

class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'] = forms.ChoiceField(choices=district_default_choices, label="Quận/Huyện", required=True)
        # self.fields['ward'] = forms.ChoiceField(choices=ward_default_choices, label="Chọn phường/xã", required=True)
        # self.fields['ward'].widget = forms.Select()


class ImportListingForm(forms.Form):
    file = forms.FileField(required=True)
