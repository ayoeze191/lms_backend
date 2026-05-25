from django.urls import path
from .views import (
    SectionListCreateView,
    SectionDetailView,
    LessonListCreateView,
    LessonDetailView,
)

urlpatterns = [
    path(
        '<int:course_pk>/sections/',
        SectionListCreateView.as_view(),
        name='section-list-create'
    ),
    path(
        '<int:course_pk>/sections/<int:pk>/',
        SectionDetailView.as_view(),
        name='section-detail'
    ),
    path(
        '<int:course_pk>/sections/<int:section_pk>/lessons/',
        LessonListCreateView.as_view(),
        name='lesson-list-create'
    ),
    path(
        '<int:course_pk>/sections/<int:section_pk>/lessons/<int:pk>/',
        LessonDetailView.as_view(),
        name='lesson-detail'
    ),
]