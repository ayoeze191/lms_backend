from django.urls import path
from .views import (
    FacultyListCreateView,
    DepartmentListCreateView,
    AcademicSessionListCreateView,
    SemesterListCreateView,
    CourseListCreateView,
    CourseDetailView,
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('faculties/', FacultyListCreateView.as_view(), name='faculty-list-create'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('sessions/', AcademicSessionListCreateView.as_view(), name='session-list-create'),
    path('semesters/', SemesterListCreateView.as_view(), name='semester-list-create'),
]