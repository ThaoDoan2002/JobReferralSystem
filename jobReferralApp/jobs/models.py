from django.db import models
from users.models import Employer, Area, Applicant, Career
from ckeditor.fields import RichTextField


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class RecruitmentPost(BaseModel):
    employer = models.ForeignKey(Employer, models.CASCADE)
    title = models.CharField(max_length=255)
    experience = models.CharField(max_length=255,null=True,default="1 năm")
    expirationDate = models.DateField(null=True, blank=True, default="2025-01-20")
    description = RichTextField(null=True,blank=True,default="BCS")
    quantity = models.IntegerField(null=True,default="1")
    sex = models.CharField(max_length=50,null=True,default="ABC")
    workingForm = models.CharField(max_length=255,null=True,default="ABC")
    area = models.CharField(max_length=255,null=True,default="ABC")
    wage = models.CharField(max_length=255,null=True,default="ABC")
    position = models.CharField(max_length=255,null=True,default="ABC")
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('employer', 'title')
        ordering = ['-created_date']



class JobApplication(BaseModel):
    recruitment = models.ForeignKey(RecruitmentPost, models.RESTRICT, null=Trues)  # luu tru thi khong nen cascade => RESTRICT
    applicant = models.ForeignKey(Applicant, models.RESTRICT)
    coverLetter = models.CharField(max_length=255, null=True,blank=True)

    class Meta:
        unique_together = ('recruitment', 'applicant')

    def __str__(self):
        return self.recruitment.title + ", " + self.applicant.user.username + " apply"


