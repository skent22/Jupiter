from django.shortcuts import redirect, render
from django import forms

# Create your views here.
def indexPageView(request) :
    return render(request, 'titan/index.html')

def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :

    if request.method == 'GET':
        test = 'frick spencer'
        name = request.GET
        if 'prescriberform' in name.keys():
            test ='frick me' 
            # firstname = request.GET['firstname']
            # firstname = request.GET['firstname']
            # firstname = request.GET['firstname']
            # firstname = request.GET['firstname']
            #data = Employee.objects.filter(emp_first=sFirst, emp_last=sLast)

    data = ['drug1','drug2','drug3']
    context = {
        'resultset' : data,
        'test': test,
        'name':name
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

def addprescriberPageView(request) :
    return render(request, 'titan/addprescriber.html') 

