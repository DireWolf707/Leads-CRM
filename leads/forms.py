from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    def __init__(self, agent_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['agent'].queryset = agent_manager.agents

    class Meta:
        model = Lead
        exclude = ('agent_manager', 'contacted')
