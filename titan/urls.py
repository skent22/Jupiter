from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView, statisticsPageView, detailsdrugsPageView, addtutorPageView,detPageView
urlpatterns = [
    path('det/<int:prescid>/<str:dn>/',detPageView,name='det'),
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("details/<int:tutorid>", detailsPageView, name="details"),
    path("detailsdrugs/<int:drugid>", detailsdrugsPageView, name="detailsdrugs"),
    path("addtutor/", addtutorPageView, name="addtutor"),
    path("statistics/", statisticsPageView, name="statistics"),
    path("send_mail/", indexPageView, name="mail"),
    path("", indexPageView, name="index"),
        ]