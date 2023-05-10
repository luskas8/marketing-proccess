from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('api/rdstation/', include('rdstation.urls'), name='rdstation'),
    path('pipedrive/webhook/', views.pipedriveWebhook, name='pipedrive_webhook'),
]