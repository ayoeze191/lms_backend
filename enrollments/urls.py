from django.urls import path
from .views import (
    EnrollmentListCreateView,
    EnrollmentDetailView,
    EnrollmentApprovalView,
    ResultCreateUpdateView,
    PublishResultView,
)
urlpatterns = [
    path('', EnrollmentListCreateView.as_view(), name='enrollment-list-create'),
    path('<int:pk>/', EnrollmentDetailView.as_view(), name='enrollment-detail'),
    path('<int:pk>/approval/', EnrollmentApprovalView.as_view(), name='enrollment-approval'),
    path('<int:enrollment_pk>/results/', ResultCreateUpdateView.as_view(), name='result-create-update'),
    path('<int:enrollment_pk>/results/publish/', PublishResultView.as_view(), name='result-publish'),
]