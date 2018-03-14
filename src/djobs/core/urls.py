from django.urls import path

from djobs.core.views import SubmitView, JobListView, JobDetailView, PrintPreView

urlpatterns = [
    path('submit/', SubmitView.as_view(), name='job.submit'),
    path('submit/preview/', PrintPreView.as_view(), name='job.preview'),
    path('<int:pk>/', JobDetailView.as_view(), name='job.detail'),
    path('', JobListView.as_view(), name='job.list'),
]
