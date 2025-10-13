from rest_framework.exceptions import AuthenticationFailed, APIException
from accounts.models import User
from companies.models import Enterprise, Employee
from django.contrib.auth.hashers import check_password, make_password

class Authentication:
    def signin(self, email = None, password = None) -> User:
        exception_auth = APIException("Email e/ou senha inválidos")
        user_exists = User.objects.filter(email=email).exists()

        # verifica se o usuário existe
        if not user_exists or not check_password(password, User.objects.get(email=email).password):
            raise exception_auth
        
        # carrega o usuário
        user = User.objects.filter(email=email).first()

        # verifica se a senha está correta
        if not check_password(password, user.password):
            raise exception_auth

        # retorna o usuário
        return user

    def signup(self, name = None, email = None, password = None, type_account = "owner", company_id = False) -> User:

        # valida os dados de nome, email e senha como sendo obrigatórios
        if not name or name == "":
            raise APIException("O nome é obrigatório! Não pode ser vazio.")
        if not email or email == "":
            raise APIException("O email é obrigatório! Não pode ser vazio.")
        if not password or password == "":
            raise APIException("A senha é obrigatória! Não pode ser vazia.")
        
        if type_account == "employee" and not company_id:
            raise APIException("O ID da empresa é obrigatório para funcionários!")
        
        user = User()
        # verifica se o email já está cadastrado, sendo que o email é um campo único
        if User.objects.filter(email=email).exists():
            raise APIException("O email já está cadastrado!")
        
        # criptografa a senha
        password_hashed = make_password(password)

        # criação do usuário
        created_user = User.objects.create(
            name = name,
            email = email,
            password = password_hashed,
            is_owner = 0 if type_account == "employee" else 1 # se for funcionário, is_owner = 0, se for proprietário, is_owner = 1
        )

        # se o tipo de conta for proprietário, cria a empresa
        if type_account == "owner":

            # vincula o funcionário à empresa
            created_enterprise = Enterprise.objects.create(
                name = f"Nome da empresa",
                user_id = company_id
            )

        # se o tipo de conta for funcionário, vincula o funcionário à empresa
        if type_account == "employee":
            Employee.objects.create(
                enterprise_id = company_id or created_enterprise.id,
                user_id = created_user.id                
            )

        return created_user
