from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from enrollments.models import Enrollment, LessonProgress
from enrollments.serializers import EnrollmentSerializer, LessonProgressSerializer
from lessons.models import Lesson


class EnrollmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_student:
            return Response(
                {"error": "Only students can enroll in courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = EnrollmentSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Enrollment.objects.get(pk=pk, student=user)
        except Enrollment.DoesNotExist:
            return None

    def get(self, request, pk):
        enrollment = self.get_object(pk, request.user)
        if not enrollment:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        enrollment = self.get_object(pk, request.user)
        if not enrollment:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        enrollment.delete()
        return Response(
            {"message": "Enrollment cancelled successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class LessonProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, enrollment_pk, lesson_pk):
        try:
            enrollment = Enrollment.objects.get(
                pk=enrollment_pk,
                student=request.user
            )
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            lesson = Lesson.objects.get(pk=lesson_pk)
        except Lesson.DoesNotExist:
            return Response(
                {"error": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        progress, created = LessonProgress.objects.get_or_create(
            enrollment=enrollment,
            lesson=lesson
        )

        progress.is_completed = True
        progress.completed_at = timezone.now()
        progress.save()

        # Check if all lessons in the course are completed
        total_lessons = Lesson.objects.filter(
            section__course=enrollment.course
        ).count()
        completed_lessons = enrollment.progress.filter(
            is_completed=True
        ).count()

        if total_lessons == completed_lessons:
            enrollment.status = Enrollment.Status.COMPLETED
            enrollment.completed_at = timezone.now()
            enrollment.save()

        return Response(
            {
                "message": "Lesson marked as completed.",
                "course_completed": enrollment.status == Enrollment.Status.COMPLETED,
            },
            status=status.HTTP_200_OK
        )