from django.urls import path, include
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    path('', RedirectView.as_view(url="contact", permanent=False), name='index'),
    path('contact', views.contact_view, name='contact'),
    path('forms/proccess/<str:personId>', views.additional_info_view, name='additional_info'),
    path('api/rdstation/', include('rdstation.urls'), name='rdstation'),
    path('api/pipedrive/', include('pipedrivecrm.urls'), name='pipedrive'),
]