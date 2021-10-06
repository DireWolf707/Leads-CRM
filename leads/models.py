from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse

User = get_user_model()


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_agent'
    )

    def __str__(self) -> str:
        return str(self.user)


def profile_pic(instance, filename):
    return f'profile/{instance.get_full_name()} #{get_random_string(length=10)}/{filename}'


class Lead(models.Model):
    class Source(models.TextChoices):
        YOUTUBE = 'YT', 'Youtube'
        GOOGLE = 'G', 'Google'
        NEWSLETTER = 'NL', 'Newsletter'

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.PositiveIntegerField(default=0)
    contacted = models.BooleanField(default=False)
    source = models.CharField(max_length=2, choices=Source.choices,
                              default=Source.YOUTUBE)
    profile_picture = models.ImageField(
        upload_to=profile_pic, blank=True, null=True
    )
    agent = models.ForeignKey(
        Agent, on_delete=models.SET_NULL, related_name='leads', null=True
    )

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.get_full_name()

    def get_absolute_url(self):
        """
        Return absolute url for the lead
        """
        return reverse("leads:detail", kwargs={"id": self.id})


# TODO add signal to delete profile pic if Lead gets deleted
