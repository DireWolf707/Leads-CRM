from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.views import View
from django.forms import modelform_factory
from leads.models import Agent
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
class AgentCreateUpdateView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form, id = self.get_form()
        context = {'form': form, 'id': id}
        return render(self.request, 'agents/form.html', context=context)

    def post(self, request, *args, **kwargs):
        form, id = self.get_form()
        if form.is_valid():
            return self.form_valid(form, id)
        return self.form_invalid(form)

    def form_valid(self, form, id):
        if id:
            user = form.save()
            agent = self.agent
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
        pass

    def get_object(self, id):
        self.agent = get_object_or_404(
            Agent, id=id, agent_manager=self.request.user.agent_manager
        )
        return self.agent.user

    def get_form(self):
        instance = None
        id = self.kwargs.get('id')
        if id:
            AgentForm = modelform_factory(User, fields=(
                'username', 'first_name', 'last_name')
            )
            instance = self.get_object(id)
        else:
            AgentForm = modelform_factory(User, fields=('email', 'username',
                                                        'first_name', 'last_name')
                                          )
        form = AgentForm(data=self.request.POST or None, instance=instance)
        return form, id
