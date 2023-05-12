import os
import json
import requests
from datetime import datetime

from rdstation import views

def create_lead(name, email, ddd, phone) -> int:
    api_key = os.environ.get('RDSTATION_API_KEY')
    url = "https://api.rd.services/platform/conversions?api_key=" + api_key

    # Cria um lead no RDStation
    payload = {
        "event_type": "CONVERSION",
        "event_family": "CDP",
        "payload": {
            "conversion_identifier": "luskas8.xyz/contact",
            "name": name,
            "email": email,
            "personal_phone": str(ddd) + " " + str(phone),
        }
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return 201
        
        return False
    except Exception as e:
        print(e)
        return 400