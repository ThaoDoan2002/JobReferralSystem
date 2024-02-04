from django.db import models
from users.models import Employer, Area, Applicant

class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Recruitment(BaseModel):
    employer = models.ForeignKey(Employer, models.CASCADE)
    title = models.CharField(max_length=255)
    #experience
    expirationDate = models.DateField()
    description = models.TextField()
    quantity = models.IntegerField()
    sex = models.CharField(max_length=50)
    workingForm = models.CharField(max_length=255)
    # carrers = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True) #nhớ sửa lại sau khi xong
    areas = models.ManyToManyField(Area)

    def __str__(self):
        return self.title


class JobApplication(BaseModel):
    description = models.TextField(null=True)
    jobPost = models.ForeignKey(Recruitment, models.RESTRICT) #luu tru thi khong nen cascade => RESTRICT
    applicant = models.ForeignKey(Applicant, models.RESTRICT)

    def __str__(self):
        return self.job.title





