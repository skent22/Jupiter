from django.shortcuts import redirect, render
from django import forms

from django.core.mail import send_mail
from .forms import EmailForm
from titan.models import drug, prescriber, state, credential, link
from django.db.models import Q

from titan.utils import get_top_opioid, get_top_prescriptions, get_top_prescribers, get_opioid_pie_chart

# Create your views here.
def indexPageView(request) :
    topOpioids = drug.objects.raw(
        '''
        Select d.drugid, d.drugname, sum(qty) totaldrugs
        from pd_drugs d
        inner join pd_triple t on d.drugname = t.drugname
        where d.isopioid = 't'
        group by d.drugid, d.drugname
        Order by sum(qty) Desc
        '''
    )
    
    opioid = [x.drugname.split('.')[0] for x in topOpioids]
    prescriptions = [y.totaldrugs for y in topOpioids]
    topOpioid = get_top_opioid(opioid, prescriptions)

    total_opioids = 0
    for x in topOpioids : total_opioids += x.totaldrugs

    #State Heat map

    state_info = state.objects.raw(
    '''Select state, deaths
        from pd_statedata
        where deaths is not null
        order by deaths DESC
        limit 5
        '''
    )
    context = {
        'drugs' : topOpioids,
        'opioid_chart': topOpioid,
        'total_opioids' : total_opioids,
        'state_info' : state_info,
    }

    return render(request, 'titan/index.html', context)


def aboutPageView(request) :
    return render(request, 'titan/about.html') 

def searchPageView(request) :
    data = ''
    sql = ''
    form = ""

    states = state.objects.all()
    credentials = credential.objects.all()
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            form = 'prescriberform'
            params = {
            'firstname' : request.GET['firstname'].title(),
            'lastname' : request.GET['lastname'].title(),
            'state' : request.GET['state'],
            'credential' : request.GET['credential'],
            'gender' : request.GET['gender']}
            if request.GET['gender'] != "":
                gender = request.GET['gender']
            sql = 'SELECT * FROM pd_prescriber inner join linking on linking.npi = pd_prescriber.npi inner join credentials on credentials.cred_id = linking.cred_id WHERE 1=1'
           

            if params['firstname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['firstname'])+'\'' + 'or  lname like ' + '\'' + str(params['firstname'] + '\')')
            if params['lastname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['lastname'])+'\'' + 'or  lname like ' + '\'' + str(params['lastname'] + '\')')
            if params['state'] != '':
                sql += ' AND (state LIKE ' +  '\''+str(params['state'])+'\') '
            if params['credential'] != '':
                sql += ' AND (abbreviation = ' +  '\''+str(params['credential'])+'\') '
            if params['gender'] != '':
                sql += ' AND (gender = ' +  '\''+str(params['gender'])+'\') '
            sql += ' order by lname'
            data = prescriber.objects.raw(sql)

        elif 'drugform' in name.keys():
            form = 'drugform'
            medicationname = request.GET['medicationname']
            isopioid = request.GET['isopioid']
            # newlist = [medicationname, isopioid]
            sql = 'SELECT * FROM pd_drugs WHERE 1=1'
            if request.GET['medicationname'] != '':
                sql += ' AND  drugname LIKE' + '\'' + medicationname + '\''
            if request.GET['isopioid'] != '':
                sql += ' AND isopioid = ' + '\'' + isopioid + '\''
            sql += ' order by drugname'
            data = drug.objects.raw(sql)
    context = {
        'resultset' : data,
        'test': sql,
        'form': form,
        'states': states,
        'credentials': credentials,
    }
    return render(request, 'titan/search.html', context)

def detailsPageView(request, prescriberid ) :
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            params = {
               'firstname' : request.GET['firstname'].title(),
                'lastname' : request.GET['lastname'].title(),
                'state' : request.GET['state'],
                'gender' : request.GET['gender']}
            prescriber.objects.filter(npi=prescriberid).update(fname = params['firstname'],lname = params['lastname'],state = params['state'],gender = params['gender'])

    if request.method == 'POST':
        print(request.POST)
        name = request.POST
        if 'del' in name.keys():
            link.objects.filter(cred_id=credential.objects.get(abbreviation=request.POST['del']), npi=prescriberid).delete()
            print('delete')
    if request.method == 'POST':
        name = request.POST
        print(request.POST)
        if 'credform' in name.keys():
            print('credform')
            new_link = link()
            new_link.cred_id = credential.objects.get(abbreviation=request.POST['credential'])
            new_link.npi = prescriber.objects.get(npi=prescriberid)
            new_link.save(force_insert=True)

            print(new_link)
    d = prescriber.objects.get(npi=prescriberid)
    sql = '''
    Select p.npi, d.drugid, d.drugname, sum(qty) as totaldrugs
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    inner join pd_drugs d on d.drugname = t.drugname 
    where p.npi = ''' + str(prescriberid)  +   ''' group by p.npi, d.drugid, d.drugname
    order by sum(qty) desc
    limit 10 '''
    states = state.objects.all()
    pres = prescriber.objects.raw(sql)

    #Make top prescriptions Graph
    cred = credential.objects.all()
    trip = link.objects.filter(npi = prescriberid)
    #update form prescriber
    
    
    #Make Graph
    drugname = [x.drugname for x in pres]
    prescriptions = [y.totaldrugs for y in pres]
    prescriptions_chart = get_top_prescribers(drugname, prescriptions)

    #Make percent opioid pie chart
    opioid_percent_sql = '''
    Select npi,
	(select case when sum(qty) is not null then 10000 * sum(qty) else 0 end from pd_triple where prescriberid = ''' + str(prescriberid)  +   ''' and drugname  in (select drugname from pd_drugs where isopioid = 't'))/
	sum(qty) as PercentOpioid,
	(select case when sum(qty) is not null then 10000 * sum(qty) else 0 end from pd_triple where prescriberid = ''' + str(prescriberid)  +   ''' and drugname in (select drugname from pd_drugs where isopioid = 'f'))/
	sum(qty) as PercentNonOpioid
	
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    where prescriberid =''' + str(prescriberid) + '''
    group by npi'''

    queryObject = prescriber.objects.raw(opioid_percent_sql)

    pecent_opioid = queryObject[0].percentopioid
    print(pecent_opioid)
    percent_nonopioid = queryObject[0].percentnonopioid
    print(percent_nonopioid)
    opioid_pie_chart = get_opioid_pie_chart(pecent_opioid, percent_nonopioid)


    context = {
        'resultset' : d,
        'pres': pres,
        'prescriptions_chart' : prescriptions_chart,
        'opioid_pie_chart' : opioid_pie_chart,
        'credential':cred,
        'link':trip
    }

    return render(request, 'titan/details.html',context)

def detailsdrugsPageView(request, drugid) :
    
    #get drug object based on drugid
    d = drug.objects.get(drugid=drugid)
    sql = ''' 
    Select p.npi, fname, lname, sum(qty) as totalDrugs
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    inner join pd_drugs d on d.drugname = t.drugname 
    where drugid = ''' + '\'' + str(drugid)  +'\'' +   '''group by npi, fname,lname
    order by sum(qty) desc
    limit 10 '''
    pres = prescriber.objects.raw(sql)

    #Make Graph
    prescribee = [x.fname for x in pres]
    prescriptions = [y.totaldrugs for y in pres]
    top_prescribers_chart = get_top_prescriptions(prescribee, prescriptions)

    total_prescribed = 0
    for x in pres : total_prescribed += x.totaldrugs

    context = {
        'resultset' : d,
        'pres': pres,
        'top_prescribers_chart' : top_prescribers_chart,
        'total_prescribed' : total_prescribed
    }
    return render(request, 'titan/detailsdrugs.html', context)
def statisticsPageView(request) :
    return render(request, 'titan/statistics.html')

def addprescriberPageView(request) :

    #created needed lists to be used iin drop down forms
    spec = prescriber.objects.order_by('specialty').distinct('specialty')
    states = state.objects.all()
    credentials = credential.objects.all()

    # IF there is a form submitted, then do all this logic
    if request.method == 'GET':
        name = request.GET
        if 'addprescriber' in name.keys():
            params = {
                    'firstname' : request.GET['firstname'].title(),
                    'lastname' : request.GET['lastname'].title(),
                    'state' : request.GET['state'],
                    'credential' : request.GET['credential'],
                    'gender' : request.GET['gender'],
                    'specialty' :request.GET['specialty'],
                    'isopioidpresriber': request.GET['license']}
            

            #create new presriber object
            new_presriber = prescriber()
            new_presriber.fname = params['firstname']
            new_presriber.lname = params['lastname']
            new_presriber.state = params['state']
            new_presriber.gender = params['gender']
            new_presriber.specialty = params['specialty']
            new_presriber.isopioidprescriber = params['isopioidpresriber']
            new_presriber.save()

            #get credential object based on the credential they submitted
            new_credential = credential.objects.filter(abbreviation=request.GET['credential'])

            #create linking object based on last two objects that we just created
            new_linking = link()
            new_linking.cred_id = new_credential[0]
            new_linking.npi = new_presriber
            new_linking.save()

    context = {
        'states': states,
        'credentials': credentials,
        'spec':spec
    }
    return render(request, 'titan/addprescriber.html', context) 

def sendMail(request):

    # create a variable to keep track of the form
    messageSent = False

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an email with Django"
            message = cd['message']

            # send the email to the recipent
            send_mail(subject, message,
                      'brennanwilliams2000@gmail.com' [cd['recipient']])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'index.html', {

        'form': form,
        'messageSent': messageSent,

    })