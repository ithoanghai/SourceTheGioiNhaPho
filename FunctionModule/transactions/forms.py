from django import forms
from django.forms import Textarea

from FunctionModule.listings import HouseType
from FunctionModule.transactions.models import Transaction


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

        widgets = {
            'message': Textarea(attrs={'class': '???', 'rows': 5}),
            'comment': Textarea(attrs={'class': '???', 'rows': 5}),
        }

class TransactionHistoryAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

        widgets = {
            'comment': Textarea(attrs={'class': '???', 'rows': 5}),
        }

class RequestQuoteForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10)
    email = forms.CharField(max_length=120, required=False)
    message = forms.CharField(max_length=2000)
    house_type = forms.CharField(required=False)
    district = forms.CharField(max_length=100, required=False)
    request_price = forms.DecimalField(max_digits=5, decimal_places=2, required=False)


class TransactionForm(forms.Form):
    house_type = forms.ChoiceField(choices=HouseType,required=False)


