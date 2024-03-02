import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    avatar = CloudinaryField('avatar')
    phoneNumber= PhoneNumberField(region="VN",null=True)
    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)
    sex = models.CharField(max_length=50)
    email = models.EmailField(unique=True)



class Employer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255,unique=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    information = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mediaLink = models.CharField(max_length=255, blank=True, null=True)
    companySize = models.IntegerField(blank=True, null=True)


    # xét blank, null = True để khi đăng ký tài khoản thì chỉ điền thông tin cơ bản rồi sau khi đã đăng ký user sẽ vào account của mình để setting

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'companyName')


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Area(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Career(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, null=True, blank=True)  # vị trí công việc
    skills = models.ManyToManyField(Skill)
    areas = models.ManyToManyField(Area)
    experience = models.CharField(max_length=255, null=True, blank=True)  # kinh nghiệm theo năm
    wage = models.CharField(max_length=255, null=True, blank=True)  # lương mong muốn
    career = models.ForeignKey(Career, on_delete=models.RESTRICT, null=True, blank=True)
    cv = CloudinaryField('cv', null=True, blank=True)
    workingForm = models.CharField(max_length=255,null=True, blank=True)


    def __str__(self):
        return self.user.username


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Interaction(BaseModel):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Comment(Interaction):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.content



class Like(Interaction):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('applicant', 'employer')


class Rating(Interaction):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    rate = models.SmallIntegerField(default=0)
    class Meta:
        unique_together = ('applicant', 'employer')



