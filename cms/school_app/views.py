from django.views.generic import TemplateView, ListView, DetailView
from django_filters.views import FilterView
from .models import School, SchoolResourcesFilter

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

class SchoolListView(FilterView):
    model = School
    paginate_by = 20
    template_name = "schools_list.html"
    ordering = ['school_name']
    filterset_class = SchoolResourcesFilter

class SchoolProfileView(DetailView):
    model = School
    template_name = "school_profile.html"

class MapView(ListView):
    model = School
    template_name = "full_map.html"