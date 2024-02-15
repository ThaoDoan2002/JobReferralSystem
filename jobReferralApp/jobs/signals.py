from django.db.models.signals import pre_save
from django.utils import timezone
from .models import RecruitmentPost

def updateRecruitmentPost(sender, instance, **kwargs):
    rePost = instance
    if rePost.expirationDate > timezone.now().date():
        rePost.active = True

pre_save.connect(updateRecruitmentPost, sender=RecruitmentPost)