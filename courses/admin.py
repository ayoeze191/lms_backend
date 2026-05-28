from django.contrib import admin

# Register your models here.
from .models import Course,Department, Faculty, AcademicSession, Semester

admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(AcademicSession)
admin.site.register(Semester)