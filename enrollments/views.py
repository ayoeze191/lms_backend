from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Enrollment, Result
from .serializers import EnrollmentSerializer, ResultSerializer


class EnrollmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_student:
            enrollments = Enrollment.objects.filter(student=request.user)
        elif request.user.is_lecturer:
            enrollments = Enrollment.objects.filter(course__lecturer=request.user)
        elif request.user.is_admin:
            enrollments = Enrollment.objects.all()
        else:
            enrollments = Enrollment.objects.none()
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
            enrollment = serializer.save()
            return Response(
                EnrollmentSerializer(enrollment).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            return None

    def get(self, request, pk):
        enrollment = self.get_object(pk)
        if not enrollment:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        enrollment = self.get_object(pk)
        if not enrollment:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if enrollment.student != request.user:
            return Response(
                {"error": "You can only cancel your own enrollment."},
                status=status.HTTP_403_FORBIDDEN
            )
        enrollment.delete()
        return Response(
            {"message": "Enrollment cancelled successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class EnrollmentApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            enrollment = Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not request.user.is_lecturer and not request.user.is_admin:
            return Response(
                {"error": "Only lecturers and admins can approve enrollments."},
                status=status.HTTP_403_FORBIDDEN
            )

        if request.user.is_lecturer and enrollment.course.lecturer != request.user:
            return Response(
                {"error": "You can only approve enrollments for your own courses."},
                status=status.HTTP_403_FORBIDDEN
            )

        action = request.data.get('action')

        if action == 'approve':
            enrollment.status = Enrollment.Status.APPROVED
            enrollment.approved_at = timezone.now()
            enrollment.save()
            return Response(
                {"message": "Enrollment approved successfully."},
                status=status.HTTP_200_OK
            )
        elif action == 'reject':
            enrollment.status = Enrollment.Status.REJECTED
            enrollment.rejected_at = timezone.now()
            enrollment.rejection_reason = request.data.get('rejection_reason', '')
            enrollment.save()
            return Response(
                {"message": "Enrollment rejected successfully."},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid action. Use 'approve' or 'reject'."},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResultCreateUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, enrollment_pk):
        if not request.user.is_lecturer and not request.user.is_admin:
            return Response(
                {"error": "Only lecturers and admins can enter results."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            enrollment = Enrollment.objects.get(pk=enrollment_pk)
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_lecturer and enrollment.course.lecturer != request.user:
            return Response(
                {"error": "You can only enter results for your own courses."},
                status=status.HTTP_403_FORBIDDEN
            )

        if enrollment.status != Enrollment.Status.APPROVED:
            return Response(
                {"error": "Results can only be entered for approved enrollments."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result, created = Result.objects.get_or_create(enrollment=enrollment)
        serializer = ResultSerializer(result, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublishResultView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, enrollment_pk):
        if not request.user.is_lecturer and not request.user.is_admin:
            return Response(
                {"error": "Only lecturers and admins can publish results."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            enrollment = Enrollment.objects.get(pk=enrollment_pk)
            result = enrollment.result
        except Enrollment.DoesNotExist:
            return Response(
                {"error": "Enrollment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Result.DoesNotExist:
            return Response(
                {"error": "Result not found. Enter result first."},
                status=status.HTTP_404_NOT_FOUND
            )

        result.is_published = True
        result.save()
        return Response(
            {"message": "Result published successfully."},
            status=status.HTTP_200_OK
        )