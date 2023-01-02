from django import forms
from django.forms import Textarea
from import_export.forms import ImportForm, ExportForm
from django.utils.translation import gettext_lazy as _
from ..realtors.models import Realtor


class ImportForm(ImportForm):
    choices = [
        ('0', '---'),
        ('Database',  'File sao lưu CSDL'),
        ('Custom',  'File XLSX tùy chỉnh'),
    ]
    import_type = forms.ChoiceField(
        label=_('File Source Type'),
        choices=choices,
    )


class ExportForm(ExportForm):
    choices = choices = [
        ('0', '---'),
        ('Database',  'Sao lưu CSDL'),
        ('Custom',  'File XLSX tùy chỉnh'),
    ]
    export_type = forms.ChoiceField(
        label=_('Export Type'),
        choices=choices,
    )


class RealtorAdminForm(forms.ModelForm):
    class Meta:
        model = Realtor
        fields = '__all__'

        widgets = {
            'story': Textarea(attrs={'class': '???', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ImportRealtorForm(forms.Form):
    file = forms.FileField(required=True)
