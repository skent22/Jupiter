# Register your models here.
from django.contrib import admin
from .models import drug, prescriber, triple,credential,link
# Register your models here.
admin.site.register(drug)
admin.site.register(prescriber)
admin.site.register(triple)
admin.site.register(credential)
admin.site.register(link)

# class credential(admin.ModelAdmin):
#     fields = ('abbreviation')

# class credential(admin.ModelAdmin):
#     exclude = ('cred_id',)

