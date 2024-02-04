from .models import User, Employer, Applicant
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings


def createEmployer(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer:
            employer = Employer.objects.create(user=instance)
            employer.user.is_active = False
            employer.user.set_password(instance.password)
            employer.user.save()

            send_mail(
                "Active Employer Account",
                "Please active soon.",
                settings.EMAIL_HOST_USER,
                [instance.email],
                fail_silently=False,
            )


def createApplicant(sender, instance, created, **kwargs):
    if created:
        if instance.is_applicant:
            applicant = Applicant.objects.create(user=instance)
            applicant.user.set_password(instance.password)
            applicant.user.save()



post_save.connect(createEmployer, sender=User)
post_save.connect(createApplicant, sender=User)

