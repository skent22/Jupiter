from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView, statisticsPageView
urlpatterns = [
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("details/", detailsPageView, name="details"),
    path("statistics/", statisticsPageView, name="statistics"),
    path("", indexPageView, name="index"),
        ]