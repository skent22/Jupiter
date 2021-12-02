from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView, statisticsPageView, detailsdrugsPageView
urlpatterns = [
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("details/<int:prescriberid>", detailsPageView, name="details"),
    path("details/<int:drugid>", detailsdrugsPageView, name="detailsdrugs"),
    path("statistics/", statisticsPageView, name="statistics"),
    path("", indexPageView, name="index"),
        ]