from django.core.paginator import Paginator
from django.db.models import Q
from django.http import response, HttpResponse
from django.shortcuts import render

from FunctionModule.realtors.models import Realtor


def search(request):
    query = request.GET.get("keys")
    if query is not None:
        specialists = Realtor.objects.filter(
            Q(name__icontains=query)
            | Q(phone1__icontains=query)
            | Q(phone2__icontains=query)
            | Q(department__icontains=query)
            | Q(email__icontains=query)
            | Q(title__icontains=query)
            | Q(work_area__icontains=query)
            | Q(facebook__icontains=query)
            | Q(address__icontains=query)
            , is_published=True, is_cooperate=True
        )
    else:
        specialists = Realtor.objects.filter(
            is_published=True, is_cooperate=True
        )
    specialists = specialists.order_by('-hire_date')
    paginator = Paginator(specialists, 16)
    page = request.GET.get('page')
    paged_spect = paginator.get_page(page)
    context = {
        'specialists': paged_spect,
    }

    return render(request, 'home/specialist.html', context)