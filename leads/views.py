from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.views.generic import View
from .models import Lead
from django.shortcuts import get_object_or_404
from .forms import LeadForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')


class LeadListView(View):
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.all()
        context = {'leads': leads}
        return render(request, 'leads/list.html', context=context)


class LeadDetailView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        lead = self.get_object(id)
        context = {'lead': lead, 'id': id}
        return render(request, 'leads/detail.html', context=context)

    def post(self, request, *args, **kwargs):
        id = kwargs['id']
        lead = self.get_object(id)
        lead.delete()
        return redirect('leads:list')

    def get_object(self, id):
        lead = get_object_or_404(Lead, id=id)
        return lead


# TODO: CHECK FOR IMAGE UPLOAD/CHANGE
# TODO: Change/add django message to Form invalid/valid
class LeadCreateUpdateView(View):
    def get(self, request, *args, **kwargs):
        instance = None
        id = kwargs.get('id')
        if id:
            instance = self.get_object(id)
        form = LeadForm(instance=instance)
        return self.render_template(form, id)

    def post(self, request, *args, **kwargs):
        instance = None
        id = kwargs.get('id')
        if id:
            instance = self.get_object(id)
        form = LeadForm(request.POST, instance=instance)
        if form.is_valid():
            return self.is_valid(form, id)
        return self.is_invalid(form, id)

    def is_valid(self, form, id):
        if not id:
            send_mail(subject="A lead has been created", message="Go to site to see the new Lead", from_email=None, recipient_list=['test_user@mail.com'],
                      fail_silently=False)
        instance = form.save()
        return redirect('leads:detail', instance.id)

    def is_invalid(self, form, id):
        return self.render_template(form, id)

    def render_template(self, form, id):
        return render(self.request, 'leads/form.html', context={'form': form, 'id': id})

    def get_object(self, id):
        lead = get_object_or_404(Lead, id=id)
        return lead
