from rest_framework.exceptions import AuthenticationFailed, APIException
from django.contrib.auth.hashers import check_password, make_password
from accounts.models import User
from companies.models import Enterprise, Employee

class Authentication:
    """Classe para autenticação e cadastro de usuários."""

    def signin(self, email=None, password=None) -> User:
        """Realiza a autenticação do usuário com email e senha."""

        if not email or email == '': # Verifica se o email foi fornecido
            raise APIException('O email não deve ser null')
        
        if not password or password == '': # Verifica se a senha foi fornecida
            raise APIException('O password não deve ser null')

        exception_auth = AuthenticationFailed('Email e/ou senha incorreto(s)') # Exceção para falha de autenticação

        user_exists = User.objects.filter(email=email).exists() # Verifica se o usuário existe

        if not user_exists: # Se o usuário não existir
            raise exception_auth # Lança exceção de autenticação falhada
        
        user = User.objects.filter(email=email).first() # Obtém o usuário pelo email

        if not check_password(password, user.password): # Verifica se a senha está correta
            raise exception_auth # Lança exceção de autenticação falhada
        
        return user
    
    def signup(self, name, email, password, type_account='owner', company_id=False):
        """Realiza o cadastro do usuário."""

        if not name or name == '':
            raise APIException('O nome não deve ser null')
        
        if not email or email == '':
            raise APIException('O email não deve ser null')
        
        if not password or password == '':
            raise APIException('O password não deve ser null')
        
        if type_account == 'employee' and not company_id:
            raise APIException('O id da empresa não deve ser null')

        user = User
        if user.objects.filter(email=email).exists():
            raise APIException('Este email já existe na plataforma')
        
        password_hashed = make_password(password)

        created_user = user.objects.create(
            name=name,
            email=email,
            password=password_hashed,
            is_owner=0 if type_account == 'employee' else 1
        )

        if type_account == 'owner':
            created_enterprise = Enterprise.objects.create(
                name='Nome da empresa',
                user_id=created_user.id
            )

        if type_account == 'employee':
            Employee.objects.create(
                enterprise_id=company_id or created_enterprise.id,
                user_id=created_user.id
            )

        return created_user