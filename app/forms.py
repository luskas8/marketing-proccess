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
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreva seu nome...'
            }
        )
    )
    
    email = forms.EmailField(
        label='E-mail',
        validators=[EmailValidator("E-mail inválido")],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Insira um endereço de email válido.',
        },
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Escreva seu email aqui...'
            }
        )
    )

    ddd = forms.IntegerField(
        label='DDD',
        max_value=99,
        validators=[ddd_regex],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Insira um valor decimal válido com até 2 casas decimais.',
            'max_value': 'O valor deve ter no máximo 2 dígitos.',
        },
        widget=forms.widgets.NumberInput(
            attrs={
                'placeholder': 'DDD do telefone...'
            }
        )
    )

    phone = forms.IntegerField(
        label='Telefone',
        validators=[phone_regex],
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Telefone inválido.',
        },
        widget=forms.widgets.NumberInput(
            attrs={
                'placeholder': 'Número de elefone...'
            }
        )
    )

class AddcionalInfoForm(forms.Form):    
    job_title = forms.CharField(
        label='Cargo',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu cargo nesse campo.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreve seu cargo aqui...'
            }
        )
    )

    country = forms.CharField(
        label='País',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu país nesse campo.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreve seu país aqui...'
            }
        )
    )

    zip_code = forms.IntegerField(
        label='CEP',
        max_value=99999999,
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu CEP nesse campo.',
        },
        widget=forms.widgets.NumberInput(
            attrs={
                'placeholder': 'Escreve seu cep aqui...'
            }
        )
    )

    state = forms.CharField(
        label='Estado',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu estado nesse campo.',
        },
        max_length=2,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreve as siglas do seu estado aqui...'
            }
        )
    )

    city = forms.CharField(
        label='Cidade',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque sua cidade nesse campo.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreve sua cidade aqui...'
            }
        )
    )

    address = forms.CharField(
        label='Logradouro',
        error_messages={
            'required': 'Este campo é obrigatório.',
            'invalid': 'Coloque seu endereço nesse campo.',
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Escreve seu endereço aqui...'
            }
        )
    )

    cpf = forms.IntegerField(
        label='CPF',
        max_value=99999999999,
        error_messages={
            'required': 'Informe um CPF ou CNPJ.',
            'invalid': 'Coloque seu CPF nesse campo.',
        },
        widget=forms.widgets.NumberInput(
            attrs={
                'placeholder': 'Escreve seu CPF aqui...'
            }
        ),
        help_text='Opcional para pessoa jurídica',
        required=False
    )

    cnpj = forms.IntegerField(
        label='CNPJ',
        max_value=99999999999999,
        error_messages={
            'required': 'Informe um CPF ou CNPJ.',
            'invalid': 'Coloque seu CNPJ nesse campo.',
        },
        widget=forms.widgets.NumberInput(
            attrs={
                'placeholder': 'Escreve o seu CNPJ aqui...'
            }
        ),
        help_text='Opcional para pessoa física',
        required=False
    )

    def clean(self):
        data = self.cleaned_data

        # Verifica se o usuário informou CPF ou CNPJ
        if data.get('cpf', None) or data.get('cnpj', None):
            pass
        else:
            msg = 'Informe um CPF ou CNPJ.'
            self.add_error("cpf", msg)
            self.add_error("cnpj", msg)

        return self.cleaned_data