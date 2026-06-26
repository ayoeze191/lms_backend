# courses/tasks.py
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Course

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_course_assignment_email(self, course_id, lecturer_id):
    """
    Send email notification when a lecturer is assigned to a course.
    This runs in the background via Celery.
    
    Args:
        course_id: ID of the Course instance
        lecturer_id: ID of the User (lecturer) instance
    """
    try:
        # Fetch the course and lecturer from database
        course = Course.objects.get(id=course_id)
        User = get_user_model()
        lecturer = User.objects.get(id=lecturer_id)
        
        # Prepare email content
        subject = f"Course Assignment: {course.code} - {course.title}"
        
        message = f"""
Dear {lecturer.get_full_name() or lecturer.username},

You have been assigned to teach the following course:

Course: {course.title}
Code: {course.code}
Department: {course.department.name if hasattr(course, 'department') else 'N/A'}
Credit Units: {course.credit_units if hasattr(course, 'credit_units') else 'N/A'}
Level: {course.level if hasattr(course, 'level') else 'N/A'}

Please log in to the UniLMS portal to manage your students.

Regards,
UniLMS Admin
        """
        
        # Send the email
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lecturer.email],
            fail_silently=False,
        )
        
        logger.info(f"Email sent to {lecturer.email} for course {course.code}")
        return f"Email sent to {lecturer.email}"
        
    except Course.DoesNotExist:
        logger.error(f"Course with id {course_id} not found")
        return None
        
    except User.DoesNotExist:
        logger.error(f"Lecturer with id {lecturer_id} not found")
        return None
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Retry the task with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

@shared_task
def send_bulk_course_emails(course_lecturer_pairs):
    """
    Send multiple course assignment emails at once.
    
    Args:
        course_lecturer_pairs: List of (course_id, lecturer_id) tuples
    """
    results = []
    for course_id, lecturer_id in course_lecturer_pairs:
        try:
            result = send_course_assignment_email.delay(course_id, lecturer_id)
            results.append({"success": True, "task_id": result.id})
        except Exception as e:
            results.append({"success": False, "error": str(e)})
    return results