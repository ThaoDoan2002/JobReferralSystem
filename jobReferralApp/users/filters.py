from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from users.models import Applicant, Area

class ApplicantFilter(FilterSet):
    areas = CharFilter(method='filter_areas')
    skills = CharFilter(method='filter_skills')
    career = CharFilter(field_name='career__name', lookup_expr='icontains')

    def filter_areas(self, queryset, name, value):
        # Phân tách các khu vực được nhập
        areas = [a.strip() for a in value.split(',')]
        # Tạo một Q object để chứa các điều kiện OR cho mỗi khu vực
        q_objects = Q()
        for area in areas:
            q_objects |= Q(areas__name__icontains=area)
        # Lọc ứng viên có ít nhất một khu vực khớp với danh sách được chỉ định
        return queryset.filter(q_objects)

    def filter_skills(self, queryset, name, value):
        # Phân tách các khu vực được nhập
        skills = [a.strip() for a in value.split(',')]
        # Tạo một Q object để chứa các điều kiện OR cho mỗi khu vực
        q_objects = Q()
        for skill in skills:
            q_objects |= Q(skills__name__icontains=skill)
        # Lọc ứng viên có ít nhất một khu vực khớp với danh sách được chỉ định
        return queryset.filter(q_objects)

    class Meta:
        model = Applicant
        fields = {
            'position': ['icontains'],
            'experience':['icontains'],
            'wage': ['icontains']
        }