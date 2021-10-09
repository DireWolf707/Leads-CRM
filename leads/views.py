from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from .models import Lead
from django.shortcuts import get_object_or_404
from .forms import LeadForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import AgentManagerAndLoginRequiredMixin


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class LeadListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'leads/list.html', context=context)

    def get_context_data(self):
        user = self.request.user
        context = dict()
        leads = Lead.objects.all()
        if user.is_agent:
            context["leads"] = leads.filter(agent=user.agent)
        else:
            context["leads"] = leads.filter(
                agent_manager=user.agent_manager, agent__isnull=False
            )
            context["unassigned_leads"] = Lead.objects.filter(
                agent_manager=user.agent_manager, agent__isnull=True
            )
        return context


class LeadDetailDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        lead = self.get_object(id)
        context = {'lead': lead, 'id': id}
        return render(request, 'leads/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_agent_manager:
            return self.handle_no_permission()
        id = kwargs['id']
        lead = self.get_object(id)
        lead.delete()
        return redirect('leads:list')

    def get_object(self, id):
        user = self.request.user
        if user.is_agent:
            lead = get_object_or_404(Lead, id=id, agent=user.agent)
        else:
            lead = get_object_or_404(
                Lead, id=id, agent_manager=user.agent_manager
            )
        return lead

    def handle_no_permission(self):
        raise PermissionDenied()


# TODO: CHECK FOR IMAGE UPLOAD/CHANGE
# TODO: Change/add django message to Form invalid/valid
class LeadCreateUpdateView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form, id = self.get_form()
        return render(request, 'leads/form.html', context={'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        form, id = self.get_form()
        if form.is_valid():
            return self.is_valid(form, id)
        return self.is_invalid(form, id)

    def is_valid(self, form, id):
        instance = form.save(commit=False)
        if not id:
            instance.agent_manager = self.agent_manager
            send_mail(subject="A lead has been created", message="Go to site to see the new Lead", from_email=None, recipient_list=[self.request.user.email],
                      fail_silently=False)
        instance.save()
        return redirect('leads:detail', instance.id)

    def is_invalid(self, form, id):
        pass

    def get_object(self, id):
        lead = get_object_or_404(
            Lead, id=id, agent_manager=self.agent_manager
        )
        return lead

    def get_form(self):
        self.agent_manager = self.request.user.agent_manager
        id = self.kwargs.get('id')
        instance = None
        if id:
            instance = self.get_object(id)
        form = LeadForm(
            self.agent_manager, data=self.request.POST or None, instance=instance
        )
        return form, id
