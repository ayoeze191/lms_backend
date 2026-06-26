# courses/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Course
from .tasks import send_course_assignment_email

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Course)
def notify_lecturer_on_assignment(sender, instance, created, **kwargs):
    """
    Signal handler that triggers when a Course is saved.
    If a lecturer is assigned (and it's an update, not creation),
    queue an email notification using Celery.
    """
    # Only send notification if:
    # 1. It's not a new course creation (we want to notify on assignment)
    # 2. A lecturer is assigned
    if not created and instance.lecturer:
        try:
            # Queue the email task - this returns immediately
            task = send_course_assignment_email.delay(
                course_id=instance.id,
                lecturer_id=instance.lecturer.id
            )
            
            logger.info(
                f"Email task queued for course {instance.code} "
                f"to lecturer {instance.lecturer.email} "
                f"(Task ID: {task.id})"
            )
            
        except Exception as e:
            # Log the error but don't break the application
            logger.error(
                f"Failed to queue email task for course {instance.code}: {str(e)}"
            )
    else:
        # Log if conditions aren't met
        if created:
            logger.debug(f"New course created, not sending assignment email")
        elif not instance.lecturer:
            logger.debug(f"No lecturer assigned to course {instance.code}")