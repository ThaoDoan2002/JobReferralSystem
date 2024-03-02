import mailchimp3

from .models import User, Employer, Applicant
from django.db.models.signals import post_save
from django.core.mail import send_mail

from django.conf import settings


def createUser(sender, instance, created, **kwargs):
    if created:
        if instance.is_employer and not instance.is_applicant:
            admin = User.objects.get(is_superuser=True)
            employer = Employer.objects.create(user=instance)
            employer.user.is_active = False
            employer.user.set_password(instance.password)
            employer.user.save()
            # Gửi email thông báo cho admin
            send_mail(
                'Yêu cầu kích hoạt tài khoản mới',
                f'Một nhà tuyển dụng đã đăng ký và yêu cầu kích hoạt tài khoản mới. Email: {instance.email}',
                '2151013090thao@ou.edu.vn',
                [admin.email],  # admin
                fail_silently=False,
            )

            # Gửi thông báo tới Mailchimp
            # mailchimp_api_key = settings.MAILCHIMP_API_KEY
            # mailchimp_list_id = settings.MAILCHIMP_LIST_ID
            #
            # client = mailchimp3.MailChimp(mailchimp_api_key, 'us17')  # Thay 'us20' bằng data center của bạn
            #
            # subscriber_data = {
            #     'email_address': instance.email,
            #     'status': 'subscribed',
            #     'merge_fields': {
            #         'FNAME': instance.first_name,
            #         'LNAME': instance.last_name,
            #     },
            # }

            # client.lists.members.create(mailchimp_list_id, subscriber_data)

        if instance.is_applicant and not instance.is_employer:
            applicant = Applicant.objects.create(user=instance)
            applicant.user.set_password(instance.password)
            applicant.user.save()

        if instance.is_applicant and instance.is_employer:
            instance.delete()



post_save.connect(createUser, sender=User)

