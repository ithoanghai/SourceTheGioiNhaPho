from django.forms import forms, Media
from django.forms import Textarea, TextInput, EmailInput, NumberInput

from django.utils.translation import gettext_lazy as _


class RangeNumericForm(forms.Form):
    name = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super().__init__(*args, **kwargs)

        self.fields[self.name + '_from'] = forms.Field(label='', required=False,
            widget=NumberInput(attrs={'placeholder': _('Từ')}))
        self.fields[self.name + '_to'] = forms.Field(label='', required=False,
            widget=NumberInput(attrs={'placeholder': _('Đến')}))

    @property
    def media(self):
        return super().media + Media(css=[self.NUMERIC_FILTER_CSS])


class SliderNumericForm(RangeNumericForm):
    pass