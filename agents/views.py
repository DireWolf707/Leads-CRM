from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from django.views import View
from django.forms import modelform_factory
from django.core.mail import send_mail
from django.contrib import messages
from leads.models import Agent
from .mixins import AgentManagerAndLoginRequiredMixin

User = get_user_model()


class AgentListView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Return agents belonging to the logged in Agent manager"""
        agents = Agent.objects.filter(agent_manager__user=request.user)
        context = {'agents': agents}
        return render(request, 'agents/list.html', context=context)


class AgentDetailDeleteView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Return agent from unique ID"""
        id = kwargs.get('id')
        agent = self.get_object(id)
        context = {'agent': agent.user, 'id': id}
        return render(request, 'agents/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        """Deletes agent and corresponding user instance"""
        id = kwargs['id']
        agent = self.get_object(id)
        agent.user.delete()
        agent.delete()
        return redirect('agents:list')

    def get_object(self, id):
        """Returns the agent and checks if it belongs to logged in Agent manager"""
        return get_object_or_404(Agent, id=id, agent_manager=self.request.user.agent_manager)


class AgentCreateUpdateView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Returns agent form and id"""
        form, id = self.get_form()
        context = {'form': form, 'id': id}
        return render(self.request, 'agents/form.html', context=context)

    def post(self, request, *args, **kwargs):
        """Validates submitted form and redirect to agent detail page"""
        form, id = self.get_form()
        if form.is_valid():
            return self.form_valid(form, id)
        return self.form_invalid(form, id)

    def form_valid(self, form, id):
        """Save the valid form"""

        # if update agent, simply save form
        if id:
            user = form.save()
            agent = self.agent
        # if create agent, create a user instance related to this agent and send mail to the new agent with username and password
        else:
            user = form.save(commit=False)
            user.is_agent = True
            user.is_agent_manager = False
            password = get_random_string(12)
            user.set_password(password)
            user.save()
            agent = Agent.objects.create(
                user=user, agent_manager=self.request.user.agent_manager
            )
            send_mail(subject="Hello Agent", message=f"Your agent account has been successfully created with username: {user.username} and password: {password}",
                      from_email=None, recipient_list=[user.email])
        return redirect("agents:detail", agent.id)

    def form_invalid(self, form, id):
        """Return invalid form errors"""

        errors = form.errors.as_data()
        for i in errors:
            messages.error(self.request, f'{i}: {list(errors[i][0])[0]}')
        # if update agent redirect to agent detail view
        if id:
            return redirect("agents:detail", id)
        # if create agent redirect to agents list view
        return redirect("agents:list")

    def get_object(self, id):
        """Returns the agent and checks if it belongs to logged in Agent manager"""
        self.agent = get_object_or_404(
            Agent, id=id, agent_manager=self.request.user.agent_manager
        )
        return self.agent.user

    def get_form(self):
        """Returns empty or prepopulated agent form and id depending upon create or update operation"""
        instance = None
        id = self.kwargs.get('id')
        # if update agent, query the corresponding agent instance to populate form
        if id:
            # don't include email
            AgentForm = modelform_factory(User, fields=(
                'username', 'first_name', 'last_name', 'profile_picture')
            )
            instance = self.get_object(id)
        # if create agent
        else:
            # include email
            AgentForm = modelform_factory(User, fields=('email', 'username',
                                                        'first_name', 'last_name', 'profile_picture')
                                          )
        # generate form depending upon data
        form = AgentForm(data=self.request.POST or None,
                         files=self.request.FILES or None, instance=instance)
        return form, id
