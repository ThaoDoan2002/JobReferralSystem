from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Employer, Applicant, Skill, Area, Career, Comment, Rating
from ckeditor_uploader.widgets \
    import CKEditorUploadingWidget
from django import forms

# from jobs.admin import admin_site

from import_export.admin import  ImportExportModelAdmin


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['id']

class UserAdmin(ImportExportModelAdmin):
    list_display = ['id', 'username']
    form = UserForm



class ApplicantAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

class EmployerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']





# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Skill)
admin.site.register(Area, ImportExportModelAdmin)
admin.site.register(Career)
admin.site.register(Comment)
admin.site.register(Rating)
