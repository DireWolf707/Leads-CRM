from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from leads.views import HomeView
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls', namespace='leads')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
