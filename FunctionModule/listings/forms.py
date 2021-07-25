from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import Textarea, ModelForm, BaseInlineFormSet

from FunctionModule.cadastral.constants import district_data, ward_data
from .models import Listing, ListingImage

district_default_choices = [(d['code'], d['name']) for d in district_data['01']]
ward_default_choices = [(d['code'], d['name']) for d in ward_data['008']]


class ListingAdminForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

        widgets = {
            'description': Textarea(attrs={'class': '???', 'rows': 12}),
            'salient_features': Textarea(attrs={'class': '???', 'rows': 5}),
            'location_advantage': Textarea(attrs={'class': '???', 'rows': 3}),
            'furniture_design': Textarea(attrs={'class': '???', 'rows': 3}),
            'living_facilities': Textarea(attrs={'class': '???', 'rows': 3}),
            'residential_community': Textarea(attrs={'class': '???', 'rows': 3}),
            'regional_welfare': Textarea(attrs={'class': '???', 'rows': 3}),
            'extra_data': Textarea(attrs={'class': '???', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'] = forms.ChoiceField(choices=district_default_choices, label="Quận/Huyện",
                                                    required=True)
        # self.fields['ward'] = forms.ChoiceField(choices=ward_default_choices, label="Chọn phường/xã", required=True)
        # self.fields['ward'].widget = forms.Select()


class ImportListingForm(forms.Form):
    file = forms.FileField(required=True)


class ImageForm(ModelForm):
    photo = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ListingImage
        fields = ['photo', ]
        # fields = '__all__'


TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'

class ImageFormSet(BaseInlineFormSet):
    form = ImageForm

    def save_new_objects(self, commit=True):
        try:
            files = self.files.getlist('listingimage_set')
            # image/png
            # image/jpeg
            for f in files: # type: InMemoryUploadedFile
                # print(f.content_type)
                ListingImage(photo=f, listing=self.instance).save()
        except AttributeError:
            pass
            
        return super().save_new_objects(commit)