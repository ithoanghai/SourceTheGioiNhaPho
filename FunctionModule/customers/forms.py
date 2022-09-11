import sys
from django import forms
from django.forms import Textarea, ModelForm, BaseInlineFormSet

from .models import Customer


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'description': Textarea(attrs={'class': '???', 'rows': 12}),
            'request': Textarea(attrs={'class': '???', 'rows': 10}),
            'listing_watched': Textarea(attrs={'class': '???', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['ward'].widget = forms.Select()
        #self.fields['realtor'].disabled = False
