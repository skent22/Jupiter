from django.shortcuts import render

# Create your views here.
def indexPageView(request) :
    return render(request, 'titan/index.html')

def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :
    data = ['drug1','drug2','drug3']
    context = {
        'resultset' : data,
    }
    return render(request, 'titan/search.html', context)
def detailsPageView(request, prescriberid ) :
    return render(request, 'titan/details.html')
def detailsdrugsPageView(request, drugid) :

    #get drug object based on drugid

    data = ['drug1','drug2','drug3']
    context = {
        'resultset' : data,
    }
    return render(request, 'titan/detailsdrugs.html', context)
def statisticsPageView(request) :
    return render(request, 'titan/statistics.html') 