from django import forms


class RequestQuoteForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=10)
    email = forms.CharField(max_length=120, required=False)
    message = forms.CharField(max_length=2000)
    house_type = forms.CharField(required=False)
    district = forms.CharField(max_length=100, required=False)
    request_price = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
