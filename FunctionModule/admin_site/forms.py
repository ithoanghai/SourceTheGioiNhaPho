from django.core.exceptions import ValidationError
from django.forms import forms, Media

from django.utils.translation import gettext_lazy as _


class RangeNumericForm(forms.Form):
    name = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super().__init__(*args, **kwargs)

        self.fields[self.name + '_from'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('From')}))
        self.fields[self.name + '_to'] = forms.FloatField(label='', required=False,
            widget=forms.NumberInput(attrs={'placeholder': _('To')}))

    @property
    def media(self):
        return super().media + Media(css=[self.NUMERIC_FILTER_CSS])


class SliderNumericForm(RangeNumericForm):
    pass