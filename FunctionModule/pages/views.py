from django import template
from django.contrib.admin import site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from FunctionModule.cadastral.constants import state_data, district_data
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


def home_view(request):
    listings_for_sale = (Listing.objects
                             .order_by('-list_date')
                             .filter(is_published=True, transaction_type=TransactionType.SELL)[:3])
    listings_for_rent = (Listing.objects
                             .order_by('-list_date')
                             .filter(is_published=True, transaction_type=TransactionType.FOR_RENT)[:3])
    listings_project = (Listing.objects
                            .order_by('-list_date')
                            .filter(is_published=True, transaction_type=TransactionType.PROJECT)[:3])
    list_district_hn = district_data.get("01")
    context = {
        'listings_for_sale': listings_for_sale,
        'listings_for_rent': listings_for_rent,
        'listings_project': listings_project,
        'state_data': state_data,
        'district_data': list_district_hn,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
    }

    return render(request, 'home/index.html', context)


def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'home/about.html', context)


def specialist_us(request):
    context = {
    }

    return render(request, 'home/specialistUs.html', context)


def specialist(request):
    context = {
    }

    return render(request, 'home/specialist.html', context)


def whyChoose(request):
    context = {
    }

    return render(request, 'home/whyChoose.html', context)


def services(request):
    context = {
    }

    return render(request, 'home/services.html', context)


def contact(request):
    context = {
    }

    return render(request, 'home/contact.html', context)


def recruitment(request):
    context = {
    }

    return render(request, 'home/recruitment.html', context)


def apply(request):
    position = request.GET.get('trans_type', '')
    context = {
        'position': position,
    }

    return render(request, 'home/apply.html', context)


def termsOfUse(request):
    context = {
    }

    return render(request, 'home/termsOfUse.html', context)


def privacyPolicy(request):
    context = {
    }

    return render(request, 'home/privacyPolicy.html', context)


"""Admin url here"""


def dashboard(request):
    return redirect('admin/login')


def admin_login(request):
    return render(request, 'admin/login.html')


def layout(request, layout_id):
    app_list = site.get_app_list(request)
    context = {
        'layout_id': layout_id,
        'available_apps': app_list
    }
    return render(request, 'admin/index.html', context)

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


def profile(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/profile.html', context)


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
