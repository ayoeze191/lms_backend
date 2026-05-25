from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Section, Lesson
from .serializers import SectionSerializer, LessonSerializer
from courses.models import Course


class SectionListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    def get(self, request, course_pk):
        sections = Section.objects.filter(course_id=course_pk)
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, course_pk):
        try:
            course = Course.objects.get(pk=course_pk)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can add sections."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = SectionSerializer(data={**request.data, 'course': course_pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SectionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            return None

    def patch(self, request, course_pk, pk):
        section = self.get_object(pk)
        if not section:
            return Response(
                {"error": "Section not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if section.course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can edit sections."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = SectionSerializer(section, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_pk, pk):
        section = self.get_object(pk)
        if not section:
            return Response(
                {"error": "Section not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if section.course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can delete sections."},
                status=status.HTTP_403_FORBIDDEN
            )
        section.delete()
        return Response(
            {"message": "Section deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class LessonListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, course_pk, section_pk):
        lessons = Lesson.objects.filter(section_id=section_pk)
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, course_pk, section_pk):
        try:
            section = Section.objects.get(pk=section_pk)
        except Section.DoesNotExist:
            return Response(
                {"error": "Section not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if section.course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can add lessons."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(section=section)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return None

    def patch(self, request, course_pk, section_pk, pk):
        lesson = self.get_object(pk)
        if not lesson:
            return Response(
                {"error": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if lesson.section.course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can edit lessons."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = LessonSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_pk, section_pk, pk):
        lesson = self.get_object(pk)
        if not lesson:
            return Response(
                {"error": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if lesson.section.course.instructor != request.user:
            return Response(
                {"error": "Only the course instructor can delete lessons."},
                status=status.HTTP_403_FORBIDDEN
            )
        lesson.delete()
        return Response(
            {"message": "Lesson deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )