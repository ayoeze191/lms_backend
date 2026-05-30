from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Course


@receiver(post_save, sender=Course)
def notify_lecturer_on_assignment(sender, instance, created, **kwargs):
    if not created and instance.lecturer:
        try:
            send_mail(
                subject=f"Course Assignment: {instance.code} - {instance.title}",
                message=f"""
Dear {instance.lecturer.username},

You have been assigned to teach the following course:

Course: {instance.title}
Code: {instance.code}
Department: {instance.department.name}
Credit Units: {instance.credit_units}
Level: {instance.level}

Please log in to the UniLMS portal to manage your students.

Regards,
UniLMS Admin
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.lecturer.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")