from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string

User = get_user_model()


class AgentManager(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='agent_manager'
    )

    def __str__(self) -> str:
        """Returns string value"""
        return str(self.user)


class Agent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='agent'
    )
    agent_manager = models.ForeignKey(
        AgentManager, on_delete=models.CASCADE, related_name='agents'
    )

    def __str__(self) -> str:
        """Returns string value"""
        return str(self.user)


def lead_profile_pic(instance, filename):
    return f'leads/{instance.get_full_name()} #{get_random_string(10)}/{filename}'


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
    description = models.TextField(blank=False, null=False)
    cell_phone = models.CharField(max_length=20)
    profile_picture = models.ImageField(
        upload_to=lead_profile_pic, blank=True, null=True
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
        """Returns string value"""
        return self.get_full_name()

    def get_absolute_url(self):
        """
        Return absolute url for the lead
        """
        return reverse("leads:detail", kwargs={"id": self.id})


@receiver(post_save, sender=User)
def create_agent_manager(sender, instance, created, *args, **kwargs):
    if created:
        if instance.is_agent_manager:
            AgentManager.objects.create(user=instance)


@receiver(post_delete, sender=Lead)
@receiver(post_delete, sender=User)
def delete_profile_pic(sender, instance, *args, **kwargs):
    instance.profile_picture.delete(save=False)
