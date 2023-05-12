import json
import os
from urllib.parse import urlencode

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.sendmail import sendmail
from rdstation import lead

'''

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
        return Response({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))

        if request_body['meta']['action'] == 'added':
            api_token = os.environ.get('PIPEDRIVE_API_KEY')
            personID = str(request_body['current']['person_id'])
            try:
                response = requests.get("https://api.pipedrive.com/v1/persons/" + personID + "?api_token=" + api_token)

                if not response['success']:
                    return Response({"message": "Pipedrive webhook deal working, but can't get persons data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                personEmail = response = response['data']['email'][0]['value']
                personName = response = response['data']['name']
                sendmail(personEmail, "Bem-vindo " + personName, "<p>Para continuar por favor preencha esse formulário:</p><p>https://www.luskas8.xyx/forms/processo?email="+ urlencode(personEmail) +"</p>")
                RDresponse = lead.funnel_lead(person_email=personEmail)

                if RDresponse == 200:
                    return Response({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)
                
                return Response({"message": "It was not possible to update RDStation lead to a qualified lead, try by your self or contact the developers"}, status=status.HTTP_200_OK)
                
            except Exception as e:
                print(e)
                return Response({"message": "Pipedrive webhook deal working, but can't get persons data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Pipedrive webhook deal working"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def webhook_person(request):
    if request.method == 'GET':
        return Response({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
    
    return Response({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)