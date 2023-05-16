import json
import os
from time import sleep
from datetime import datetime

import requests
from rest_framework import status

from rdstation import views


def create(name, email, ddd, phone) -> int:
    api_key = os.environ.get('RDSTATION_API_KEY')

    # Caso não tenha api key, retorna erro
    if not api_key:
        return status.HTTP_400_BAD_REQUEST

    url = f"https://api.rd.services/platform/conversions?api_key={api_key}"

    # Cria um lead no RDStation
    payload = {
        "event_type": "CONVERSION",
        "event_family": "CDP",
        "payload": {
            "conversion_identifier": "luskas8.xyz/contact/",
            "name": name,
            "email": email,
            "personal_phone": str(ddd) + " " + str(phone),
            "cf_pipedrive_id": "",
            "cf_cep": "",
            "country": "",
            "city": "",
            "state": "",
            "cf_logradouro": "",
            "job_title": ""
        }
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != status.HTTP_200_OK:
            print(response.status_code, response.json())
            return status.HTTP_400_BAD_REQUEST
        
        return status.HTTP_201_CREATED
    except Exception as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST

def funnel(person_email) -> int:    
    access_token = os.environ.get('RDSTATION_ACCESS_TOKEN')
    expires_in = os.environ.get('RDSTATION_EXPIRES_IN')
    timestamp = int(datetime.timestamp(datetime.now()))

    # Caso não tenha access token ou o token tenha expirado, tenta obter um novo
    if not access_token or not expires_in or int(expires_in) <= timestamp:
        oauth_status_code = views.oauth_refresh()
        if oauth_status_code != status.HTTP_200_OK:
            return oauth_status_code
    
    url = f"https://api.rd.services/platform/contacts/email:{person_email}/funnels/default"

    payload = {
        "lifecycle_stage": "Qualified Lead",
        "opportunity": False
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    try:
        # Tentativa de atualizar o lead para lead qualificado no RDStation
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == status.HTTP_200_OK:
            return status.HTTP_200_OK
        
        print(response.status_code, response.json())
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    except Exception as e:
        print(e)
        return status.HTTP_500_INTERNAL_SERVER_ERROR
        
    return status.HTTP_200_OK

def update(data, uuid) -> int:
    access_token = os.environ.get('RDSTATION_ACCESS_TOKEN')
    expires_in = os.environ.get('RDSTATION_EXPIRES_IN')
    timestamp = int(datetime.timestamp(datetime.now()))

    # Caso não tenha access token ou o token tenha expirado, tenta obter um novo
    if not access_token or not expires_in or int(expires_in) <= timestamp:
        oauth_status_code = views.oauth_refresh()
        if oauth_status_code != status.HTTP_200_OK:
            return oauth_status_code


    url = f"https://api.rd.services/platform/contacts/uuid:{uuid}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.patch(url, json=data, headers=headers)

    if response.status_code != status.HTTP_200_OK:
        print(response.status_code, response.json())
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return status.HTTP_200_OK

def delete(uuid) -> int:
    access_token = os.environ.get('RDSTATION_ACCESS_TOKEN')
    expires_in = os.environ.get('RDSTATION_EXPIRES_IN')
    timestamp = int(datetime.timestamp(datetime.now()))

    # Caso não tenha access token ou o token tenha expirado, tenta obter um novo
    if not access_token or not expires_in or int(expires_in) <= timestamp:
        oauth_status_code = views.oauth_refresh()
        if oauth_status_code != status.HTTP_200_OK:
            return oauth_status_code
    
    url = f"https://api.rd.services/platform/contacts/uuid:{uuid}"

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code != status.HTTP_204_NO_CONTENT:
        print(response.status_code, response.json())
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return status.HTTP_200_OK
