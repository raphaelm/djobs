from django.conf import settings
from django.conf.urls import url
from django.urls import path, include
from django.views.static import serve

from djobs.core.admin import site
from djobs.core import urls as coreurls

urlpatterns = [
    path('jobs/admin/', site.urls),
    path('jobs/', include(coreurls)),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^jobs/media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
