from django import forms

from FunctionModule.cadastral.constants import district_data
from FunctionModule.cadastral.lookups import DistrictLookup
from .fields import EmptyChoiceField
from .models import Listing

district_default_choices = [('', 'Chọn quận/huyện')] + [(d['code'], d['name']) for d in district_data['01']]

class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'] = forms.ChoiceField(choices=district_default_choices, label="Quận/Huyện", required=True)
        self.fields['ward'] = EmptyChoiceField(empty_label="Chọn Quận/Huyện trước", required=False)


class ImportListingForm(forms.Form):
    file = forms.FileField(required=True)
