from django.urls import path
from . import views

app_name = 'agents'

urlpatterns = [
    path('all/', views.AgentListView.as_view(), name='list'),
    path('create/', views.AgentCreateUpdateView.as_view(), name='create'),
    path('<int:id>/update/', views.AgentCreateUpdateView.as_view(), name='update'),
    path('<int:id>/', views.AgentDetailView.as_view(), name='detail'),
]
