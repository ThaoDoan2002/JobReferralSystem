from django.db.models import Count
from django.db.models.functions import ExtractQuarter, ExtractYear

from jobs.models import JobApplication


def count_applyJob_by_career():
    return JobApplication.objects.annotate(quarter=ExtractQuarter('testdate'),
                                           year=ExtractYear('testdate')).values('recruitment__career__name',
                                                                                    'quarter', 'year').annotate(
        count=Count('id'))
