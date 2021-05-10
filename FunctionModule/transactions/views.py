from rest_framework import status, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from pydantic import BaseModel

from .models import Transaction 
from .serializers import *

class TransactionSearchQuery(BaseModel):
    keywords: str = None
    state: int = None
    bedrooms: int = None
    price: int = None


def index(request):
    transactions = Transaction.objects.order_by('-date').filter()
    paginator = Paginator(transactions, 6)
    page = request.GET.get('page')
    paged_transations = paginator.get_page(page)

    context = {
        'transactions': paged_transations
    }

    return render(request, 'transactions/search.html', context)


def transaction(request, transaction_id):

    transaction = get_object_or_404(Transaction, pk=transaction_id)
    transactions_same = Transaction.objects.order_by('-date').filter(status=transaction.status)
    context = {
        'transaction': transaction,
        'transactions_same': transactions_same
    }

    return render(request, 'transactions/detail.html', context)

def detail(request):
    transaction_id = request.GET.get('id', '')
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    context = {
        'transaction': transaction,
     }

    return render(request, 'transactions/detail.html', context)


def search(request):
    queryset_list = Transaction.objects.order_by('-date')

    # Trang thai giao dich
    if 'reason' in request.GET:
        reason = request.GET['reason']
        if reason:
            queryset_list = queryset_list.filter(reason=reason)

    # Tim theo khach hang
    if 'user' in request.GET:
        user = request.GET['user']
        if user:
            queryset_list = queryset_list.filter(user=user)

    # tim theo bat dong san
    if 'listing' in request.GET:
        listing = request.GET['listing']
        if listing:
            queryset_list = queryset_list.filter(listing=listing)

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            query = Q(comment__icontains=keywords) 
            queryset_list = queryset_list.filter(query)

     # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query = Q(price__lte=price)
            queryset_list = queryset_list.filter(query)


    context = {
        'transactions': queryset_list,
    }

    return render(request, 'transactions/search.html', context)

@api_view(['GET', 'POST'])
def transactionsAPIViewWay1(request):
    """
    List all transactions, or create a new transaction.
    """
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class transactionsAPIView(generics.RetrieveAPIView):
    queryset= Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
 
        serializer_context = {
            'request': request,
        }
        serializer = TransactionSerializer(queryset, many=True, context=serializer_context)    

        return Response(serializer.data, status=status.HTTP_200_OK)


   