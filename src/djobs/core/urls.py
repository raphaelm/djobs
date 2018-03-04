from django.urls import path

from djobs.core.views import SubmitView, JobListView, JobDetailView

urlpatterns = [
    path('submit/', SubmitView.as_view(), name='job.submit'),
    path('job/<pk>/', JobDetailView.as_view(), name='job.detail'),
    path('', JobListView.as_view(), name='job.list'),
]
