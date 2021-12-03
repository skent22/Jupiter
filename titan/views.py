from django.shortcuts import redirect, render
from django import forms

from titan.models import prescriber
from django.db.models import Q
# Create your views here.
def indexPageView(request) :
    return render(request, 'titan/index.html')

def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :
    newlist = []
    data = ''
    sql = ''
    form = ""
    if request.method == 'GET':
        test = 'frick spencer'
        
        name = request.GET
        if 'prescriberform' in name.keys():
            test = 'frick me'
            params = {
            'firstname' : request.GET['firstname'].title(),
            'lastname' : request.GET['lastname'].title(),
            'state' : request.GET['state'],
            'credential' : request.GET['credential'],
            'gender' : request.GET['gender']}
            if request.GET['gender'] != "":
                gender = request.GET['gender']
            # newlist = [firstname, lastname, state, credential, gender]
            # data = Prescriber.objects.filter(fname__contains = firstname,
            #  lname__contains = lastname,
            #  state__contains = state,
            #  credential__contains = credential,
            #  gender__contains = gender
            #   )
            sql = 'SELECT * FROM pd_prescriber inner join linking on linking.npi = pd_prescriber.npi inner join credentials on credentials.cred_id = linking.cred_id WHERE 1=1'
           

            if params['firstname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['firstname'])+'\'' + 'or  lname like ' + '\'' + str(params['firstname'] + '\')')
            if params['lastname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['lastname'])+'\'' + 'or  lname like ' + '\'' + str(params['lastname'] + '\')')
            if params['state'] != '':
                sql += ' AND (state LIKE ' +  '\''+str(params['state'])+'\') '
            if params['state'] != '':
                sql += ' AND (state LIKE ' +  '\''+str(params['state'])+'\') '
            if params['credential'] != '':
                sql += ' AND (abbreviation = ' +  '\''+str(params['credential'])+'\') '
            if params['gender'] != '':
                sql += ' AND (gender = ' +  '\''+str(params['gender'])+'\') '
            data = prescriber.objects.raw(sql)
            # data = prescriber.objects.filter((Q(fname__contains=params['firstname']) | Q(lname__contains=params['firstname']))) 
        
        elif 'drugform' in name.keys():
            form = 'drugform'
            medicationname = request.GET['medicationname']
            isopioid = ""
            if request.GET['isopioid'] != "":
                isopioid = request.GET['isopioid']
            newlist = [medicationname, isopioid]

    # data = ['drug1','drug2','drug3']
    context = {
        'resultset' : data,
        'test': test,
        'form': form
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

