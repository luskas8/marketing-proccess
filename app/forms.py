from django import forms
from django.core.validators import EmailValidator, RegexValidator

class ContactForm(forms.Form):
    ddd_regex = RegexValidator(
        regex=r'^[1-9]{2}$',
        message="O DDD deve conter 2 dígitos numéricos."
    )

    phone_regex = RegexValidator(
        regex=r'^(?:[2-8]|9[1-9])[0-9]{7}$',
        message="Número de telefone inválido."
    )

    name = forms.CharField(
        label='Nome',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu nome nesse campo.',
        }
    )
    email = forms.EmailField(
        label='E-mail',
        validators=[EmailValidator("E-mail inválido")],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Insira um endereço de email válido.',
        }
    )
    ddd = forms.DecimalField(
        label='DDD',
        max_digits=2,
        decimal_places=0,
        validators=[ddd_regex],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Insira um valor decimal válido com até 2 casas decimais.',
            'max_digits': 'O valor deve ter no máximo 5 dígitos.',
            'max_decimal_places': 'O valor deve ter no máximo 2 casas decimais.',
        }
    )
    phone = forms.DecimalField(
        label='Telefone', 
        max_digits=9,
        decimal_places=0,
        validators=[phone_regex],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Telefone inválido.',
            'max_digits': 'Telefone inválido',
            'max_decimal_places': 'Telefones não tem mais que isso de dígitos.',
        }
    )

class AddcionalInfoForm(forms.Form):
    job_title = forms.CharField(
        label='Cargo',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu cargo nesse campo.',
        }
    )

    country = forms.CharField(
        label='País',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu país nesse campo.',
        }
    )

    zip_code = forms.DecimalField(
        label='CEP',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu CEP nesse campo.',
        }
    )

    state = forms.CharField(
        label='Estado',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu estado nesse campo.',
        }
    )

    city = forms.CharField(
        label='Cidade',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque sua cidade nesse campo.',
        }
    )

    address = forms.CharField(
        label='Logradouro',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu endereço nesse campo.',
        }
    )