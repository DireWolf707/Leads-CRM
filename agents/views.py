from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.views import View
from leads.models import Agent
from .forms import AgentForm
from .mixins import AgentManagerAndLoginRequiredMixin

User = get_user_model()


# TODO: add prefetch to db query
class AgentListView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        agents = Agent.objects.filter(agent_manager=request.user.agent_manager)
        context = {'agents': agents}
        return render(request, 'agents/list.html', context=context)


class AgentDetailDeleteView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        agent = self.get_object(id)
        context = {'agent': agent}
        return render(request, 'agents/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        agent = self.get_object(id)
        agent.user.delete()
        agent.delete()
        return redirect('agents:list')

    def get_object(self, id):
        return get_object_or_404(Agent, id=id, agent_manager=self.request.user.agent_manager)


# TODO: CHECK FOR IMAGE UPLOAD/CHANGE
# TODO: Change/add django message to Form invalid/valid
# TODO: Refactor Code to use dispatch
class AgentCreateUpdateView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        instance = None
        if id:
            instance = self.get_object(id)
        form = AgentForm(instance=instance)
        context = {'form': form, 'id': id}
        return render(self.request, 'agents/form.html', context=context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        instance = None
        if id:
            instance = self.get_object(id)
        form = AgentForm(request.POST, instance=instance)
        if form.is_valid():
            return self.form_valid(form, id)
        return self.form_invalid(form)

    def form_valid(self, form, id):
        if id:
            user = form.save()
            agent = user.agent
        else:
            user = form.save(commit=False)
            user.is_agent = True
            user.is_agent_manager = False
            user.set_password(get_random_string(12))
            user.save()
            agent = Agent.objects.create(
                user=user, agent_manager=self.request.user.agent_manager
            )
            # TODO: Send mail to new agent with the random password
        return redirect("agents:detail", agent.id)

    def form_invalid(self, form):
        print(form)
        pass

    def get_object(self, id):
        agent = get_object_or_404(
            Agent, id=id, agent_manager=self.request.user.agent_manager
        )
        return agent.user
