from django import forms
from django.forms import Textarea

from .models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        widgets = {
            'content': Textarea(attrs={'class': '???', 'rows': 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
