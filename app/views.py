from django.http import HttpResponse
from django.shortcuts import render

from rdstation import lead

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
            
            if response_status == 201:
                # Retornar uma resposta de erro
                return render(request, 'app/contact.html', {'form': form, 'error': True})

            # Retornar uma resposta de sucesso ou redirecionar para outra página
            return render(request, 'app/thanks.html', { 'message': "Em instantes um de nossas agentes irá entrar em contato!" })
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form, 'error': False})

def additional_info(request):
    if request.method == "POST":
        form = AddcionalInfoForm(request.POST)

        if form.is_valid():
            # Processar o formulário e enviar a mensagem
            personID = request.GET.get('personID')
            email = request.GET.get('email')
            job_title = form.cleaned_data['job_title']
            zip_code = form.cleaned_data['zip_code']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
        
        print(job_title, zip_code, country, state, city, address)
        return render(request, 'app/thanks.html', { 'message': "Muito bem, estamos muito contentes pelo seu interesse!" })
    
    else:
        form = AddcionalInfoForm()
    
    return render(request, 'app/info.html', {'form': form, 'error': False})


