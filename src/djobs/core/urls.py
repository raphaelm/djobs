from django.urls import path

from djobs.core.views import SubmitView

urlpatterns = [
    path('submit/', SubmitView.as_view()),
]
