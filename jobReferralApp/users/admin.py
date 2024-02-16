from django.contrib import admin
from .models import User, Employer, Applicant, Skill, Area

class UserAdmin (admin.ModelAdmin):
    list_display = ['id', 'username']


class ApplicantAdmin (admin.ModelAdmin):
    list_display = ['id', 'user']


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Employer)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Skill)
admin.site.register(Area)