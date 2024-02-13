from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from enum import Enum


class CareerChoices(Enum):
    CHOOSE_CAREER = 'Tất cả ngành nghề'
    KD_BH = 'Kinh doanh / Bán hàng'
    B_PD = 'Biên / Phiên dịch'
    BC_TH = 'Báo chí / Truyền hình'
    BC_VT = 'Bưu chính - Viễn thông'
    BH = 'Bảo hiểm'
    BDS = 'Bất động sản'
    CK_V_NT = 'Chứng khoán / Vàng / Ngoại tệ'
    CNTT = 'Công nghệ thông tin'
    CK_CT_TDH = 'Cơ khí / Chế tạo / Tự động hóa'
    DL = 'Du lịch'


class ExperienceChoices(Enum):
    CHOOSE_EXPERIENCE = "Tất cả kinh nghiệm"
    NONE = "Chưa có kinh nghiệm"
    LESS_A_YEAR = "Dưới 1 năm"
    A_YEAR = "1 năm"
    TWO_YEAR = "2 năm"
    THREE_YEAR = "3 năm"
    FOUR_YEAR = "4 năm"
    FIVE_YEAR = "5 năm"
    G_FIVE_YEAR = "Trên 5 năm"


class WageChoices(Enum):
    CHOOSE_WAGE = "Tất cả mức lương"
    L_10M = "Dưới 10 triệu"
    G_10M_L_15M = "10 - 15 triệu"
    G_15M_L_20M = "15 - 20 triệu"
    G_20M_L_25M = "20 - 25 triệu"
    G_25M_L_30M = "25 - 30 triệu"
    G_30M_L_50M = "30 - 50 triệu"
    G_50M = "Trên 50 triệu"
    DEAL = "Thỏa thuận"



class User (AbstractUser):
    avatar = CloudinaryField('avatar', null=True)
    phoneNumber = models.CharField(max_length=255)
    is_employer = models.BooleanField(default=False)
    is_applicant = models.BooleanField(default=False)


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyName = models.CharField(max_length=255,blank=True, null=True)
    position = models.CharField(max_length=255,blank=True, null=True)
    information = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    mediaLink = models.CharField(max_length=255,blank=True, null=True)
    companySize = models.IntegerField(blank=True, null=True)
    workingForm = models.CharField(max_length=50,blank=True, null=True)
    #xét blank, null = True để khi đăng ký tài khoản thì chỉ điền thông tin cơ bản rồi sau khi đã đăng ký user sẽ vào account của mình để setting

    def __str__(self):
        return self.user.username



class Skill (models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Applicant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=50)
    career = models.CharField(max_length=50, choices=[(c.value, c.value) for c in CareerChoices], default=CareerChoices.CHOOSE_CAREER.value)
    position = models.CharField(max_length=255)
    skills = models.ManyToManyField(Skill)
    experience = models.CharField(max_length=50, choices=[(e.value, e.value) for e in ExperienceChoices], default=ExperienceChoices.CHOOSE_EXPERIENCE.value)
    wage = models.CharField(max_length=50, choices=[(w.value, w.value) for w in WageChoices], default=WageChoices.CHOOSE_WAGE.value)
    area = models.ManyToManyField(Area)

    def __str__(self):
        return self.user.username

