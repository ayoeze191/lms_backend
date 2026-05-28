from django.db import models
from django.conf import settings
from courses.models import Course


class Enrollment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.email} - {self.course.code} ({self.status})"

    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']


class Result(models.Model):
    class Grade(models.TextChoices):
        A = 'A', 'A'
        B = 'B', 'B'
        C = 'C', 'C'
        D = 'D', 'D'
        E = 'E', 'E'
        F = 'F', 'F'

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='result'
    )
    ca_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Continuous Assessment score out of 40'
    )
    exam_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Exam score out of 60'
    )
    total_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )
    grade = models.CharField(
        max_length=2,
        choices=Grade.choices,
        blank=True,
        null=True
    )
    grade_point = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def compute_grade(self):
        total = float(self.ca_score) + float(self.exam_score)
        self.total_score = total

        if total >= 70:
            self.grade = self.Grade.A
            self.grade_point = 5.0
        elif total >= 60:
            self.grade = self.Grade.B
            self.grade_point = 4.0
        elif total >= 50:
            self.grade = self.Grade.C
            self.grade_point = 3.0
        elif total >= 45:
            self.grade = self.Grade.D
            self.grade_point = 2.0
        elif total >= 40:
            self.grade = self.Grade.E
            self.grade_point = 1.0
        else:
            self.grade = self.Grade.F
            self.grade_point = 0.0

    def save(self, *args, **kwargs):
        self.compute_grade()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student.email} - {self.enrollment.course.code} - {self.grade}"