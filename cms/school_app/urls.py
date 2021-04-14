from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('schools_list/', views.SchoolListView.as_view()),
    path('schools/<int:pk>/', views.SchoolProfileView.as_view()),
    path('full_map/', views.MapView.as_view()),
]

