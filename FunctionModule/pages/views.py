from itertools import groupby
from random import random

from django import template
from django.views.decorators.cache import cache_page

from django.contrib.admin import site
from django.core.paginator import Paginator
from django.db.models import QuerySet, Count
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader

from FunctionModule.cadastral.lookups import get_all_states, get_all_districts
from FunctionModule.listings.choices import price_choices, bedroom_choices
from FunctionModule.listings.models import Listing, TransactionType
from FunctionModule.realtors.models import Realtor


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


#@cache_page(60 * 60)
def home_view(request):
    listings_for_sale = (Listing.objects.order_by('priority','-date_update')
                             .filter(is_published=True, transaction_type=TransactionType.SELL)[:30])
    listings_for_rent = (Listing.objects.order_by('priority','-date_update')
                             .filter(is_published=True, transaction_type=TransactionType.FOR_RENT)[:30])
    listings_project = (Listing.objects.order_by('priority','-date_update')
                            .filter(is_published=True, transaction_type=TransactionType.PROJECT)[:15])
    listing_advertising = (Listing.objects.order_by('priority','-date_update')
                            .filter(is_published=True, is_advertising=True)[:30])
    listing_by_group_forsale = (Listing.objects
              .values('district').annotate(dcount=Count('district'))
              .filter(is_published=True, transaction_type=TransactionType.SELL))
    listing_by_group_forrent = (Listing.objects.values('district')
                                .annotate(dcount=Count('district'))
                                .filter(is_published=True, transaction_type=TransactionType.FOR_RENT))
    listing_by_group_project = (Listing.objects.values('district')
                                .annotate(dcount=Count('district'))
                                .filter(is_published=True, transaction_type=TransactionType.PROJECT))
    listing_by_group_advertising = (Listing.objects.values('district')
                                .annotate(dcount=Count('district'))
                                .filter(is_published=True, is_advertising=True))
    list_district_hn = get_all_districts()
    context = {
        'listings_for_sale': listings_for_sale,
        'listings_for_rent': listings_for_rent,
        'listings_project': listings_project,
        'listing_advertising': listing_advertising,
        'listing_by_group_forsale': listing_by_group_forsale,
        'listing_by_group_forrent': listing_by_group_forrent,
        'listing_by_group_project': listing_by_group_project,
        'listing_by_group_advertising': listing_by_group_advertising,
        'state_data': get_all_states(),
        'district_data': list_district_hn,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
    }

    response = render(request, 'home/index.html', context)
    #response.status_code = 307
    return response


def message(request):
    context = {

    }

    return render(request, 'home/message.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    context = {
        'realtors': realtors,
    }

    return render(request, 'home/about.html', context)


def specialistus(request):
    context = {
    }

    return render(request, 'home/specialistUs.html', context)


def specialist(request):
    specialists = Realtor.objects.filter(is_published=True, is_cooperate=True).order_by('-hire_date')
    paginator = Paginator(specialists, 16)
    page = request.GET.get('page')
    paged_spect = paginator.get_page(page)
    context = {
        'specialists': paged_spect,
    }

    return render(request, 'home/specialist.html', context)


def specialist_detail(request, realtor_id):
    listings = Listing.objects.filter(realtor__id=realtor_id).order_by('-date_update')
    paginator = Paginator(listings, 9)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    realtor_detail = get_object_or_404(Realtor, pk=realtor_id, is_published=True, is_cooperate=True)
    context = {
        'realtor': realtor_detail,
        'listings': paged_listings,
    }

    return render(request, 'home/specialistDetail.html', context)


def whychoose(request):
    context = {
    }

    return render(request, 'home/whyChoose.html', context)


def services(request):
    context = {
    }

    return render(request, 'home/services.html', context)


def contacts(request):
    context = {
    }

    return render(request, 'home/contact.html', context)


def recruitment(request):
    context = {
    }

    return render(request, 'home/recruitment.html', context)

def termsofuse(request):
    context = {
    }

    return render(request, 'home/termsOfUse.html', context)


def privacypolicy(request):
    context = {
    }

    return render(request, 'home/privacyPolicy.html', context)


"""Admin url here"""
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        app_list = site.get_app_list(request)
        load_template = request.path.split('/')[1]
        context = {
            'segment': load_template,
            'available_apps': app_list
        }
        # context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('admin/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('admin/page-500.html')
        return HttpResponse(html_template.render(context, request))


def chart(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/charts.html', context)


def map(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/maps.html', context)

def table(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/tables.html', context)


def pageblank(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/page-blank.html', context)


def error403(request):
    context = {

    }
    return render(request, 'admin/page-403.html', context)


def error404(request):
    context = {

    }
    return render(request, 'admin/page-404.html', context)


def error500(request):
    context = {

    }
    return render(request, 'admin/page-500.html', context)


def handler404(request, exception, template_name='home/page-404.html'):
    response = render(request, 'home/page-404.html')
    response.status_code = 404
    return response


def handler500(request):
    context = {
    }
    response = render(request, 'home/page-500.html',context)
    response.status_code = 500
    return response

