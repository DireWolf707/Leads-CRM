# Generated by Django 3.2.8 on 2021-10-10 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import leads.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='AgentManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('age', models.PositiveIntegerField(default=0)),
                ('contacted', models.BooleanField(default=False)),
                ('source', models.CharField(choices=[('YT', 'Youtube'), ('G', 'Google'), ('NL', 'Newsletter')], default='YT', max_length=2)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=leads.models.lead_profile_pic)),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_leads', to='leads.agent')),
                ('agent_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agent_manager_leads', to='leads.agentmanager')),
            ],
        ),
        migrations.AddField(
            model_name='agent',
            name='agent_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='leads.agentmanager'),
        ),
        migrations.AddField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
    ]
