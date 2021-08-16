from django.contrib import messages
from django.core.mail.backends import console
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import RequestQuoteForm
from .models import TransTypeInit
from .serializers import *
from ..accounts.models import User
from ..listings.models import Listing


@csrf_protect
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        trantype = TransTypeInit.CONTACT

        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        name = f'{firstname} {lastname}'
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        yesterday = timezone.now() - timedelta(days=1)

        if listing_id != '':
            listing = Listing.objects.get(pk=listing_id)
            if request.user.is_authenticated:
                user = request.user
            if listing is not None:
                if user is not None:
                    has_contacted = Transaction.objects.filter(listing=listing, user=user, date__gte=yesterday)
                    if has_contacted:
                        messages.error(request, 'Bạn đã gửi yêu cầu tới chúng tôi về căn hộ này. Xin thử gửi lại yêu cầu sau.')
                    else:
                        # user = User.objects.create(name=name, email=email, phone=phone)
                        Transaction.objects.create(listing=listing, user=user, trantype=trantype, message=message)
                        messages.error(request, 'Bạn đã gửi yêu cầu thành công tới chúng tôi về BĐS %s.' % (listing.code))
                else:
                    # user = User.objects.create(name=name, email=email, phone=phone)
                    Transaction.objects.create(listing=listing, trantype=trantype, message=message)
                    messages.error(request,'Bạn đã gửi yêu cầu thành công tới chúng tôi về BĐS %s.' % (listing.code))
            return redirect('/listings/' + listing_id)
        else:
            if request.user.is_authenticated:
                user = request.user
                if user is not None:
                    Transaction.objects.create(user=user, trantype=trantype, message=message)
            else:
                print("here")
                Transaction.objects.create(trantype=trantype, message=message)

            messages.success(request, 'Yêu cầu được gửi thành công. Chúng tôi sẽ liên lạc lại với bạn sớm nhất.')
            return redirect('contacts')


@csrf_protect
def request_quote(request):
    form = RequestQuoteForm(request.POST)
    if not form.is_valid():
        return JsonResponse({
            "error": form.errors
        }, status=400)
    trantype = TransTypeInit.ORDER
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
        user = request.user
        has_contacted = Transaction.objects.filter(user=user, date__gte=yesterday)
        if has_contacted:
            return JsonResponse({
                'message': 'Chúng tôi đã nhận được thông tin của quý khách và sẽ liên hệ lại trong thời gian sớm nhất.'
            })
    else:
        user = None
    user = User.objects.create(name=name, email=email, phone=phone)
    Transaction.objects.create(user=user, trantype=trantype, message=message, house_type=house_type, district=district, request_price=request_price)

    return JsonResponse(
        {
            'message': 'Chúng tôi đã nhận được thông tin của quý khách và sẽ liên hệ lại trong thời gian sớm nhất.'
        })


@api_view(['GET', 'POST'])
def transactionsAPIViewWay1(request):
    """
    List all transactions, or create a new transaction.
    """
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class transactionsAPIView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer_context = {
            'request': request,
        }
        serializer = TransactionSerializer(queryset, many=True, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)
