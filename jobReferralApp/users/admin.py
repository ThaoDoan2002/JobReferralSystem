from django.contrib import admin
from .models import User, Employer, Applicant

# Register your models here.
admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Applicant)