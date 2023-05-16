# Marketing Proccess
Integração entre o formulário de captura de dados por marketing digital e CRM de forma que os dados do lead estejam sempre sincronizados entre os sistemas.

O projeto pode ser testado neste [link](https://www.luskas8.xyz).

## Tecnologias

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [HTML](https://developer.mozilla.org/pt-BR/docs/Web/HTML)
- [CSS](https://developer.mozilla.org/pt-BR/docs/Web/CSS)

## Como usar?

Primeiro de tudo é necessário ter conta em duas ferramentas, [RD Station](https://www.rdstation.com/) e [Pidedrive](https://www.pipedrive.com/).
Seguir os passos para obter as autorizações de acesso em cada um e em seguida, criar um arquivo de variáveis de ambiente ´.env´ há exemplo com o arquivo ´.env.emxemple´

Em seguida é necessaário ter Python 3.10 instalado no seu computador, em seguida clone o repositório do projeto e entre no repositório criado:

```sh
git clone https://github.com/luskas8/marketing-proccess.git
cd marketing-proccess
```

Ápos chegou a hora de instalar todas as dependências do projeto com o seguinte script no prompt:

```sh
pip install -r requirements.txt
```

Chegou a hora de testar:

```sh
python manage.py runserver
```

## Telas

**/contact** - tela inicial, é a tela onde uma pessoa faz o contato inicial enviando alguns dados, demonstrando interresse no produto.

**/forms/proccess/:personID** - tela de coleta de mais dados, a pessoa recebe um link por email para essa tela, assim que é passa a ser um lead qualificado,
ou seja, quando entra no funil de vendas.

### Documentação de API

A api pode ser acessada neste [link](https://www.luskas8.xyz/api/schema).

### Melhorias

- Salvar os campos personalizados e não deixa-los _hard code_.
- Automatizar obtenção do token do RD Station, com um job agendado.

### Contribuição
Se você deseja contribuir com este projeto, fique à vontade para abrir uma issue ou enviar um pull request. Toda contribuição é bem-vinda!

### Licença
Este projeto está licenciado sob a MIT License, o que significa que você pode usá-lo, modificá-lo e distribuí-lo livremente.
