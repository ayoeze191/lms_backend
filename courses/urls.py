from django.urls import path
from .views import (
    CourseListCreateView,
    CourseDetailView,
    CategoryListView,
)
urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course-list-create'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]