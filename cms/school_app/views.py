from django.views.generic import TemplateView, ListView, DetailView
from django_filters.views import FilterView
from .models import School, SchoolResourcesFilter, Post

# Create your views here.
class HomePageView(TemplateView):
    template_name = "index.html"

class AboutView(TemplateView):
    template_name = "about.html"

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
    queryset = School.objects.exclude(lat=None).exclude(lon=None)
    template_name = "full_map.html"

class PostList(ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 3
    template_name = 'post_list.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
