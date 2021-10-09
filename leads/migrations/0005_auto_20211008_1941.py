# Generated by Django 3.2.8 on 2021-10-08 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leads', '0004_lead_agent_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lead',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_leads', to='leads.agent'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='agent_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_manager_leads', to='leads.agentmanager'),
        ),
    ]