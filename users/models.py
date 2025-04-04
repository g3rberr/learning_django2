# import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "store.settings")


from django.contrib.auth.models import AbstractUser


from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.template.loader import render_to_string


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        html_content = render_to_string(
            'users/send_email.html',
            context={'link': verification_link}
        )
        text_message = 'Пожалуйста, подтвердите ваш email.'
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=(self.user.email,),
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


    def is_expired(self):
        return True if now() >= self.expiration else False

