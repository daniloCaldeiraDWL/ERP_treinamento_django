# Testes do backend

Os testes da aplicação estão sendo feito utilizando o Postman. 

Primeiro, eu tenho que fazer o login na aplicação, obtendo o token. 

## Criação de usuários:
- POST: http://127.0.0.1:8000/api/v1/auth/signup 
    - Prencher os campos em Body/form-data de name, email e password e assim é criado um novo usuário. 
    - Se tudo estiver correto, é criado o usuário no banco de dado e é apresetando para nós seus dados no body da resposta. 

## Login obtendo o token:
- POST: http://127.0.0.1:8000/api/v1/auth/signin
    - Prencher os campos Body/form-data de email e password.
    - Se tudo estiver correto, retorna o token de acesso. Copiamos este token
- Nas rotas que eu quero acessar, antes fazemos:
    - Vamos em Autorization e no Auth type eu ativo: Beared Token. 
    - Entro com o token copiado e está feito o login. 

##  Teste da tabela group de forma geral:
- GET: http://127.0.0.1:8000/api/v1/companies/groups
    - É retornado todos os grupos que eu tenho cadastrado no banco de dados. 

- POST: http://127.0.0.1:8000/api/v1/companies/groups
    - Passando o nome do grupo e as persmissions corretas, é criado um novo grupo de permissões. 
    - Não são aceitas permissions inexistentes ou errradas. 
    - É possível criar um grupo sem permissão nenhuma e editá-lo depois. 

## Teste da tebala group de forma individual
- GET: http://127.0.0.1:8000/api/v1/companies/groups/1 (sendo 1 o id)
    - É retornado o grupo em específico

- PUT: http://127.0.0.1:8000/api/v1/companies/groups/1
    - É possível editar um grupo. 
    - Não permite editar um grupo para um nome que já exista. 

- DELETE: http://127.0.0.1:8000/api/v1/companies/groups/10
    - Deleta um grupo pelo id. 
    - Não apaga, logicamente se ele não existe. 