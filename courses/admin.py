from django.contrib import admin
# Register your models here.
from .models import Course,Department, Faculty, AcademicSession, Semester

class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'lecturer', 'department', 'created_at']
    list_filter = ['department', 'level', 'created_at']
    search_fields = ['code', 'title', 'lecturer__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def save_model(self, request, obj, form, change):
        """Override save to add logging."""
        super().save_model(request, obj, form, change)
        if change and obj.lecturer:
            # Log that email will be queued
            self.message_user(
                request, 
                f"Course updated. Email notification will be sent to {obj.lecturer.email}.")

admin.site.register(Course, CourseAdmin)
admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(AcademicSession)
admin.site.register(Semester)
