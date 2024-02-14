from django.db import models
from users.models import Employer, Area, Applicant

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class RecruitmentPost(BaseModel):
    employer = models.ForeignKey(Employer, models.CASCADE)
    title = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    expirationDate = models.DateField()
    description = models.TextField()
    quantity = models.IntegerField()
    sex = models.CharField(max_length=50)
    workingForm = models.CharField(max_length=255)
    carrer = models.CharField(max_length=255)
    area = models.CharField(max_length=255)
    wage = models.CharField(max_length=255)
    position = models.CharField(max_length=255)



    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']




class JobApplication(BaseModel):
    recruitment = models.ForeignKey(RecruitmentPost, models.RESTRICT, null=True) #luu tru thi khong nen cascade => RESTRICT
    applicant = models.ForeignKey(Applicant, models.RESTRICT)
    cv = models.CharField(max_length=255, null=True) #tai file docx, pdf
    def __str__(self):
        return self.applicant.user.username + self.recruitment.title





