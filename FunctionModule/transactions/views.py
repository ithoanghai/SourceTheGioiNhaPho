from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from datetime import timedelta

from FunctionModule.hitcount.views import HitCountDetailView

from .forms import RequestQuoteForm
from .models import TransTypeInit
from .serializers import *
from ..accounts.models import User
from ..customers.models import Customer
from ..listings import HouseType
from ..listings.models import Listing

@csrf_protect
def index(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            trans = Transaction.objects.filter(user=request.user).order_by('-date')
            paginator = Paginator(trans, 10)
            page = request.GET.get('page')
            paged_trans = paginator.get_page(page)
            context = {
                'transactions': paged_trans,
            }

            return render(request, 'transactions/transactions.html', context)

    else:
        return render(request, 'accounts/_profile.html')


def transaction(request, transaction_id):
    TransactionCountHitDetailView()
    transaction_detail = get_object_or_404(Transaction, pk=transaction_id)
    houseType = HouseType.choices
    context = {
        'transaction': transaction_detail,
        'houseType': houseType
    }

    return render(request, 'transactions/detail.html', context)


@csrf_protect
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        trantype = request.POST['trantype']

        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        name = f'{firstname} {lastname}'
        email = request.POST['email']
        phone = request.POST['phone']
        location = request.POST['location']
        house_type = request.POST['houseType']
        price = request.POST['price']
        message = request.POST['message']
        yesterday = timezone.now() - timedelta(days=1)

        if listing_id != 'none':
            listing = Listing.objects.get(pk=listing_id)
            if listing is not None:
                if request.user.is_authenticated:
                    user = request.user
                    if user is not None:
                        customer = Customer.objects.filter(Q(phone=phone) | Q(user=user)).first()
                        has_contacted = Transaction.objects.filter(listing=listing, customer=customer, date__gte=yesterday)
                        if has_contacted:
                            messages.success(request, 'B???n ???? g???i y??u c???u t???i ch??ng t??i v??? c??n h??? n??y. Xin th??? g???i l???i y??u c???u sau.')
                        else:
                            if customer is None: customer = Customer.objects.create(user=user, name=name, email=email, phone=phone)
                            Transaction.objects.create(listing=listing, user=user, customer=customer, trantype=trantype, caring_area=location, house_type=house_type, request_price=listing.price, message=message)
                            messages.success(request, 'B???n ???? g???i y??u c???u th??nh c??ng t???i ch??ng t??i v??? B??S %s.' % (listing.code))
                else:
                    customer = Customer.objects.filter(Q(phone=phone)).first()
                    if customer is None: customer = Customer.objects.create(name=name, email=email, phone=phone)
                    Transaction.objects.create(listing=listing, customer=customer, trantype=trantype, caring_area=location, house_type=house_type, request_price=listing.price, message=message)
                    messages.success(request,'B???n ???? g???i y??u c???u th??nh c??ng t???i ch??ng t??i v??? B??S %s.' % (listing.code))
            return redirect('/listings/' + listing_id)
        else:
            if request.user.is_authenticated:
                user = request.user
                if user is not None:
                    customer = Customer.objects.filter(Q(phone=phone) | Q(user=user)).first()
                    if customer is None: customer = Customer.objects.create(user=user, name=name, email=email, phone=phone)
                    Transaction.objects.create(user=user, customer=customer, trantype=trantype, caring_area=location, house_type=house_type, request_price=price, message=message)
            else:
                customer = Customer.objects.filter(Q(phone=phone)).first()
                if customer is None: customer = Customer.objects.create(name=name, email=email, phone=phone)
                Transaction.objects.create(customer=customer, trantype=trantype, caring_area=location, house_type=house_type, request_price=price, message=message)

            messages.success(request, 'Y??u c???u ???????c g???i th??nh c??ng. Ch??ng t??i s??? li??n l???c l???i v???i b???n s???m nh???t.')
        return redirect('message')


@csrf_protect
def request_quote(request):
    print("request_quote")
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
    house_type = form.cleaned_data.get('hoty')
    district = form.cleaned_data.get('district')
    request_price = form.cleaned_data.get('request_price')
    yesterday = timezone.now() - timedelta(days=1)
    #  Check if user has made inquiry already
    if request.user.is_authenticated:
        user = request.user
        has_contacted = Transaction.objects.filter(user=user, date__gte=yesterday)
        if has_contacted:
            return JsonResponse({
                'message': 'Ch??ng t??i ???? nh???n ???????c th??ng tin c???a qu?? kh??ch v?? s??? li??n h??? l???i trong th???i gian s???m nh???t.'
            })
    else:
        user = None
    user = User.objects.create(name=name, email=email, phone=phone)
    Transaction.objects.create(user=user, trantype=trantype, message=message, house_type=house_type, caring_area=district, request_price=request_price)

    return JsonResponse(
        {
            'message': 'Ch??ng t??i ???? nh???n ???????c th??ng tin c???a qu?? kh??ch v?? s??? li??n h??? l???i trong th???i gian s???m nh???t.'
        })


class TransactionMixinDetailView(object):
    """
    Mixin to save us some typing.  Adds context for us!
    """
    model = Transaction

    def get_context_data(self, **kwargs):

        context = super(TransactionMixinDetailView, self).get_context_data(**kwargs)
        context['transaction_list'] = Transaction.objects.all()[:5]
        context['transaction_views'] = ["ajax", "detail", "detail-with-count"]
        return context


class TransactionCountHitDetailView(TransactionMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True


class TransactionDetailView(TransactionMixinDetailView, HitCountDetailView):
    """
    Generic hitcount class based view.
    """
    pass