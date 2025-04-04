from allauth.socialaccount.models import SocialApp

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.shortcuts import render

from common.views import TitleMixin
from users.models import User, EmailVerification
from .forms import (LoginForm, UserRegistrationForm,
                    UserProfileForm)


class UserLoginView(TitleMixin, LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    title = 'Store - Авторизация'

    def get_context_data(self, *args, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context['github_enabled'] = SocialApp.objects.filter(provider="github").exists()
        return context


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрированы!'

    title = 'Store - Регистрация'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


# This class handles email verification for users in a web application.
class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, **kwargs):
        code = kwargs.get('code')
        email = kwargs.get('email')

        user = get_object_or_404(User, email=email)
        email_verification = EmailVerification.objects.filter(user=user, code=code).first()

        if email_verification:
            if email_verification.is_expired():
                user.delete()
                messages.error(request, 'Ссылка истекла! Зарегистрируйтесь снова')
            else:
                user.is_verified_email = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')                
                return render(request, self.template_name)
        else:
            messages.error(request, 'Ошибка')

        return HttpResponseRedirect(reverse('users:login'))


# def registration(request):
#     if request.method == 'POST':
#         form = RegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your account was successfully created!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = RegistrationForm()
#     context = {'title': 'Registration', 'form': form}

#     return render(request, 'users/registration.html', context)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     baskets = Basket.objects.filter(user=request.user)
#     context = {'form': form, 'baskets': baskets}
#     return render(request, 'users/profile.html', context)
