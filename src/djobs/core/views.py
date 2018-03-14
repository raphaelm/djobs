from django import forms
from django.contrib import messages
from django.forms import ClearableFileInput
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, DetailView

from djobs.core.models import AccessCode, JobOpening
from djobs.core.pdf import PDFGenerator


class CustomFileInput(ClearableFileInput):
    template_name = 'core/submit/clearable_file_input.html'


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = [
            'public', 'print_card', 'job_title', 'job_location',
            'job_remote', 'job_salary_range', 'job_description',
            'company_name', 'company_description', 'company_contact',
            'logo'
        ]
        widgets = {
            'public': forms.CheckboxInput(
                attrs={'class': 'filled-in'}
            ),
            'print_card': forms.CheckboxInput(
                attrs={'class': 'filled-in'}
            ),
            'job_remote': forms.CheckboxInput(
                attrs={'class': 'filled-in'}
            ),
            'job_description': forms.Textarea(
                attrs={'class': 'materialize-textarea'}
            ),
            'company_description': forms.Textarea(
                attrs={'class': 'materialize-textarea'}
            ),
            'company_contact': forms.Textarea(
                attrs={'class': 'materialize-textarea'}
            ),
            'logo': CustomFileInput,
        }


class SubmitView(TemplateView):

    @cached_property
    def code(self):
        try:
            return AccessCode.objects.get(
                code=self.request.GET.get('code')
            )
        except AccessCode.DoesNotExist:
            return

    @cached_property
    def opening(self):
        try:
            return self.code.job
        except JobOpening.DoesNotExist:
            return JobOpening(access_code=self.code)

    @cached_property
    def form(self):
        return JobOpeningForm(
            data=self.request.POST if self.request.method == "POST" else None,
            files=self.request.FILES if self.request.method == "POST" else None,
            instance=self.opening
        )

    def get_template_names(self):
        if self.code:
            return ['core/submit/form.html']
        else:
            return ['core/submit/start.html']

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        if self.code:
            ctx['form'] = self.form
            ctx['opening'] = self.opening
        return ctx

    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            self.form.save()
            messages.success(request, _('Your job posting has been saved!'))
            return redirect(request.path + '?code=' + self.code.code)
        else:
            return super().get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'code' in request.GET:
            if not self.code:
                messages.error(request, _('The access code you inserted was not found in our database. Please contact '
                                          'us if you think this is an error!'))
        return super().get(request, *args, **kwargs)


class PrintPreView(TemplateView):

    @cached_property
    def code(self):
        try:
            return AccessCode.objects.get(
                code=self.request.GET.get('code')
            )
        except AccessCode.DoesNotExist:
            return

    @cached_property
    def opening(self):
        try:
            return self.code.job
        except JobOpening.DoesNotExist:
            return JobOpening(access_code=self.code)

    def get(self, request, *args, **kwargs):
        if not self.code:
            messages.error(request, _('The access code you inserted was not found in our database. Please contact '
                                      'us if you think this is an error!'))

        data = PDFGenerator(self.opening).create_pdf()
        resp = HttpResponse(data)
        resp['Content-Type'] = 'application/pdf'
        resp['Content-Disposition'] = 'inline; filename="preview.pdf"'
        return resp


class JobDetailView(DetailView):
    model = JobOpening
    context_object_name = 'job'
    template_name = 'core/detail.html'

    def get_queryset(self):
        return JobOpening.objects.filter(active=True, public=True).order_by('company_name')


class JobListView(ListView):
    model = JobOpening
    context_object_name = 'jobs'
    template_name = 'core/list.html'

    def get_queryset(self):
        return JobOpening.objects.filter(active=True, public=True).order_by('company_name')
