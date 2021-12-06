from django.urls import path
from .views import  indexPageView, aboutPageView, searchPageView, detailsPageView, statisticsPageView, detailsdrugsPageView, addprescriberPageView, setQueriesPageView,detPageView
urlpatterns = [
    path('det/<int:prescid>/<str:dn>/',detPageView,name='det'),
    path("about/", aboutPageView, name="about"),
    path("search/", searchPageView, name="search"),
    path("details/<int:prescriberid>", detailsPageView, name="details"),
    path("detailsdrugs/<int:drugid>", detailsdrugsPageView, name="detailsdrugs"),
    path("addprescriber/", addprescriberPageView, name="addprescriber"),
    path("statistics/", statisticsPageView, name="statistics"),
    path("send_mail/", indexPageView, name="mail"),
    path('set/<qnum>',setQueriesPageView, name='set'),
    path("", indexPageView, name="index"),
        ]