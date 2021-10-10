from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from django.contrib import messages
from .models import Lead
from django.shortcuts import get_object_or_404
from .forms import LeadForm
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import AgentManagerAndLoginRequiredMixin


class HomeView(View):
    def get(self, request, *args, **kwargs):
        """Returns home page"""
        return render(request, 'home.html')


class LeadListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Returns leads list related to logged in agent or agent manager"""
        user = self.request.user
        context = dict()
        leads = Lead.objects.all()
        # if agent query contacted and uncontacted leads
        if user.is_agent:
            agent = user.agent
            context["contacted_leads"] = leads.filter(
                agent=agent, contacted=True
            )
            context["uncontacted_leads"] = leads.filter(
                agent=agent, contacted=False
            )
            return render(request, 'leads/agent_leads_list.html', context=context)
        # if agent manager query assigned and unassigned leads
        else:
            agent_manager = user.agent_manager
            context["assigned_leads"] = leads.filter(
                agent_manager=agent_manager, agent__isnull=False
            )
            context["unassigned_leads"] = Lead.objects.filter(
                agent_manager=agent_manager, agent__isnull=True
            )
            return render(request, 'leads/agent_manager_leads_list.html', context=context)


class LeadDetailDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Returns lead details and id"""
        id = kwargs['id']
        lead = self.get_object(id)
        context = {'lead': lead, 'id': id}
        return render(request, 'leads/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        """Deletes lead if user is an agent manager and redirects to leads list"""

        # Permission check
        if not request.user.is_agent_manager:
            return self.handle_no_permission()
        id = kwargs['id']
        lead = self.get_object(id)
        lead.delete()
        return redirect('leads:list')

    def get_object(self, id):
        """Returns the lead and checks if it belongs to logged in agent or agent manager respectively"""
        user = self.request.user
        # if agent
        if user.is_agent:
            lead = get_object_or_404(Lead, id=id, agent=user.agent)
        # if agent manager
        else:
            lead = get_object_or_404(
                Lead, id=id, agent_manager=user.agent_manager
            )
        return lead

    def handle_no_permission(self):
        """Raise PermissionDenied Error"""
        raise PermissionDenied()


class LeadCreateUpdateView(AgentManagerAndLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        """Returns lead form and id"""

        form, id = self.get_form()
        return render(request, 'leads/form.html', context={'form': form, 'id': id})

    def post(self, request, *args, **kwargs):
        """Validates submitted form and redirect to lead detail page"""

        form, id = self.get_form()
        if form.is_valid():
            return self.form_valid(form, id)
        return self.form_invalid(form, id)

    def form_valid(self, form, id):
        """Save the valid form"""

        instance = form.save(commit=False)
        # if lead create, assign current logged in agent manager to the lead and send confirmation mail
        if not id:
            instance.agent_manager = self.agent_manager
            send_mail(subject="A lead has been created", message="Go to site to see the new Lead",
                      from_email=None, recipient_list=[self.request.user.email])
        # if lead update, just save the changes
        instance.save()
        return redirect('leads:detail', instance.id)

    def form_invalid(self, form, id):
        """Return invalid form errors"""

        errors = form.errors.as_data()
        for i in errors:
            messages.error(self.request, f'{i}: {list(errors[i][0])[0]}')
        # if update lead redirect to lead detail view
        if id:
            return redirect("leads:detail", id)
        # if create lead redirect to leads list view
        return redirect("leads:list")

    def get_object(self, id):
        """Returns the lead and checks if it belongs to logged in Agent manager"""

        lead = get_object_or_404(
            Lead, id=id, agent_manager=self.agent_manager
        )
        return lead

    def get_form(self):
        """Returns empty or prepopulated lead form and id depending upon create or update operation"""

        self.agent_manager = self.request.user.agent_manager
        id = self.kwargs.get('id')
        instance = None
        # if udpate lead, query the corresponding lead instance to populate form
        if id:
            instance = self.get_object(id)
        # generate form depending upon data
        form = LeadForm(
            self.agent_manager, data=self.request.POST or None, files=self.request.FILES or None, instance=instance
        )
        return form, id


class LeadContactView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        """Changes contacted status of lead and redirect to leads list"""
        contacted = self.request.POST.get('contacted')
        # check if POST data have contacted value and if user is an agent
        if contacted and request.user.is_agent:
            contacted = True if contacted == 'true' else False
            # query to update lead contacted status if lead belong to the logged in user
            Lead.objects.filter(
                id=kwargs['id'], agent=request.user.agent
            ).update(contacted=contacted)
        return redirect('leads:list')
