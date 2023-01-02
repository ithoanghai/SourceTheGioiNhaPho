import sys
from io import BytesIO
from PIL import Image
from django import forms
from django.forms import Textarea, ModelForm, BaseInlineFormSet, inlineformset_factory
from django.core.files.uploadedfile import InMemoryUploadedFile
from import_export.forms import ImportForm, ExportForm
from .models import Listing, ListingImage, ListingHistory, ContractImage
from django.utils.translation import gettext_lazy as _


class ImportForm(ImportForm):
    choices = [
        ('0', '---'),
        ('Database',  'Tệp sao lưu CSDL'),
        ('K1',  'CSV Nhà phố'),
        ('K2',  'CSV Thiên Khôi'),
    ]
    import_type = forms.ChoiceField(
        label=_('File Source Type'),
        choices=choices,
    )


class ExportForm(ExportForm):
    choices = choices = [
        ('0', '---'),
        ('Database',  'Sao lưu CSDL'),
        ('Facebook',  'CSV cho Facebook'),
    ]
    export_type = forms.ChoiceField(
        label=_('Export Type'),
        choices=choices,
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = (
        'transaction_type', 'house_type', 'state', 'district', 'ward', 'street', 'urban_area', 'address', 'title',
        'description', 'area', 'price', 'registration_type', 'bedrooms', 'bathrooms', 'floors', 'direction',
        'lane_width', 'width', 'furniture_design', 'regional_welfare')
        widgets = {
            'furniture_design': Textarea(attrs={'class': '???', 'rows': 3}),
            'regional_welfare': Textarea(attrs={'class': '???', 'rows': 3}),
            'expert_comments': Textarea(attrs={'class': '???', 'rows': 3}),
        }


    #district = AutoCompleteSelectField('districts', required=False, help_text=None)
    #ward = AutoCompleteSelectMultipleField('wards', required=False, help_text=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.fields['district'].queryset = None
        #self.fields['ward'].queryset = get_wards_by_district(self.district)
        #self.fields['ward'].widget = forms.Select()


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


ListingImageFormSet = inlineformset_factory(Listing, ListingImage, fields=('photo',), extra=5)


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
