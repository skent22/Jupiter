# Brennan Williams!!!! Matt Corbett!!!!! Spencer Harrison!!!!! Stetson Harrison!!!!
# 6 December 2021

# IS INTEX PROJECT!!!!


from django.shortcuts import redirect, render
from django import forms
import time
# create sequence measures_measure_id_seq
# owned by pd_prescriber.npi;
   
# alter sequence measures_measure_id_seq restart with 1992994776;

# alter table pd_prescriber
# alter column npi set default nextval('measures_measure_id_seq')


# ALTER TABLE pd_triple 
#     ALTER id ADD GENERATED ALWAYS AS IDENTITY 
#         (START WITH 625495);

from django.core.mail import send_mail
from .forms import EmailForm
from titan.models import drug, prescriber, state, credential, link, triple
from django.db.models import Q
from django.db.models import Max

from titan.utils import get_top_opioid, get_top_prescriptions, get_top_prescribers, get_opioid_pie_chart


#We have a lot of print statements - delete?
#Every Drug is displaying as an opioid

# Create your views here.
def detPageView(request,prescid,dn):
    if request.method == 'GET':
        x = triple.objects.get(prescriberid=prescid,drugname=dn)
        y = request.GET['presctot']
        print(request.GET.keys())
        triple.objects.filter(prescriberid=prescid,drugname=dn).update(qty = x.qty + int(request.GET['presctot']))
        context = {'resultset' : prescriber.objects.get(npi=prescid)}
    return detailsPageView(request,prescid)


def setQueriesPageView(request,qnum):
    q = ''
    qset = ''
    form = ''
    if qnum == '1':
       
        q = '''select npi,lname,fname,gender,state,specialty,isopioidprescriber from pd_prescriber
                inner join pd_triple on pd_prescriber.npi = pd_triple.prescriberid
                inner join pd_drugs on pd_drugs.drugname = pd_triple.drugname
                where npi in (select npi from pd_prescriber
                inner join pd_triple on pd_prescriber.npi = pd_triple.prescriberid
                inner join pd_drugs on pd_drugs.drugname = pd_triple.drugname
                where isopioid = True) and npi not in (select npi from pd_prescriber
                inner join pd_triple on pd_prescriber.npi = pd_triple.prescriberid
                inner join pd_drugs on pd_drugs.drugname = pd_triple.drugname
                where isopioid = False);'''
        qset = prescriber.objects.raw(q)
        form = 'prescriberform'
    elif qnum == '2':
        print('oh boy')
        q = '''Select p.npi 
from pd_prescriber p
inner join pd_triple t on p.npi = t.prescriberid
inner join pd_drugs d on t.drugname = d.drugname
group by p.npi
Having 100*  (select sum(qty) from pd_triple where p.npi = prescriberid and drugname in (select drugname from pd_drugs where isopioid = 't'))/sum(qty) > 75  and sum(qty) > 100
'''
        qset = prescriber.objects.raw(q)
        form = 'prescriberform'
        print(form)
    context = {'resultset': qset,
                'test':qnum,
                'form':form}
    print(context['resultset'])
    return render(request,'titan/search.html',context)

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
    spec = prescriber.objects.order_by('specialty').distinct('specialty')
    drugs = drug.objects.all
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            form = 'prescriberform'
            params = {
            'firstname' : request.GET['firstname'].title(),
            'lastname' : request.GET['lastname'].title(),
            'state' : request.GET['state'],
            'credential' : request.GET['credential'],
            'gender' : request.GET['gender'],
            'specialty': request.GET['specialty']}
            if request.GET['gender'] != "":
                gender = request.GET['gender']
            sql = 'SELECT * FROM pd_prescriber inner join linking on linking.npi = pd_prescriber.npi inner join credentials on credentials.cred_id = linking.cred_id WHERE 1=1'
           

            if params['firstname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['firstname'])+ '\'' + 'or  lname like ' + '\'' + str(params['firstname'] + '\')')
            if params['lastname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['lastname'])+'\'' + 'or  lname like ' + '\'' + str(params['lastname'] + '\')')
            if params['state'] != '':
                sql += ' AND (state LIKE ' +  '\''+str(params['state'])+'\') '
            if params['credential'] != '':
                sql += ' AND (abbreviation = ' +  '\''+str(params['credential'])+'\') '
            if params['gender'] != '':
                sql += ' AND (gender = ' +  '\''+str(params['gender'])+'\') '
            if params['specialty'] != '':
                sql += ' AND (specialty = ' +  '\''+str(params['specialty'])+'\') '
            sql += ' order by lname'
            data = prescriber.objects.raw(sql)
    
            print(data)
        elif 'drugform' in name.keys():
            form = 'drugform'
            medicationname = request.GET['drug']
            isopioid = request.GET['isopioid']
            # newlist = [medicationname, isopioid]
            sql = 'SELECT * FROM pd_drugs WHERE 1=1'
            if request.GET['drug'] != '':
                sql += ' AND  drugname =' + '\'' + medicationname + '\''
            if request.GET['isopioid'] != '':
                sql += ' AND isopioid = ' + '\'' + isopioid + '\''
            sql += ' order by drugname'
            data = drug.objects.raw(sql)
            print(data)
    context = {
        'resultset' : data,
        'test': sql,
        'form': form,
        'states': states,
        'credentials': credentials,
        'spec':spec,
        'drug': drugs
    }
    return render(request, 'titan/search.html', context)

def detailsPageView(request, prescriberid ) :
    if request.method == 'GET':
        print(request.GET)
        name = request.GET
        if 'despres' in name.keys():
            print('worked')
            prescriber.objects.filter(npi=prescriberid).delete()
            print('delete')
            return render(request,'titan/search.html')
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            params = {
               'firstname' : request.GET['firstname'].title(),
                'lastname' : request.GET['lastname'].title(),
                'state' : request.GET['state'],
                'gender' : request.GET['gender'],
                'specialty':request.GET['specialty']}
            prescriber.objects.filter(npi=prescriberid).update(fname = params['firstname'],lname = params['lastname'],state = params['state'],gender = params['gender'],specialty=params['specialty'])

    if request.method == 'GET':
        name = request.GET
        print(name)
        if 'tripleadd' in name.keys():
            params = {
               'drug' : request.GET['drug'],
                'qty' : request.GET['qty']}
            new_triple = triple()
            new_triple.drugname = drug.objects.get(drugname=params['drug'])
            new_triple.qty = params['qty']
            new_triple.prescriberid = prescriber.objects.get(npi=prescriberid)
            new_triple.save(force_insert=True)

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
    Select p.npi, p.gender, d.drugid, d.drugname, d.isopioid, sum(qty) as totaldrugs
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    inner join pd_drugs d on d.drugname = t.drugname 
    where p.npi = ''' + str(prescriberid)  +   ''' group by p.npi, d.drugid, d.drugname, p.gender
    order by sum(qty) desc
    limit 10 '''
    states = state.objects.all()
    pres = prescriber.objects.raw(sql)    
    drugs = drug.objects.all()
    #Make top prescriptions Graph
    cred = credential.objects.all()
    trip = link.objects.filter(npi = prescriberid)
    spec = prescriber.objects.order_by('specialty').distinct('specialty')
    #update form prescriber

    drugs_not_listed_query = '''
    Select drugid, drugname
    from pd_drugs
    where drugname not in (select drugname from pd_triple where prescriberid = ''' + str(prescriberid) + ')'

    drugs_not_listed = drug.objects.raw(drugs_not_listed_query)
    # # listdrug = []
    drugpass = []
    # # for x in pres:
    # #     listdrug.append(x)
    for x in drugs_not_listed:
        drugpass.append(x.drugname)
    print('please')
    print(drugpass)
    
    #Make Graph
    drugname = [x.drugname for x in pres]
    prescriptions = [y.totaldrugs for y in pres]
    prescriptions_chart = get_top_prescribers(drugname, prescriptions)

    #Make percent opioid pie chart
    opioid_percent_sql = '''
    Select npi,
	(select case when sum(qty) is not null then sum(qty) else 0 end from pd_triple where prescriberid = ''' + str(prescriberid)  +   ''' and drugname  in (select drugname from pd_drugs where isopioid = 't')) as PercentOpioid,
	(select case when sum(qty) is not null then sum(qty) else 0 end from pd_triple where prescriberid = ''' + str(prescriberid)  +   ''' and drugname in (select drugname from pd_drugs where isopioid = 'f')) as PercentNonOpioid
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    where prescriberid =''' + str(prescriberid) + '''
    group by npi'''

    queryObject = prescriber.objects.raw(opioid_percent_sql)
    print(queryObject)
    if len(queryObject) > 0:
        pecent_opioid = queryObject[0].percentopioid
        # print(pecent_opioid)
        percent_nonopioid = queryObject[0].percentnonopioid
        # print(percent_nonopioid)
        opioid_pie_chart = get_opioid_pie_chart(pecent_opioid, percent_nonopioid)
    else: 
        opioid_pie_chart = ''

    bHasTriple = False
    if len(pres) > 0 :
        bHasTriple = True

    total_prescribed = 0
    for x in pres : total_prescribed += x.totaldrugs

    total_opioid_prescribed = 0
    for x in pres : 
        if x.isopioid == True :
            total_opioid_prescribed += x.totaldrugs

    if total_prescribed != 0 :
        perc_opioid_prescription = round(total_opioid_prescribed/total_prescribed * 100, 1)
    else :
        perc_opioid_prescription = 0



    context = {
        'resultset' : d,
        'pres': pres,
        'prescriptions_chart' : prescriptions_chart,
        'opioid_pie_chart' : opioid_pie_chart,
        'credential':cred,
        'link':trip,
        'states':states,
        'spec' : spec,
        'drug' : drugpass,
        'bHasTriple' : bHasTriple,
        'total_prescribed' : total_prescribed,
        'total_opioid_prescribed' : total_opioid_prescribed,
        'total_nonopioid_prescribed' : total_prescribed - total_opioid_prescribed,
        'perc_opioid_prescription' : perc_opioid_prescription
    }
    print(context['pres'])
    return render(request, 'titan/details.html',context)

def detailsdrugsPageView(request, drugid) :
    
    #get drug object based on drugid
    d = drug.objects.get(drugid=drugid)
    sql = ''' 
    Select p.npi, fname, lname, isopioidprescriber, sum(qty) as totalDrugs
    from pd_prescriber p
    inner join pd_triple t on p.npi = t.prescriberid
    inner join pd_drugs d on d.drugname = t.drugname 
    where drugid = ''' + '\'' + str(drugid)  +'\'' +   '''group by npi, fname,lname, isopioidprescriber
    order by sum(qty) desc
    limit 10 '''
    pres = prescriber.objects.raw(sql)

    total_times_prescribed_sql = '''
    Select d.drugname, sum(t.qty) as sumdrugs, count(prescriberid) as times_prescribed
    from pd_drugs d
    inner join pd_triple t on d.drugname = t.drugname 
    where drugid = ''' + '\'' + str(drugid)  +'\'' + '''
    group by d.drugname'''
    total_times_prescribed = drug.objects.raw(total_times_prescribed_sql)
    
    for x in total_times_prescribed :
        print(x.sumdrugs)


    #Make Graph
    prescribee = [x.fname for x in pres]
    prescriptions = [y.totaldrugs for y in pres]
    top_prescribers_chart = get_top_prescriptions(prescribee, prescriptions)

    total_prescribed = 0
    for x in pres : total_prescribed += x.totaldrugs

    new_drugname = str(d.drugname)
    new_drugname = new_drugname.replace('.', ' ')

    context = {
        'resultset' : d,
        'pres': pres,
        'top_prescribers_chart' : top_prescribers_chart,
        'total_prescribed' : total_prescribed,
        'new_drugname' : new_drugname,
        'total_times_prescribed' : total_times_prescribed,
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
        print(name)
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