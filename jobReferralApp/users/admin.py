from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Employer, Applicant, Skill, Area, Career, Comment, Rating
from ckeditor_uploader.widgets \
    import CKEditorUploadingWidget
from django import forms

from jobs.admin import admin_site


class EmployerForm(forms.ModelForm):
    information = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Employer
        fields = '__all__'


class EmployerAdmin(admin.ModelAdmin):
    form = EmployerForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


# Register your models here.
admin_site.register(User, UserAdmin)
admin_site.register(Employer, EmployerAdmin)
admin_site.register(Applicant, ApplicantAdmin)
admin_site.register(Skill)
admin_site.register(Area)
admin_site.register(Career)
admin_site.register(Comment)
admin_site.register(Rating)
