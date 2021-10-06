from django.shortcuts import render
from django.views.generic import View
from .models import Lead
from django.shortcuts import get_object_or_404


class LeadListView(View):
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.all()
        context = {'leads': leads}
        return render(request, 'leads/list.html', context=context)


class LeadDetailView(View):
    def get(self, request, *args, **kwargs):
        lead = get_object_or_404(Lead, id=kwargs['id'])
        context = {'lead': lead}
        return render(request, 'leads/detail.html', context=context)
