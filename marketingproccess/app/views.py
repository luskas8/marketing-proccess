from django.http import HttpResponse
from django.shortcuts import render

from .forms import ContactForm

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
            # Lógica para enviar o e-mail ou salvar a mensagem no banco de dados, por exemplo
            print(name, email, ddd, phone)
            # Retornar uma resposta de sucesso ou redirecionar para outra página
            return render(request, 'app/thanks.html')
    else:
        form = ContactForm()

    return render(request, 'app/contact.html', {'form': form})