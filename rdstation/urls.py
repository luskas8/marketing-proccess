from django.urls import path

from . import views

urlpatterns = [
    path('webhook', views.webhook, name='rdstation_webhook'),
    path('oauth/', views.oauth, name='rdstation_oauth'),
    path('oauth/callback', views.oauth_callback, name='rdstation_oauth_callback'),
]