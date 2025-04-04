# from http import HTTPStatus
# from datetime import timedelta

# from django.test import TestCase
# from django.urls import reverse
# from django.utils.timezone import now

# from users.forms import RegistrationForm
# from users.models import User, EmailVerification

# class RegistrationViewTestCase(TestCase):

#     def setUp(self):
#         self.data = {
#             'first_name': 'Valeri', 'last_name': 'Pavlikov',
#             'username': 'valeri', 'email': 'yaperdole26@gmail.com',
#             'password1': '898381286180rv', 'password2': '898381286180rv',
#         }
#         self.path = reverse('users:registration')

#     def test_user_registration_get(self):
#         response = self.client.get(self.path)

#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(response.context_data['title'], 'Store - Регистрация')
#         self.assertTemplateUsed(response, 'users/registration.html')
#         # self.assertEqual(str(response.context_data['form']), str(RegistrationForm()))

#     def test_user_registration_post_success(self):
        
#         username = self.data['username']
#         self.assertFalse(User.objects.filter(username=username).exists())
#         response = self.client.post(self.path, self.data)

#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
#         self.assertRedirects(response, reverse('users:login'))
#         self.assertTrue(User.objects.filter(username=username).exists())
#         email_verification = EmailVerification.objects.filter()
#         self.assertEqual(
#             email_verification.first().expiration.date(),
#             (now() + timedelta(hours=48)).date()
#         )
        



from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserRegistrationForm
from users.models import User, EmailVerification



class UserRegistrationFormTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')

        self.data = {
            'first_name': 'Valeri', 'last_name': 'Pavlikov',
            'username': 'valeri', 'email': 'yaperdole26@gmail.com',
            'password1': '898381286180rv', 'password2': '898381286180rv',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertEqual(str(response.context_data['form']), str(UserRegistrationForm()))
        self.assertTemplateUsed(response, 'users/registration.html')
    
    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)


        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # проверка на создание верификации
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )
    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK) 
        self.assertContains(response, 'A user with that username already exists.')