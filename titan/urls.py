from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView, statisticsPageView, detailsdrugsPageView, addprescriberPageView
urlpatterns = [
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("details/<int:prescriberid>", detailsPageView, name="details"),
    path("detailsdrugs/<int:drugid>", detailsdrugsPageView, name="detailsdrugs"),
    path("addprescriber/", addprescriberPageView, name="addprescriber"),
    path("statistics/", statisticsPageView, name="statistics"),
    path("", indexPageView, name="index"),
        ]