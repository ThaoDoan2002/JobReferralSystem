from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from jobs.models import RecruitmentPost

class RecruitmentPostFilter(FilterSet):
    career = CharFilter(field_name='career__name', lookup_expr='icontains')
    class Meta:
        model = RecruitmentPost
        fields = {
            'experience': ['icontains'],
            'sex': ['iexact'],
            'workingForm': ['icontains'],
            'area': ['icontains'],
            'wage': ['icontains'],
            'position': ['icontains'],

        }