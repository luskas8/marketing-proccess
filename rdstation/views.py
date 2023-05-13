import json
import os
from datetime import datetime
from urllib.parse import urlencode

import requests
from django.shortcuts import redirect, render
from pipedrive.client import Client as PipedriveClient
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook(request):
    # Se o método da requisição é GET e retorna uma mensagem de sucesso caso o webhook esteja funcionando
    if request.method == 'GET':
        return JsonResponse({"message": "RDStation webhooks working"}, status=status.HTTP_200_OK)
    
    # Se o método da requisição é POST processa os dados recebidos
    elif request.method == 'POST':
        try:
            request_body = request.body.decode('utf-8')
            leads = json.loads(request_body)['leads']

            # Obtém os tokens da API de variáveis de ambiente
            API_TOKEN = os.environ.get("API_TOKEN")
            COMPANY_DOMAIN = os.environ.get("COMPANY_DOMAIN")
            pipedrive_url = "https://{}.pipedrive.com".format(COMPANY_DOMAIN)

            for lead in leads:
                # Cria uma instância do cliente do Pipedrive com a URL da API
                pipedrive = PipedriveClient(domain=pipedrive_url)
                pipedrive.set_api_token(API_TOKEN)

                # Cria uma pessoa no Pipedrive com os dados do lead
                response = pipedrive.persons.create_person({
                    "name": lead["name"],
                    "email": lead["email"],
                    "phone": [{"value": lead["personal_phone"]}],
                    "visible_to": "3"
                })

                if not response['success']:
                    return JsonResponse({"message": "Error when creating Pipedrive person"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                personId = response['data']['id']

            return JsonResponse({"message": "Success, created persons at Pipedrive"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def oauth_refresh():
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    refresh_token = os.environ.get("refresh_token")

    if not refresh_token:
        print("Missing refresh token")
        requests.post("https://luskas8.xyz/api/rdstation/oauth/")
        return status.HTTP_200_OK

    # Código para obter um novo access token
    token_url = 'https://api.rd.services/auth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    try:
        response = requests.post(token_url, data=payload)

        if response.status_code != 200:
            return status.HTTP_401_UNAUTHORIZED

        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        expires_in =  str(response.json()['expires_in'] + int(datetime.timestamp(datetime.now())))

        # Guarda os tokens no arquivo .env
        os.environ['RDSTATION_ACCESS_TOKEN'] = access_token
        os.environ['RDSTATION_REFRESH_TOKEN'] = refresh_token
        os.environ['RDSTATION_EXPIRES_IN'] = expires_in
            
        return status.HTTP_200_OK
        
    except Exception as e:
        print(e)
        return status.HTTP_500_INTERNAL_SERVER_ERROR

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def oauth(request):
    client_id = os.environ.get("client_id")
    redirect_uri = os.environ.get("redirect_uri")

    if not client_id or not redirect_uri:
        return JsonResponse({"message": "Missing authorization credencials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Conntroi a URL de autorização
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
    }
    authorization_url = 'https://api.rd.services/auth/dialog/authorize?' + urlencode(params)

    return JsonResponse({"message": "OAuth request done"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def oauth_callback(request):
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    redirect_uri = os.environ.get("redirect_uri")
    authorization_code = request.GET.get('code')

    if not client_id or not client_secret or not redirect_uri or not authorization_code:
        return JsonResponse({"message": "Missing authorization credencials or code"}, status=status.HTTP_401_UNAUTHORIZED)

    # Troca o código de autorização pelo access token
    token_url = 'https://api.rd.services/auth/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': authorization_code,
        'redirect_uri': redirect_uri,
    }

    try:
        response = requests.post(token_url, json=payload)

        if response.status_code != 200:
            print(response.json())
            return JsonResponse({'message': "Something went wrong"}, status=response.status_code)

        return JsonResponse({'message':'OAuth flow completed successfully'}, status=status.HTTP_200_OK)
        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        expires_in = str(response.json()['expires_in'] + int(datetime.timestamp(datetime.now())))

        # Guarda os tokens no arquivo .env
        os.environ['RDSTATION_ACCESS_TOKEN'] = access_token
        os.environ['RDSTATION_REFRESH_TOKEN'] = refresh_token
        os.environ['RDSTATION_EXPIRES_IN'] = expires_in
        
    except Exception as e:
        print(e)
        return JsonResponse({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)