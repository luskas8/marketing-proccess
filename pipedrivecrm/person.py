from pipedrive.client import Client as PipedriveClient
from rest_framework import status


def create(data) -> list:
    # Obtém os tokens da API de variáveis de ambiente
    API_TOKEN = os.environ.get("API_TOKEN")
    COMPANY_DOMAIN = os.environ.get("COMPANY_DOMAIN")

    if not API_TOKEN or not COMPANY_DOMAIN:
        return status.HTTP_401_UNAUTHORIZED

    pipedrive_url = f"https://{COMPANY_DOMAIN}.pipedrive.com"
    # Cria uma instância do cliente do Pipedrive com a URL da API
    pipedrive = PipedriveClient(domain=pipedrive_url)
    pipedrive.set_api_token(API_TOKEN)

    # Cria uma pessoa no Pipedrive com os dados do lead
    response = pipedrive.persons.create_person(data)

    if not response['success']:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    
    return [ status.HTTP_201_CREATED, response['data']['id'] ]