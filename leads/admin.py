from django.contrib import admin
from .models import Lead, Agent, AgentManager
admin.site.register(AgentManager)
admin.site.register(Agent)
admin.site.register(Lead)
