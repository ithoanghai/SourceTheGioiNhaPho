from datetime import timedelta

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from .forms import RequestQuoteForm
from .models import Contact, RequestQuote
from ..listings.models import Listing


@csrf_protect
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        name = f'{firstname} {lastname}'
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST.get('user_id', None)
        yesterday = timezone.now() - timedelta(days=1)
        #  Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.filter(listing_id=listing_id, user_id=user_id,
                                                   contact_date__gte=yesterday)
            if has_contacted:
                messages.error(request,
                               'Bạn đã gửi yêu cầu tới chúng tôi về căn hộ này. Xin thử gửi lại yêu cầu sau.')
                return redirect('/listings/' + listing_id)
        else:
            ses_id = request.session.session_key
            print(ses_id)

        listing = Listing.objects.get(pk=listing_id)

        Contact.objects.create(listing=listing.code, listing_id=listing_id, name=name, email=email,
                               phone=phone, message=message, user_id=user_id)

        messages.success(request, 'Yêu cầu được gửi thành công. Chúng tôi sẽ liên lạc lại với bạn sớm nhất.')
        return redirect('/listings/' + listing_id)
        # return JsonResponse({})


@csrf_protect
def request_quote(request):
    form = RequestQuoteForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "error": form.errors
        }, status=400)
    lastname = form.cleaned_data.get('lastname')
    firstname = form.cleaned_data.get('firstname')
    name = f'{firstname} {lastname}'
    email = form.cleaned_data.get('email')
    phone = form.cleaned_data.get('phone')
    message = form.cleaned_data.get('message')
    house_type = form.cleaned_data.get('house_type')
    district = form.cleaned_data.get('district')
    request_price = form.cleaned_data.get('request_price')
    yesterday = timezone.now() - timedelta(days=1)
    #  Check if user has made inquiry already
    if request.user.is_authenticated:
        user_id = request.user.id
        has_contacted = RequestQuote.objects.filter(user_id=user_id, contact_date__gte=yesterday)
        if has_contacted:
            return JsonResponse({
                'message': 'Chúng tôi đã nhận được thông tin của quý khách và sẽ liên hệ lại trong thời gian sớm nhất.'
            })
    else:
        user_id = None

    RequestQuote.objects.create(name=name, email=email, phone=phone, message=message, house_type=house_type,
                                district=district, request_price=request_price, user_id=user_id)

    return JsonResponse(
        {
            'message': 'Chúng tôi đã nhận được thông tin của quý khách và sẽ liên hệ lại trong thời gian sớm nhất.'
        })
