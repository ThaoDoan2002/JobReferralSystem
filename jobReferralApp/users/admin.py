from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Employer, Applicant, Skill, Area, Career, Comment, Like,Rating
from ckeditor_uploader.widgets \
    import CKEditorUploadingWidget
from django import forms



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
admin.site.register(User, UserAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Skill)
admin.site.register(Area)
admin.site.register(Career)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
