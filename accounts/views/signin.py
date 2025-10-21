from accounts.views.base import Base
from accounts.auth import Authentication
from accounts.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class Signin(Base):
    """View para o login de usuários."""

    def post(self, request):
        """Realiza o login do usuário e retorna o token de autenticação."""

        email = request.data.get('email') # Obtém o email do corpo da requisição
        password = request.data.get('password') # Obtém a senha do corpo da requisição

        user = Authentication.signin(self, email=email, password=password) # Realiza a autenticação do usuário
        
        token = RefreshToken.for_user(user) # Gera o token de autenticação

        enterprise = self.get_enterprise_user(user.id) # Obtém as informações da empresa e permissões do usuário

        serializer = UserSerializer(user) # Serializa os dados do usuário

        return Response({
            "user": serializer.data,
            "enterprise": enterprise,
            "refresh": str(token),
            "access": str(token.access_token)
        }) # Retorna a resposta com os dados do usuário, empresa e tokens