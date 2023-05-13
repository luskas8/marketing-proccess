from django.urls import path

from . import views

urlpatterns = [
    path('api/rdstation/webhook/', views.webhook, name='rdstation_webhook'),
    path('api/rdstation/oauth/', views.oauth, name='rdstation_oauth'),
    path('api/rdstation/oauth/callback/', views.oauth_callback, name='rdstation_oauth_callback')
]