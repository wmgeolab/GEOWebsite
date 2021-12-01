from django.views.generic import TemplateView, ListView, DetailView
from django_filters.views import FilterView
from .models import School, SchoolResourcesFilter, Post
from django.http import HttpResponse
import csv

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

class SchoolListView(FilterView):
    queryset = School.objects.exclude(test_score=None).exclude(gender_ratio=None)
    paginate_by = 20
    template_name = "schools_list.html"
    ordering = ['school_name']
    filterset_class = SchoolResourcesFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_copy = self.request.GET.copy()
        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        return context

class SchoolProfileView(DetailView):
    model = School
    template_name = "school_profile.html"

class MapView(ListView):
    queryset = School.objects.exclude(lat=None).exclude(lon=None).exclude(test_score=None).exclude(gender_ratio=None)
    template_name = "full_map.html"

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 3
    template_name = 'post_list.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

def SchoolListDownload(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    field_names = School._meta.fields
    field_names = [str(field).split('.')[-1] for field in field_names]
    writer.writerow(field_names)
    items = School.objects.all()
    for obj in items:
        writer.writerow([getattr(obj, field) for field in field_names])

    response['Content-Disposition'] = 'attachment; filename="schools.csv"'

    return response
