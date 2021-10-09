from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.db.models.signals import post_save

User = get_user_model()


class AgentManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='agent_manager'
    )

    def __str__(self) -> str:
        return str(self.user)


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='agent'
    )
    agent_manager = models.ForeignKey(
        AgentManager, on_delete=models.CASCADE, related_name='agents'
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
        Agent, on_delete=models.SET_NULL, related_name='agent_leads', null=True, blank=True
    )
    agent_manager = models.ForeignKey(
        AgentManager, on_delete=models.CASCADE, related_name='agent_manager_leads'
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
# TODO add signal to delete AgentManger if User gets deleted

def create_agent_manager(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_agent_manager:
            AgentManager.objects.create(user=instance)


post_save.connect(create_agent_manager, User)
