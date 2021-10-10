from django.urls.base import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import views
from .forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.core.mail import send_mail


class SignupView(CreateView):
    template_name = 'accounts/accounts.html'
    form_class = UserCreationForm
    extra_context = {'type': 'Signup'}

    def form_valid(self, form):
        """If the form is valid, save the associated model and login the user and send mail"""
        self.object = form.save()
        login(self.request, self.object)
        send_mail(subject="New Signup", message="Your account has been successfully created",
                  from_email=None, recipient_list=[self.object.email])
        return redirect('leads:list')


class LoginView(views.LoginView):
    template_name = 'accounts/accounts.html'
    extra_context = {'type': 'Login'}


class PasswordResetView(views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/mail/password_reset_email.html'
    subject_template_name = 'accounts/mail/password_reset_subject.txt'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'accounts/password_reset_confirm.html'
