from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


def new_code():
    return get_random_string(16, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class AccessCode(models.Model):
    tag = models.CharField(max_length=190, null=True, blank=True)
    code = models.CharField(max_length=190, default=new_code, unique=True)

    def __str__(self):
        return self.code


class JobOpening(models.Model):
    access_code = models.OneToOneField(
        AccessCode, related_name='job', on_delete=models.PROTECT
    )

    active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Only active job openings will be shown or printed.')
    )
    public = models.BooleanField(
        default=False,
        verbose_name=_('This job posting should be shown online'),
        help_text=_('If you set this option, we will publish the job posting both on our website and on a printed '
                    'card at the conference venue. If you do not set it, we will only show it on a printed card '
                    'at the conference venue, but not online.')
    )
    print_card = models.BooleanField(
        default=True,
        verbose_name=_('Please print a card for physical posting at the venue'),
        help_text=_('If you check this option, we will print a card for our physical job board for you. If you do not '
                    'check it, you need to print and bring a card on your own. Please make sure to restrict yourself '
                    'to a single A5-sized landscape page.')
    )

    job_title = models.CharField(
        max_length=190,
        verbose_name=_('Job title')
    )
    job_location = models.CharField(
        max_length=190,
        verbose_name=_('Job location')
    )
    job_remote = models.BooleanField(
        default=False,
        verbose_name=_('Remote work possible')
    )
    job_salary_range = models.CharField(
        max_length=190, blank=True, null=True,
        verbose_name=_('Salary range (optional)')
    )
    job_description = models.TextField(
        verbose_name=_('Job description')
    )

    company_name = models.CharField(
        max_length=190,
        verbose_name=_('Company name')
    )
    company_description = models.TextField(
        blank=True,
        verbose_name=_('Company description'),
    )
    company_contact = models.TextField(
        verbose_name=_('Contact information'),
        help_text=_('Preferrably, this should include a person to talk to directly at the conference, and also a '
                    'contact option for after the conference.')
    )

    logo = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_('Company logo')
    )

    def __str__(self):
        return '{} at {}'.format(self.job_title, self.company_name)