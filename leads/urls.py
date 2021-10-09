from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('all/', views.LeadListView.as_view(), name='list'),
    path('<int:id>/', views.LeadDetailDeleteView.as_view(), name='detail'),
    path('create/', views.LeadCreateUpdateView.as_view(), name='create'),
    path('<int:id>/update/', views.LeadCreateUpdateView.as_view(), name='update'),
    path('<int:id>/contact/', views.LeadContactView.as_view(), name='contact'),
]
