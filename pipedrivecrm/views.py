import json
import os

import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny

from app.sendmail import sendmail
from rdstation import lead

'''

979ea8099383f9abd2dec402ba39580d32cb4110 - uuid
c1ad668236989f4f735179c1594c3eb8fb5f3bf3 - profissao
05910b25ee41b60ba64ca680ff8a7a60fcf05d0d - cep
951aabc418ef796f4b7996ee92cd0aa44fb3b07b - pais
1485bc05fc2ae3271004222bd8b803a122623ac1 - estado
8f8fc428ecec2187715f3597efaea6f41eabb169 - cidade
e75f615cb8aac7c990d023d3df74aea7c0306817 - logradouro

'''


@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook_deal(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))

        if (request_body['retry'] > 1):
            return JsonResponse({"message": "We know, stop!"}, status=status.HTTP_200_OK)

        if request_body['meta']['action'] == 'added':
            api_token = os.environ.get('API_TOKEN')
            personID = request_body['current']['person_id']

            try:
                url = f"https://api.pipedrive.com/v1/persons/{personID}?api_token={api_token}"

                response = requests.get(url)
                response_data = response.json()
                if not response_data['success']:
                    return JsonResponse({"message": "Pipedrive webhook deal working, but can't get persons data"}, status=status.HTTP_201_CREATED)
                
                personEmail = response_data['data']['email'][0]['value']
                personName = response_data['data']['name']
                subject = f"Bem-vindo {personName}!"
                link = f"https://luskas8.xyz/forms/proccess/?personID={personID}"

                sendmail(personEmail, subject, f"<p>Para continuar por favor preencha esse formulário:</p><p>{link}</p>")
                RDresponse = lead.funnel(person_email=personEmail)

                if RDresponse != 200:
                    return JsonResponse({"message": "It was not possible to update RDStation lead to a qualified lead, try by your self or contact the developers"}, status=status.HTTP_200_OK)
                    
                return JsonResponse({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)
                

            except Exception as e:
                print(e)
                return JsonResponse({"message": "Pipedrive webhook deal working, but can't get persons data"}, status=status.HTTP_204_NO_CONTENT)

    return JsonResponse({"message": "Pipedrive webhook deal working, no actions done"}, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook_person(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        if (request_body['retry'] > 1):
            return JsonResponse({"message": "We know, stop!"}, status=status.HTTP_200_OK)
        print(request_body)
        
        if request_body['meta']['action'] == 'updated':
            # todo: adicionar campos de CPF e CNPJ
            data = {
                "uuid": request_body['current']['979ea8099383f9abd2dec402ba39580d32cb4110'],
                "cf_pipedrive_id": request_body['current']['id'],
                "name": request_body['current']['name'],
                "email": request_body['current']['email'][0]['value'],
                "phone": request_body['current']['phone'][0]['value'],
                "cf_cep": request_body['current']['05910b25ee41b60ba64ca680ff8a7a60fcf05d0d'],
                "country": request_body['current']['951aabc418ef796f4b7996ee92cd0aa44fb3b07b'],
                "state": request_body['current']['1485bc05fc2ae3271004222bd8b803a122623ac1'],
                "city": request_body['current']['8f8fc428ecec2187715f3597efaea6f41eabb169'],
                "cf_logradouro": request_body['current']['e75f615cb8aac7c990d023d3df74aea7c0306817'],
                "job_title": request_body['current']['c1ad668236989f4f735179c1594c3eb8fb5f3bf3']
            }
            lead.update(data, True)
        
    return JsonResponse({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)