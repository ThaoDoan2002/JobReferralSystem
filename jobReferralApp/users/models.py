from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True, blank=True)
    phoneNumber = models.CharField(max_length=255)
    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    sex = models.CharField(max_length=50, null=True)

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    information = RichTextField(null=True, blank=True, default="abc")
    address = models.CharField(max_length=255, blank=True, null=True)
    mediaLink = models.CharField(max_length=255, blank=True, null=True)
    companySize = models.IntegerField(blank=True, null=True)

    # xét blank, null = True để khi đăng ký tài khoản thì chỉ điền thông tin cơ bản rồi sau khi đã đăng ký user sẽ vào account của mình để setting

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'companyName')


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Career(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)  # vị trí công việc
    skills = models.ManyToManyField(Skill)
    areas = models.ManyToManyField(Area)
    experience = models.CharField(max_length=255)  # kinh nghiệm theo năm
    wage = models.CharField(max_length=255)  # lương mong muốn
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True, blank=True)
    cv = CloudinaryField('cv', null=True, blank=True)
    #workingform

    def __str__(self):
        return self.user.username


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Interaction(BaseModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('applicant', 'employer')


class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)


