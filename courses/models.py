from django.db import models
from django.conf import settings


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faculties'


class Department(models.Model):
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE,
        related_name='departments'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AcademicSession(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicSession.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Semester(models.Model):
    class SemesterType(models.TextChoices):
        FIRST = 'first', 'First Semester'
        SECOND = 'second', 'Second Semester'

    session = models.ForeignKey(
        AcademicSession,
        on_delete=models.CASCADE,
        related_name='semesters'
    )
    semester_type = models.CharField(
        max_length=20,
        choices=SemesterType.choices
    )
    is_current = models.BooleanField(default=False)
    registration_open = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.name} - {self.get_semester_type_display()}"

    def save(self, *args, **kwargs):
        if self.is_current:
            Semester.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ['session', 'semester_type']


class Course(models.Model):
    class Level(models.TextChoices):
        L100 = '100', '100 Level'
        L200 = '200', '200 Level'
        L300 = '300', '300 Level'
        L400 = '400', '400 Level'
        L500 = '500', '500 Level'

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    credit_units = models.PositiveIntegerField(default=2)
    level = models.CharField(
        max_length=10,
        choices=Level.choices,
        default=Level.L100
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

    class Meta:
        ordering = ['-created_at']