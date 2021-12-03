from django.shortcuts import redirect, render
from django import forms

# Create your views here.
def indexPageView(request) :
    return render(request, 'titan/index.html')

def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :
    newlist = []
    if request.method == 'GET':
        test = 'frick spencer'
        name = request.GET
        if 'prescriberform' in name.keys():
            test ='frick me' 
            firstname = request.GET['firstname']
            lastname = request.GET['lastname']
            state = request.GET['state']
            credential = request.GET['credential']
            gender = ""
            if request.GET['gender'] != "":
                gender = request.GET['gender']
            newlist = [firstname, lastname, state, credential, gender]
            # data = Prescriber.objects.filter(fname__contains = firstname,
            #  lname__contains = lastname,
            #  state__contains = state,
            #  credential__contains = credential,
            #  gender__contains = gender
            #   )
        elif 'drugform' in name.keys():
            test = 'frick you'
            medicationname = request.GET['medicationname']
            isopioid = ""
            if request.GET['isopioid'] != "":
                isopioid = request.GET['isopioid']
            newlist = [medicationname, isopioid]

    data = ['drug1','drug2','drug3']
    context = {
        'resultset' : data,
        'test': test,
        'name':name,
        'newlist': newlist
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

