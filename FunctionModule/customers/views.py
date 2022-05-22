from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from ..customers.models import Customer


@csrf_protect
def index(request):
    if request.user.is_authenticated and request.method == 'GET':
        if request.method == 'GET':
            customs = Customer.objects.filter(user=request.user).order_by('-hire_date')
            paginator = Paginator(customs, 10)
            page = request.GET.get('page')
            paged_customs = paginator.get_page(page)
            context = {
                'customers': paged_customs,
            }

        return render(request, 'customers/customers.html', context)
    else:
        return render(request, 'accounts/_profile.html')


def customer(request, customer_id):
    customs = Customer.objects.filter(user=request.user)
    customer_detail = get_object_or_404(Customer, pk=customer_id)
    context = {
        'customers': customs,
        'customer': customer_detail,
    }

    return render(request, 'customers/detail.html', context)
