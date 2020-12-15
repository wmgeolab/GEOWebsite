# from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.serializers import serialize
from django.core.cache import cache
from django.db.models import Avg, Sum
from .models import School, SchoolResourcesFilter
from cms.forms import RegionForm


# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

class AboutPageView(TemplateView):
    template_name = "about.html"

def school_list(request):
    year_list = School.objects.values().order_by('school_name')
    filtered_qs = SchoolResourcesFilter(request.GET, queryset = year_list)

    paginator = Paginator(filtered_qs.qs, 20)

    page = request.GET.get('page')
    
    try:
        response = paginator.page(page)
    except PageNotAnInteger:
        response = paginator.page(1)
    except EmptyPage:
        response = paginator.page(paginator.num_pages)


    return render(
        request, 
        'schools_list.html', 
        {'response': response, 'year_filter': filtered_qs})


def SchoolProfileView(request, school_name, region, district):
    school = School.objects.filter(Q(school_name=school_name) & Q(region=region) & Q(district=district))
    print(school)
    return render(request, 'school_profile.html', {'school_id': school})



def FullMapData(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            region_choice = form.cleaned_data['region_choice']
            q = School.objects.filter(region=region_choice)

            print("FORM:", form)
            print(region_choice)
    else:
        form = RegionForm()
        print("FORM:", form)
        q = School.objects.filter(region='ARMM')

    return render(request, 'full_map.html', {'filter': q, 'form': form})
