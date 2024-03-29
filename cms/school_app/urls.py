from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view()),
    path("about/", views.AboutView.as_view()),
    path("schools_list/", views.SchoolListView.as_view()),
    path("schools/<int:pk>/", views.SchoolProfileView.as_view()),
    path("full_map/", views.MapView.as_view()),
    path("posts/", views.PostList.as_view()),
    path("posts/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("downloadcsv/", views.school_list_download, name="school_list_download"),
    path("geojson/", views.serve_geojson, name="serve_geojson"),
    path("api/<int:pk>/", views.api),
]
