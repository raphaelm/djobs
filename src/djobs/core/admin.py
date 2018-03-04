from django.contrib.admin import AdminSite, ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from djobs.core.models import JobOpening, AccessCode


class CRMAdminSite(AdminSite):
    site_header = 'djobs'


class AccessCodeAdmin(ModelAdmin):
    list_display = ['code', 'tag']


site = CRMAdminSite(name='admin')
site.register(JobOpening)
site.register(AccessCode, AccessCodeAdmin)
site.register(User, UserAdmin)
