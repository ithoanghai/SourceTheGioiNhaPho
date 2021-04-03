from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from FunctionModule.listings.choices import price_choices, bedroom_choices, state_choices
from FunctionModule.listings.models import Listing
from FunctionModule.realtors.models import Realtor
from django.urls import reverse_lazy

from django.contrib.admin import site


def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    context = {
        'listings': listings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
    }

    return render(request, 'pages/index.html', context)



def about(request):
    # Get all realtors
    realtors = Realtor.objects.order_by('-hire_date')

    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'realtors': realtors,
        'mvp_realtors': mvp_realtors
    }

    return render(request, 'pages/about.html', context)

"""Admin url here"""
def dashboard(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }

    return render(request, 'admin/index.html', context)

def layout1(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/includes/index-static.html', context)

def layout2(request):
    app_list = site.get_app_list(request)
    context = {
        'available_apps': app_list
    }
    return render(request, 'admin/includes/index-light.html', context)

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
        #context['segment'] = load_template

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
    return render(request, 'admin/includes/profile.html', context)

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