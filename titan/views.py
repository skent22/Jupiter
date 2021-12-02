from django.shortcuts import render

# Create your views here.
def indexPageView(request) :
    return render(request, 'titan/index.html')

def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :
    return render(request, 'titan/search.html')
def detailsPageView(request) :
    return render(request, 'titan/details.html')

def statisticsPageView(request) :
    return render(request, 'titan/statistics.html') 