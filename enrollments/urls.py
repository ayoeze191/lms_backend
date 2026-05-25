from django.urls import path
from .views import (
    EnrollmentListCreateView,
    EnrollmentDetailView,
    LessonProgressView,
)

urlpatterns = [
    path('', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path(
        '<int:enrollment_pk>/lessons/<int:lesson_pk>/complete/',
        LessonProgressView.as_view(),
        name='lesson-progress'
    ),
]