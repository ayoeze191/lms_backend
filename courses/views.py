from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .models import Course, Faculty, Department, AcademicSession, Semester
from .serializers import (
    CourseSerializer,
    FacultySerializer,
    DepartmentSerializer,
    AcademicSessionSerializer,
    SemesterSerializer,
)


class FacultyListCreateView(APIView):
    serializer_class = FacultySerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can create faculties."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListCreateView(APIView):
    serializer_class = DepartmentSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can create departments."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcademicSessionListCreateView(APIView):
    serializer_class = AcademicSessionSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        sessions = AcademicSession.objects.all()
        serializer = AcademicSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can create academic sessions."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = AcademicSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SemesterListCreateView(APIView):
    serializer_class = SemesterSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can create semesters."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseListCreateView(APIView):
    serializer_class = CourseSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    @extend_schema(operation_id='courses_list', responses=CourseSerializer(many=True))
    def get(self, request):
        courses = Course.objects.filter(is_active=True)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id='courses_create', request=CourseSerializer, responses=CourseSerializer)
    def post(self, request):
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can create courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    serializer_class = CourseSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    @extend_schema(operation_id='courses_retrieve', responses=CourseSerializer)
    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(operation_id='courses_partial_update', request=CourseSerializer, responses=CourseSerializer)
    def patch(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can update courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(operation_id='courses_destroy')
    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_admin:
            return Response(
                {"error": "Only admins can delete courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        course.delete()
        return Response(
            {"message": "Course deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
