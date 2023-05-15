import json
import os
from datetime import datetime
from urllib.parse import urlencode

import requests
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect

from pipedrivecrm import person
from . import lead as rdlead


'''

979ea8099383f9abd2dec402ba39580d32cb4110 - uuid
c1ad668236989f4f735179c1594c3eb8fb5f3bf3 - profissao
05910b25ee41b60ba64ca680ff8a7a60fcf05d0d - cep
951aabc418ef796f4b7996ee92cd0aa44fb3b07b - pais
1485bc05fc2ae3271004222bd8b803a122623ac1 - estado
8f8fc428ecec2187715f3597efaea6f41eabb169 - cidade
e75f615cb8aac7c990d023d3df74aea7c0306817 - logradouro
5700b737d526ec982fb457788a60000816c71fff - cpf
c0f2b6951407d4f1c627385d8b94951861c6f16d - cnpj

'''

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

            for lead in leads:
                uuid = lead['uuid']
                data = {
                    "979ea8099383f9abd2dec402ba39580d32cb4110": uuid,
                    "name": lead["name"],
                    "email": lead["email"],
                    "phone": [{"value": lead["personal_phone"]}],
                    "visible_to": "3"
                }
                status_code, personId = person.create(data)

                if status_code != 201:
                    return JsonResponse({"message": "Error when creating Pipedrive person"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Atualiza lead no RDStation com o id da pessoa criada no Pipedrive
                rdlead.update({ "cf_pipedrive_id": personId }, uuid)

            return JsonResponse({"message": "Success, created persons at Pipedrive"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return JsonResponse({"message": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def oauth_refresh():
    client_id = os.environ.get("client_id")
    client_secret = os.environ.get("client_secret")
    refresh_token = os.environ.get("refresh_token")

    if not refresh_token:
        print("Missing refresh token, please contact the administrator")
        return status.HTTP_401_UNAUTHORIZED

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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def oauth(request):
    access_token = os.environ.get('RDSTATION_ACCESS_TOKEN')
    expires_in = os.environ.get('RDSTATION_EXPIRES_IN')
    timestamp = int(datetime.timestamp(datetime.now()))

    if access_token and expires_in and int(expires_in) > timestamp:
        return JsonResponse({"message": "Already has a valid token"}, status=status.HTTP_200_OK)

    client_id = os.environ.get("client_id")
    redirect_uri = os.environ.get("redirect_uri")

    if not client_id or not redirect_uri:
        return JsonResponse({"message": "Missing authorization credencials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Conntroi a URL de autorização
    token_url = f'https://api.rd.services/auth/dialog?client_id={client_id}&redirect_uri={redirect_uri}'

    return HttpResponseRedirect(redirect_to=token_url)

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

        access_token = response.json()['access_token']
        refresh_token = response.json()['refresh_token']
        expires_in = str(response.json()['expires_in'] + int(datetime.timestamp(datetime.now())))
        
        # Guarda os tokens no arquivo .env
        os.environ['RDSTATION_ACCESS_TOKEN'] = access_token
        os.environ['RDSTATION_REFRESH_TOKEN'] = refresh_token
        os.environ['RDSTATION_EXPIRES_IN'] = expires_in

        return JsonResponse({'message':'OAuth flow completed successfully'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        print(e)
        return JsonResponse({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)