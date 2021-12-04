
# Create your models here.
from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.fields import CharField

# Create your models here.
class drug(models.Model):
    drugid = models.IntegerField(unique = True, null=False, editable=False,default='')
    drugname = models.CharField(verbose_name='Drug Name',max_length=30, unique=True, null=False,default='',primary_key=True)
    isopioid = models.BooleanField(null=False,verbose_name='Is Opioid')

    def __str__ (self):
        return (self.drugname)
    class Meta:
        db_table = 'pd_drugs'
        verbose_name = 'Drug'

class prescriber(models.Model):
    npi = models.AutoField(primary_key = True)
    fname = models.CharField(max_length=11, null=False,verbose_name='First Name')
    lname = models.CharField(max_length=11, null=False,verbose_name='Last Name')
    gender = models.CharField(max_length=1, null=False,verbose_name='Gender')
    state = models.CharField(max_length=2, null=False,verbose_name='First Name')
    specialty = models.CharField(max_length=62, null=False,verbose_name='Specialty')
    isopioidprescriber = models.BooleanField(null=False,verbose_name='Is Opioid Prescriber')

    def __str__ (self):
        return (self.fname + ' ' + self.lname + ' ' + '(' + self.specialty +')')
    class Meta:
        db_table = 'pd_prescriber'
        verbose_name = 'Prescriber'

class state(models.Model):
    state = models.CharField(max_length=14, null=False,primary_key=True,default='',verbose_name='State')
    stateabbrev = models.CharField(max_length=2, null=False,verbose_name='State Abbreviation')
    population = models.IntegerField( null=False,verbose_name='Population')
    deaths = models.IntegerField( null=False, verbose_name='Deaths')
    
    #models.ForeignKey('rating',to_field='rating',null=True, on_delete=models.SET_NULL)
    #models.ForeignKey('category',to_field='category',null=True,on_delete=models.SET_NULL)
    class Meta:
        db_table = 'pd_statedata'
        verbose_name = 'State'

class triple(models.Model):
    prescriberid = models.ForeignKey(prescriber,db_column='prescriberid', verbose_name=("Prescriber"), on_delete=models.CASCADE, null=False,primary_key=True,default='')
    drugname = models.ForeignKey(drug,db_column='drugname', verbose_name=("DrugName"), on_delete=models.CASCADE, null=False,default='')
    qty = models.IntegerField(null=False)

    def __str__ (self):
        return (str(self.prescriberid) + ' - ' + str(self.drugname) + ' - ' + str(self.qty))
    class Meta:
        db_table = 'pd_triple'
        verbose_name = 'Triple'
        unique_together = (('prescriberid', 'drugname'))

class credential(models.Model):
    cred_id = models.IntegerField(unique = True, null=False,primary_key=True,editable=False,default='')
    abbreviation = models.CharField(max_length=20, null=False,verbose_name='Abbreviation')
    def __str__ (self):
        return (self.abbreviation)
    class Meta:
        db_table = 'credentials'
        verbose_name = 'Credential'

class link(models.Model):
    npi = models.ForeignKey(prescriber, db_column= 'npi',verbose_name=("NPI"), on_delete=models.CASCADE, null=False,primary_key=True,default='')
    cred_id = models.ForeignKey(credential,db_column='cred_id', verbose_name=("Credential_id"), on_delete=models.CASCADE, null=False,default='')

    def __str__ (self):
        return (str(self.npi) + ' - ' + str(self.cred_id))
    class Meta:
        db_table = 'linking'
        verbose_name = 'Prescriber_Credential'
        unique_together = (('npi', 'cred_id'))