from django.urls import path

from djobs.core.admin import site

urlpatterns = [
    path('jobs/admin/', site.urls),
]
