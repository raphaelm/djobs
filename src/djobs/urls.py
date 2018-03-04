from django.urls import path, include

from djobs.core.admin import site
from djobs.core import urls as coreurls

urlpatterns = [
    path('jobs/admin/', site.urls),
    path('jobs/', include(coreurls)),
]
