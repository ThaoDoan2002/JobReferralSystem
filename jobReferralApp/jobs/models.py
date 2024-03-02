import uuid

from django.db import models
from django.utils.text import slugify
from users.models import Employer, Area, Applicant, Career


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class RecruitmentPost(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    employer = models.ForeignKey(Employer, models.CASCADE)
    title = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    expirationDate = models.DateField()
    description = models.TextField(null=True,blank=True)
    quantity = models.IntegerField()
    sex = models.CharField(max_length=50)
    workingForm = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    wage = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    career = models.ForeignKey(Career, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('employer', 'title')
        ordering = ['-created_date']



class JobApplication(BaseModel):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    testdate = models.DateTimeField(null=True)
    recruitment = models.ForeignKey(RecruitmentPost, models.RESTRICT, null=True)  # luu tru thi khong nen cascade => RESTRICT
    applicant = models.ForeignKey(Applicant, models.RESTRICT)
    coverLetter = models.CharField(max_length=255, null=True,blank=True)

    class Meta:
        unique_together = ('recruitment', 'applicant')

    def __str__(self):
        return self.recruitment.title + ", " + self.applicant.user.username + " apply"


