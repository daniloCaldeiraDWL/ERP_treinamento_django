# Instruções
Desenvolvedor: Danilo Martins Caldeira.

# Notas: 
- 08/10/2025: comecei vendo o tutorial (https://www.youtube.com/watch?v=ZXli2MJyRyk) até o minuto 17:50 deixando pronto o método criar. 
- 08/10/2025: visto o tutorial até o minuto 31:01, com os métodos de criar e deletar finalizando
- 08/10/2025: finalizado o treinamento com uma aplicação simples capaz de criar/atualizar/ler/deletar alunos 

# Sobre o Macro-projeto:
Neste repositório encontram-se vários treinamentos focados em Django. Consolidaremos aqui aplicações para agrupar uma base de treinamento, exemplos, práticas e desenvolvimentos genéricos de vários projetos. Cada projeto foca em uma temática específica, geralmente muito clara, sendo o próprio nome do projeto. Assim, conseguimos reunir e concentrar vários temas em um só lugar, facilitando consultas fururas. Os projetos serão mapeados nos milestrones. 

## Projeto CRUD with Django"
Base de estudo: https://www.youtube.com/watch?v=ZXli2MJyRyk

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