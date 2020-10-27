from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class Employer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username


# Django Signals
@receiver(post_save, sender=User)
def create_employer(sender, instance, created, **kwargs):
    if created:
        Employer.objects.create(user=instance)
        send_mail_registration(user=instance)


# Mail Service
def send_mail_registration(user):
    subject = 'Account Registration'
    html_message = render_to_string('mail/mail_register.html', {'user': user})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_EMAIL
    to = user.email

    send_mail(subject, plain_message, from_email, [to], html_message=html_message)
