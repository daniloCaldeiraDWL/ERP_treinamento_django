# Instruções
Desenvolvedor: Danilo Martins Caldeira.

# Notas: 
- 10/10/2025: inicialização do projeto e feito a Seção 1: Introdução. Foi feito a introdução e a Seção II, instalando todas as necessidades. 
- 11/10/2025: criação do core, utilização do Django REST Framework e Django cors headers.
- 12/10/2025: configuração do Django JWT, apresentação do conceito de Apps no Django. Achei super interessante que posso fazer um app e depois simplesmente copiá-lo para outro projeto e apenas importá-lo no core/settings.py
- 12/10/2025: Inicialização da seção 4, visto até a aula 17.
- 12/10/2025: Aula 19 foi feita até o minuto 19:34

# Sobre o Macro-projeto:
Este projeto é um treinamento seguindo os passos apresentados no Curso da Udemy: https://www.udemy.com/course/criando-um-sistema-para-gestao-empresarial-erp-2023/learn/lecture/41262470#overview.

## Ambiente virtual: 
Versão Python: 3.10.10

Os comandos a seguir podem ser execudados:
1. Criar: ```python -m venv venv```
2. Ativar: ```.\venv\Scripts\activate```
3. Instalar o que é preciso: ```pip install -r requirements.txt```
4. Para gerar o arquivo requirements.txt de forma automática: ```pip freeze > requirements.txt```
1. Desativar: ```deactivate```

## Notas do Django:
A documentação do Djando é disponibilizada em: https://docs.djangoproject.com/pt-br/5.2/

Anotações:

- Instalação: ```pip install django```
- Conferir se está instalado: ```django-admin --version```
- Criar um projeto Django: ```django-admin startproject core .``` ATENÇÃO COM O PONTO... ELE FAZ CRIAR FORA DA PASTA
  Ao iniciar um projeto temos alguns arquivos criados de forma automática. 
    - __init__.py: define a pasta como um pacote python.
    - settings.py: é o coração da aplicação django. Ele é um arquivo de configuração do Django. 
      - Para alterar o idioma: LANGUAGE_CODE = 'pt-br'
      - Para não ter problemas com data e hora no SQLite: USE_TZ = False
    - urls.py: onde são confirado as rotas. 
    - manage.py: arquivo que ficará na raiz do projeto, permitindo interagir de várias formas com o Django. 

- Executar o servidor: ```python manage.py runserver```. Caso tudo esteja certo, já temos o sistema disponível, com o link rodando. 
- Para finalizar: ```Ctrl + c```
- Criação do app Django: ```python manage.py startapp nome_do_app```. 
- Sempre que eu inserir um app eu tenho que defini-lo no arquivo settings em INSTALLED_APPS. 
- Também tenho que definir em urls.py 
- Para criar as tabelas do banco de dados, eu tenho que definir tudo em models.py na pasta de aplicativo.
- Após realizar inclusões ou alterações, eu tenho que executar o comando para migrar as novas alterações: 
```python manage.py makemigrations```
- Para assim, aplicarmos a migração novamente: ```python manage.py migrate``` 
- Preciso necessariamente, criar o super-usuario para o sistema: ```python manage.py createsuperuser```

Podemos, agora acessar o serviço com o link gerado. Entre muitas funcoes. 

### Painel administrador
- Com a aplicação rodando, podemos acessar o painel administrador: http://127.0.0.1:8000/admin/
- Caso não haja, temso que criar um super-usuário: ```python manage.py createsuperuser```

### Alterações no modelo
- Para realizar as alterações em modelos, significa que vamos alterar tabelas e o banco de dados na maioria dos casos. Criando novas tabelas ou inclindo. 
1. Fazemos as alterações;
2. Executamos o comando: ```python manage.py makemigrations```
3. Em alguns casos, vamos ter que tratar casos como novos campos não nulos etc. 
4. Após a migração, podemos executar: ```python manage.py migrate```

### Django rest framework
- Documentação: https://www.django-rest-framework.org/
- Instalação: 
- ```pip install djangorestframework```
- ```pip install markdown```
- ```pip install django-filter```

- Para uso é necessário inserir o aplicativo nos INSTALLED_APPS em core/settings.py com o comando: ```'rest_framework',```

### Django cors headers
Biblioteca ligada com segurança de requisições na API que estamos desenvolvendo. Ela oferece uma camada extra de segurança ppara nossa API. 
- Documentação: https://pypi.org/project/django-cors-headers/
- Instalação: ```pip install django-cors-headers```
- Instruções de instalação e configuração estão na documentação. Precisa configurar no core/settings.py

### Django Rest Framework JWT
- Documentação: https://django-rest-framework-simplejwt.readthedocs.io/en/latest/
- Instalação: ```pip install djangorestframework-simplejwt```
- Instruções de instalação e configuração estão na documentação. Precisa configurar no core/settings.py
- Em Settings, eu tenho várias configurações que eu posso fazer com a biblioteca. 


## Rotinas de trabalho com Branch isoladas de desenvolvimento
- Criar uma branch: ```git checkout -b brach/minha-nova-branch```
    - Fazer as alterações necessárias

- Realizar commit: ```git add .``` e ```git commit -m "tipo: descricao do commit resimido"```
- Realizar o push da branch isolada: ```git push brach/minha-nova-branch```

- Criação do Pull Request:
  - Acessar o repositório do GitHub
  - Clicar em "Compare & pull request"
  - Preencher as informações e crie o Pull Request

- Testar a Branch com as alterações realizadas e verificar para aprovação e mesclar na branch principal
  - Fazer o fetch para puxar as referências remotas: ```git fetch origin master```
  - Posso criar e mudar para uma branch local baseada na branch do PR: ```git checkout -b teste-local origin/feature/nova-funcionalidade```
  - Também posso clicar no botão no canto inferior do VSCode e alterar a branch que eu quero. 
    - Fazer os testes necessário, estando na branch temporária.
  - Voltar para a branch master/main: ```git checkout master```
  - Posso apagar a branch de teste criada ou a branch sincronizada

- Aprovar o Pull Request (após os testes)
    - No GitHub, acesse o Pull Request criado
    - Clique em "Merge pull request"
    - Confirme clicando em "Confirm merge"
    - Apago a branch que foi feito o merge (se quiser)

- Sincronizar o repositório local com a branch master do GitHub
    - Voltar a branch principal: ```git checkout master```
    - Atualizar repositório: ```git pull origin```
    - Apagar, se necessário a branch isolada: ```git branch -d  brach/minha-nova-branch```