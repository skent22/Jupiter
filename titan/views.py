# Brennan Williams!!!! Matt Corbett!!!!! Spencer Harrison!!!!! Stetson Kent!!!!
# 6 December 2021

# IS INTEX PROJECT!!!!

from .models import Tutor,Linking,Student,Subject,Appointment
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

from django.db.models import Q
from django.db.models import Max


#We have a lot of print statements - delete?
#Every Drug is displaying as an opioid
states = ( 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY')
# Create your views here.
def detPageView(request,tutorid,dn):
    if request.method == 'GET':
        x = Appointment.objects.get(tutor_id=tutorid,stud_id=dn)
        y = request.GET['presctot']
        print(request.GET.keys())
        Appointment.objects.filter(tutor_id=tutorid,stud_id=dn).update(qty = x.qty + int(request.GET['presctot']))
        context = {'resultset' : Appointment.objects.get(tutor_id=tutorid)}
    return detailsPageView(request,tutorid)

# View for index.html page
def indexPageView(request) :
    

    context = {
      
    }

    return render(request, 'titan/index.html', context)

# View for about.html page
def aboutPageView(request) :
    return render(request, 'titan/about.html') 

# View for the search page. Allow searching by the following parameters: firstname, lastname, state, subject, gender, degree
def searchPageView(request) :
    data = ''
    sql = ''
    # form = ""

    sub = Subject.objects.all()
    dreg = Tutor.objects.order_by('degree').distinct('degree')
    stud = Student.objects.all()
    # state = Tutor.objects.order_by('state').distinct('state')
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            # form = 'prescriberform'
            params = {
            'firstname' : request.GET['firstname'].title(),
            'lastname' : request.GET['lastname'].title(),
            'state' : request.GET['state'],
            'subject' : request.GET['credential'],
            'gender' : request.GET['gender'],
            'degree': request.GET['specialty']}
            if request.GET['gender'] != "":
                gender = request.GET['gender']
            sql = 'SELECT * FROM tutor inner join linking on linking.tutor_id = tutor.tutor_id inner join subject on subject.sub_id = linking.sub_id WHERE 1=1'
           

            if params['firstname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['firstname'])+ '\'' + 'or  lname like ' + '\'' + str(params['firstname'] + '\')')
            if params['lastname'] != '':
                sql += ' AND (fname LIKE ' +  '\''+str(params['lastname'])+'\'' + 'or  lname like ' + '\'' + str(params['lastname'] + '\')')
            if params['state'] != '':
                sql += ' AND (state LIKE ' +  '\''+str(params['state'])+'\') '
            if params['subject'] != '':
                sql += ' AND (subject_name = ' +  '\''+str(params['subject'])+'\') '
            if params['gender'] != '':
                sql += ' AND (gender = ' +  '\''+str(params['gender'])+'\') '
            if params['degree'] != '':
                sql += ' AND (degree = ' +  '\''+str(params['degree'])+'\') '
            sql += ' order by lname'
            data = Tutor.objects.raw(sql)
    
        
    context = {
        'resultset' : data,
        'test': sql,
        #'form': form,
        'sub': sub,
        'dreg': dreg,
        'stud': stud,
        'states': states,
    }
    return render(request, 'titan/search.html', context)

# View for the tutor details html page.
def detailsPageView(request, tutorid ) :
    if request.method == 'GET':
        name = request.GET
        if 'despres' in name.keys():
            print('worked')
            Tutor.objects.filter(tutor_id=tutorid).delete()
            return render(request,'titan/search.html')
    if request.method == 'GET':
        name = request.GET
        if 'prescriberform' in name.keys():
            params = {
               'firstname' : request.GET['firstname'].title(),
                'lastname' : request.GET['lastname'].title(),
                'state' : request.GET['state'],
                'gender' : request.GET['gender'],
                'degree':request.GET['specialty']}
            Tutor.objects.filter(tutor_id=tutorid).update(fname = params['firstname'],lname = params['lastname'],state = params['state'],gender = params['gender'],degree=params['degree'])

    if request.method == 'GET':
        name = request.GET
        print(name)
        if 'tripleadd' in name.keys():
            params = {
               'student' : request.GET['drug'],
                'qty' : request.GET['qty']}
            new_appt = Appointment()
            new_appt.stud = Student.objects.get(stud_id=params['student'])
            new_appt.qty = params['qty']
            new_appt.tutor = Tutor.objects.get(tutor_id=tutorid)
            new_appt.save(force_insert=True)

    if request.method == 'POST':
        name = request.POST
        if 'del' in name.keys():
            Linking.objects.filter(sub_id=Subject.objects.get(subject_name=request.POST['del']), tutor_id=tutorid).delete()
            print('delete')
    if request.method == 'POST':
        name = request.POST
        if 'credform' in name.keys():
            new_link = Linking()
            new_link.sub_id = Subject.objects.get(subject_name=request.POST['credential'])
            new_link.tutor_id = Tutor.objects.get(tutor_id=tutorid)
            new_link.save(force_insert=True)

            print(new_link)
    d = Tutor.objects.get(tutor_id=tutorid)
    sql = '''
    Select p.tutor_id, p.gender, d.stud_id, concat(d.fname, ' ', d.lname) as fullname, sum(qty) as totalAppointments
    from tutor p
    inner join appointment t on p.tutor_id = t.tutor_id
    inner join student d on d.stud_id = t.stud_id 
    where p.tutor_id = ''' + str(tutorid)  +   ''' group by p.tutor_id, d.stud_id, d.fname, d.lname, p.gender
    order by sum(qty) desc
    limit 10 '''
    oTutor = Tutor.objects.raw(sql)    
    oStudent = Student.objects.all()
    #Make top prescriptions Graph
    oSubject = Subject.objects.all()
    oAppointment = Appointment.objects.filter(tutor_id = tutorid)
    oDegree = Tutor.objects.order_by('degree').distinct('degree')
    #update form prescriber

    student_not_listed_query = '''
    Select stud_id, concat(fname, ' ', lname) as fullname
    from student
    where stud_id not in (select stud_id from appointment where tutor_id = ''' + str(tutorid) + ')'

    students_not_listed = Student.objects.raw(student_not_listed_query)
    # # listdrug = []
    studpass = []
    # # for x in pres:
    # #     listdrug.append(x)
    for x in students_not_listed:
        studpass.append(x)

    subjects_not_listed_query =     '''
                Select sub_id, subject_name
                from subject
                where sub_id not in (select sub_id from linking where tutor_id = ''' + str(tutorid) + ')'

    subjects_not_listed = Subject.objects.raw(subjects_not_listed_query)
    # # listdrug = []
    subjectpass = []
    # # for x in pres:
    # #     listdrug.append(x)
    for x in subjects_not_listed:
        subjectpass.append(x.subject_name)


    
    bHasTriple = False
    if len(oTutor) > 0 :
        bHasTriple = True

    total_appointment = 0
    for x in oTutor : total_appointment += x.totalappointments

    
    # total_opioid_prescribed = 0
    # for x in oTutor : 
    #     if x.isopioid == True :
    #         total_opioid_prescribed += x.totaldrugs

    # if total_prescribed != 0 :
    #     perc_opioid_prescription = round(total_opioid_prescribed/total_prescribed * 100, 1)
    # else :
    #     perc_opioid_prescription = 0

    current_subjects = Linking.objects.filter(tutor_id = tutorid)

    context = {
        'resultset' : d,
        'pres': oTutor,
        'subject':oSubject,
        'appointment':oAppointment,
        'spec' : oDegree,
        'student' : studpass,
        'bHasTriple' : bHasTriple,
        # 'total_prescribed' : total_prescribed,
        # 'total_opioid_prescribed' : total_opioid_prescribed,
        # 'total_nonopioid_prescribed' : total_prescribed - total_opioid_prescribed,
        # 'perc_opioid_prescription' : perc_opioid_prescription,
        'subjectpass': subjectpass,
        'states':states,
        'subs':current_subjects
    }
    return render(request, 'titan/details.html',context)

# View for the student details html page
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

# View for the addtutor html page
def addtutorPageView(request) :

    #created needed lists to be used iin drop down forms
    spec = Tutor.objects.order_by('degree').distinct('degree')
    states = ( 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY')
    subjects = Subject.objects.all()

    # IF there is a form submitted, then do all this logic
    if request.method == 'GET':
        name = request.GET
        print(name)
        if 'addtutor' in name.keys():
            params = {
                    'firstname' : request.GET['firstname'].title(),
                    'lastname' : request.GET['lastname'].title(),
                    'state' : request.GET['state'],
                    'subject' : request.GET['credential'],
                    'gender' : request.GET['gender'],
                    'degree' :request.GET['specialty'],
                    'isverified': request.GET['license']}
            

            #create new presriber object
            new_tutor = Tutor()
            new_tutor.fname = params['firstname']
            new_tutor.lname = params['lastname']
            new_tutor.state =  params['state']
            new_tutor.gender = params['gender']
            new_tutor.degree = params['degree']
            new_tutor.isverified = params['isverified']
            new_tutor.save()

            #get credential object based on the credential they submitted
            new_subject = Subject.objects.filter(subject_name=request.GET['credential'])

            #create linking object based on last two objects that we just created
            new_linking = Linking()
            new_linking.sub_id = new_subject[0]
            new_linking.tutor_id = new_tutor
            new_linking.save()

    context = {
        'states': states,
        'subjects': subjects,
        'spec':spec
    }
    return render(request, 'titan/addtutor.html', context) 

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