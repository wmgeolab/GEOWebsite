import time
from os.path import exists, getmtime

from django.core.management import call_command
from django.http import FileResponse
from django.views.generic import DetailView, ListView, TemplateView
from django_filters.views import FilterView

from .models import Post, School, SchoolResourcesFilter

# Create your views here.


class HomePageView(TemplateView):
    template_name = "index.html"


class AboutView(TemplateView):
    template_name = "about.html"


class SchoolListView(FilterView):
    model = School
    paginate_by = 20
    template_name = "schools_list.html"
    # ordering = ['school_name'] # Ordering without index is slow for large offsets
    filterset_class = SchoolResourcesFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preserve filter options
        get_copy = self.request.GET.copy()
        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        # Get list of surrounding pages for navigation buttons
        if context['is_paginated']:
            paginator = context['paginator']
            page_num = context['page_obj'].number
            page_range = paginator.page_range
            page_list = [page_num]
            i = 1
            while len(page_list) < min(5, paginator.num_pages):
                if page_num + i in page_range:
                    page_list.append(page_num + i)
                if page_num - i in page_range:
                    page_list.insert(0, page_num - i)
                i += 1
            context['page_list'] = page_list
        return context


class SchoolProfileView(DetailView):
    model = School
    template_name = "school_profile.html"


class MapView(TemplateView):
    template_name = "full_map.html"


class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 3
    template_name = 'post_list.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'


def SchoolListDownload(request):
    now = time.time()
    if not exists('csv/schools.csv') or now - getmtime('csv/schools.csv') > 7200: # 7200 seconds = 2 hours
        call_command('writecsv')
    encodings = [s.strip().upper()
                 for s in request.META['HTTP_ACCEPT_ENCODING'].split(',')]
    print(encodings)
    if 'BR' in encodings:
        # Ideally serve brotli
        print('Serving BR')
        response = FileResponse(
            open('csv/schools.csv.br', 'rb'), as_attachment=True, filename='schools.csv')
        response['Content-Encoding'] = 'br'
        response['Vary'] = 'Accept-Encoding'
    elif 'GZIP' in encodings:
        print('Serving GZ')
        # Fallback on gzip
        response = FileResponse(
            open('csv/schools.csv.gz', 'rb'), as_attachment=True, filename='schools.csv')
        response['Content-Encoding'] = 'gzip'
        response['Vary'] = 'Accept-Encoding'
    else:
        print('Serving text')
        # Fallback on no compression
        response = FileResponse(
            open('csv/schools.csv', 'rb'), as_attachment=True)
    response['Content-Type'] = 'text/csv'
    return response
