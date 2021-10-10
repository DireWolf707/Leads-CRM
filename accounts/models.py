from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


def agent_profile_pic(instance, filename):
    return f'agents/{instance.username}/{filename}'


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), unique=True)
    is_agent_manager = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    profile_picture = models.ImageField(
        upload_to=agent_profile_pic, blank=True, null=True
    )
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
