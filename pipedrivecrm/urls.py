from django.urls import path, include

from . import views

urlpatterns = [
    path('api/pipedrive/webhook_deal', views.webhook_deal, name='pipedrive_weebhook_deal'),
    path('api/pipedrive/webhook_person', views.webhook_person, name='pipedrive_weebhook_person'),
]