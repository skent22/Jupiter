# Register your models here.
from django.contrib import admin
from .models import Tutor, Student, Appointment, Linking, Subject

admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Appointment)
admin.site.register(Linking)
admin.site.register(Subject)


