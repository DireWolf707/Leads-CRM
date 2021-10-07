from django.views.generic import CreateView
from django.contrib.auth.views import LoginView as BaseLoginView
from .forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login

# TODO: send mail on successful signup


class SignupView(CreateView):
    template_name = 'accounts/accounts.html'
    form_class = UserCreationForm
    extra_context = {'type': 'Signup'}

    def form_valid(self, form):
        """If the form is valid, save the associated model and login the user"""
        self.object = form.save()
        login(self.request, self.object)
        return redirect('leads:list')


class LoginView(BaseLoginView):
    template_name = 'accounts/accounts.html'
    extra_context = {'type': 'Login'}
