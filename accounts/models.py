from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    is_agent_manager = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
