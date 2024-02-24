from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from jobs import dao

from .models import JobApplication, RecruitmentPost


class JobApplicationAdminSite(admin.AdminSite):
    site_header = 'iLoveWork'

    def get_urls(self):
        return [
            path('jobApplication-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/stats.html',{
            'stats': dao.count_applyJob_by_career()
        })


admin_site = JobApplicationAdminSite(name="myapp")


admin_site.register(JobApplication)
admin_site.register(RecruitmentPost)
