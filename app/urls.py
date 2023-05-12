from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('forms/processo/', views.additional_info, name='additional_info'),
    path('api/rdstation/', include('rdstation.urls'), name='rdstation'),
    path('api/pipedrive/', include('pipedrivecrm.urls'), name='pipedrive'),
]