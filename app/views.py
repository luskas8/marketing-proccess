from django.http import HttpResponse
from django.shortcuts import render

from rdstation import lead
from pipedrivecrm import person

from .forms import ContactForm, AddcionalInfoForm


def index(request):
    return HttpResponse("Hello, world.")

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Processar o formulário e enviar a mensagem
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            ddd = form.cleaned_data['ddd']
            phone = form.cleaned_data['phone']

            # 1. Criar um lead no RDStation
            response_status = lead.create(name, email, ddd, phone)

            # 2. Criar um person no Pipedrive:
            #   como faz uma conversão de lead no RDStation, o webhook vai ser chamado e vai criar um person no Pipedrive
            
            if response_status != 201:
                # Retornar uma resposta de erro
                return render(request, 'app/form.html', { 'title': 'Interesse no produto', 'form': form, 'error': True})

            # Retornar uma resposta de sucesso ou redirecionar para outra página
            return render(request, 'app/thanks.html', { 'message': "Em instantes um de nossas agentes irá entrar em contato!" })
        else:
            return render(request, 'app/form.html', { 'title': 'Interesse no produto', 'form': form, 'error': True})
    else:
        form = ContactForm()

    return render(request, 'app/form.html', { 'title': 'Interesse no produto', 'form': form, 'error': False})

def additional_info_view(request, personId):
    if request.method == "POST":
        form = AddcionalInfoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # Processar o formulário e enviar a mensagem
            job_title = form.cleaned_data['job_title']
            zip_code = form.cleaned_data['zip_code']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']

            data = {
                "05910b25ee41b60ba64ca680ff8a7a60fcf05d0d": str(zip_code),
                "951aabc418ef796f4b7996ee92cd0aa44fb3b07b": country,
                "1485bc05fc2ae3271004222bd8b803a122623ac1": state,
                "8f8fc428ecec2187715f3597efaea6f41eabb169": city,
                "e75f615cb8aac7c990d023d3df74aea7c0306817": address,
                "c1ad668236989f4f735179c1594c3eb8fb5f3bf3": job_title
            }
            # Atualizar o person no Pipedrive
            # status_code = person.update(data, personId)

            if True:
                # Retornar uma resposta de erro
                return render(request, 'app/form.html', { 'title': 'Informações adicionais', 'form': form, 'error': True})
        else:
            return render(request, 'app/form.html', { 'title': 'Informações adicionais', 'form': form, 'error': True})

        return render(request, 'app/thanks.html', { 'message': "Muito bem, estamos muito contentes pelo seu interesse!" })
    
    else:
        form = AddcionalInfoForm()
    
    return render(request, 'app/form.html', { 'title': 'Informações adicionais', 'form': form, 'error': False})


