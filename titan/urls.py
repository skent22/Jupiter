from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView
urlpatterns = [
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("detail/", detailsPageView, name="detail"),
    path("", indexPageView, name="index"),
        ]