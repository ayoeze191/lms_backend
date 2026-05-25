from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Course, Category
from .serializers import CourseSerializer, CategorySerializer


class CourseListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        courses = Course.objects.filter(status='published')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_instructor:
            return Response(
                {"error": "Only instructors can create courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if course.instructor != request.user:
            return Response(
                {"error": "You can only edit your own courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(
                {"error": "Course not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        if course.instructor != request.user:
            return Response(
                {"error": "You can only delete your own courses."},
                status=status.HTTP_403_FORBIDDEN
            )
        course.delete()
        return Response(
            {"message": "Course deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)