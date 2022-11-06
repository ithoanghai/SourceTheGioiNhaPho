import sys
from io import BytesIO

from PIL import Image
from django import forms
from django.forms import Textarea, ModelForm, BaseInlineFormSet
from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Listing, ListingImage, ListingHistory, ContractImage


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
            'extra_data': Textarea(attrs={'class': '???', 'rows': 12}),
        }

    # users_list = User.objects.values_list('last_name',flat=True).order_by('last_name').distinct()
    # choice_list = []
    # for rel in users_list:
    #     choice_list.append((rel, rel))
    # USER_CHOICES = choice_list
    #
    # # Used 'ChoiceField' as you want dropdown list for carmodels stored in text fields
    # title = forms.ChoiceField(widget=forms.Select, choices=USER_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ward'].widget = forms.Select()
        #self.fields['realtor'].disabled = False


class ListingHistoryAdminForm(forms.ModelForm):
    class Meta:
        model = ListingHistory
        fields = '__all__'

        widgets = {

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImportListingForm(forms.Form):
    file = forms.FileField(required=True)


class ImageForm(ModelForm):
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ListingImage
        fields = ['photo', ]
        #fields = '__all__'


class ContractImageForm(ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = ContractImage
        fields = ['image', ]
        #fields = '__all__'


TOTAL_FORM_COUNT = 'TOTAL_FORMS'
INITIAL_FORM_COUNT = 'INITIAL_FORMS'
MIN_NUM_FORM_COUNT = 'MIN_NUM_FORMS'
MAX_NUM_FORM_COUNT = 'MAX_NUM_FORMS'


class ImageFormSet(BaseInlineFormSet):
    form = ImageForm

    def save_new_objects(self, commit=True):
        try:
            files = self.files.getlist('listingimage_set')
            for f in files:  # type: InMemoryUploadedFile
                new_img = compress_image(f)
                ListingImage(photo=new_img, listing=self.instance).save()
        except AttributeError:
            pass

        return super().save_new_objects(commit)


class ContractImageFormSet(BaseInlineFormSet):
    form = ContractImageForm

    def save_new_objects(self, commit=True):
        try:
            files = self.files.getlist('contractimage_set')
            for f in files:  # type: InMemoryUploadedFile
                new_img = compress_image(f)
                ContractImage(image=new_img, listing=self.instance).save()
        except AttributeError:
            pass

        return super().save_new_objects(commit)


def compress_image(f: InMemoryUploadedFile):
    if 'png' in f.content_type.lower():
        image_type = 'PNG'
    else:
        image_type = 'JPEG'

    img = Image.open(f.file)
    output = BytesIO()
    #if f.size > 3029237:
    quality = 25

    img.save(output, image_type, quality=quality)
    output.seek(0)
    new_name = f"{f.name.split('.')[0]}.{image_type.lower()}"
    new_img = InMemoryUploadedFile(output, 'ImageField', new_name, f.content_type,
                                   sys.getsizeof(output), None, f.content_type_extra)
    return new_img
