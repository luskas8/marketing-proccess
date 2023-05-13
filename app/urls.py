from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('forms/proccess/', views.additional_info, name='additional_info'),
    path('', include('rdstation.urls'), name='rdstation'),
    path('', include('pipedrivecrm.urls'), name='pipedrive'),
]