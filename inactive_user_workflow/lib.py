from django.core.mail import send_mail

from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from django.conf import settings

from registration.models import RegistrationProfile
from django.contrib.auth.models import User

def resend_mail(username, send=True):
    user = User.objects.get(username=username)
    assert user.is_active == False

    registration_profile = RegistrationProfile.objects.get(user=user)

    current_site = Site.objects.get_current()
    
    subject = render_to_string('registration/activation_email_subject.txt',
                               { 'site': current_site })
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string('registration/activation_email.txt',
                               { 'activation_key': registration_profile.activation_key,
                                 'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                 'site': current_site })

    if send is True:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return message, user.email
