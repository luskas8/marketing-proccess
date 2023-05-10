import requests
import os
import time
from urllib.parse import urlencode
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook(request):
    if request.method == 'GET':
        return Response({"message":"RDStation webhooks working"}, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response({"message":"RDStation webhook received"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def oauth(request):
    client_id = 'YOUR_CLIENT_ID'
    redirect_uri = 'YOUR_REDIRECT_URI'

    # Construct the authorization URL
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    }
    authorization_url = 'https://api.rd.services/auth/dialog/authorize?' + urlencode(params)

    return Response("OAuth request done", status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def oauth_callback(request):
    client_id = 'YOUR_CLIENT_ID'
    client_secret = 'YOUR_CLIENT_SECRET'
    redirect_uri = 'YOUR_REDIRECT_URI'
    authorization_code = request.GET.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://api.rd.services/auth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        # Access token retrieved successfully
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        expiration_time = response.json()['expiration_time'] + time.time()

        # Store the access token and refresh token in environment variables
        os.environ['RDSTATION_ACCESS_TOKEN'] = access_token
        os.environ['RDSTATION_REFRESH_TOKEN'] = refresh_token
        os.environ['RDSTATION_EXPIRATION_TIME'] = expiration_time

        return Response({'message':'OAuth flow completed successfully'}, status=status.HTTP_200_OK)
    else:
        # Handle errors when retrieving the access token
        return Response({'message':'Failed to retrieve access tokeny'}, status=status.HTTP_400_BAD_REQUEST)