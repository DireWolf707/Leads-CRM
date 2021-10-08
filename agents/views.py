from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from leads.models import Agent
from .forms import AgentForm
# TODO: add prefetch to db query


class AgentListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        agents = Agent.objects.all()
        context = {'agents': agents}
        return render(request, 'agents/list.html', context=context)


class AgentDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        agent = self.get_object(id)
        context = {'agent': agent}
        return render(request, 'agents/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        agent = self.get_object(id)
        agent.delete()
        return redirect('agents:list')

    def get_object(self, id):
        return get_object_or_404(Agent, id=id)


class AgentCreateUpdateView(LoginRequiredMixin, View):
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
        return self.form_invalid()

    def form_valid(self, form, id):
        if id:
            agent = form.save()
        else:
            agent = form.save(commit=False)
            agent.agent_manager = self.request.user.agent_manager
            agent.save()
        return redirect("agents:detail", agent.id)

    def form_invalid(self):
        pass

    def get_object(self, id):
        return get_object_or_404(Agent, id=id)
