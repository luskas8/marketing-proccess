from django.urls import include, path
from django.views.generic.base import RedirectView
from drf_spectacular.views import (SpectacularAPIView,
                                       SpectacularSwaggerView)

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url="contact", permanent=False), name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('forms/proccess/<str:personId>', views.additional_info_view, name='additional_info'),
    path('api/rdstation/', include('rdstation.urls'), name='rdstation'),
    path('api/pipedrive/', include('pipedrivecrm.urls'), name='pipedrive'),
    path('api/schema/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/download', SpectacularAPIView.as_view(), name='schema'),
]