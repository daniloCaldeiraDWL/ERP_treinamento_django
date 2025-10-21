from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer

from rest_framework.response import Response

class Signup(Base):
    """View para o cadastro de novos usuários."""

    def post(self, request):
        """Realiza o cadastro do usuário e retorna os dados do usuário criado."""

        name = request.data.get('name') # Obtém o nome do corpo da requisição
        email = request.data.get('email') # Obtém o email do corpo da requisição
        password = request.data.get('password') # Obtém a senha do corpo da requisição

        user = Authentication.signup(self, name=name, email=email, password=password) # Realiza o cadastro do usuário

        serializer = UserSerializer(user) # Serializa os dados do usuário criado

        return Response({"user": serializer.data}) # Retorna a resposta com os dados do usuário criado