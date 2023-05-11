from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm

from rdstation import lead

def index(request):
    return HttpResponse("Hello, world.")

def pipedriveWebhook(request):
    return HttpResponse("RD WEBHOOK")

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
            wasCreated = lead.create_lead(name, email, ddd, phone)

            # 2. Criar um person no Pipedrive & criar um deal no Pipedrive:
            #   como faz uma conversão de lead no RDStation, o webhook vai ser chamado e vai criar um person e um deal no Pipedrive
            
            if wasCreated == False:
                # Retornar uma resposta de erro
                return render(request, 'app/contact.html', {'form': form, 'error': True})

            # Retornar uma resposta de sucesso ou redirecionar para outra página
            return render(request, 'app/thanks.html')
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form, 'error': False})