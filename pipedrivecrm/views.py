import os
import json
import requests
from django.shortcuts import render
from rest_framework.response import Response

from app.sendmail import sendmail

def webhook_deal(request):
    if request.method == 'GET':
        return Response({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        sendmail("luskanjos@gmail.com", "Pipedrive webhook deal working", "Pipedrive webhook deal working\nhttps://www.luskas8.xyx/forms/processo?email=luskanjos@gmail.com")
        request_body = json.loads(request.body.decode('utf-8'))
        print(request_body)
    
    return Response({"message": "Pipedrive webhook deal working"}, status=status.HTTP_200_OK)

def webhook_person(request):
    if request.method == 'GET':
        return Response({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        request_body = json.loads(request.body.decode('utf-8'))
        print(request_body)
    
    return Response({"message": "Pipedrive webhook person working"}, status=status.HTTP_200_OK)