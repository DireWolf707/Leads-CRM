from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name",
                  "last_name", "email",)
        field_classes = {'username': UsernameField}
