from django.urls import path
from .views import LeadListView, LeadDetailView

app_name = 'leads'

urlpatterns = [
    path('all/', LeadListView.as_view(), name='list'),
    path('<int:id>/', LeadDetailView.as_view(), name='detail'),
]
