from accounts.views.base import Base
from accounts.models import User
from accounts.serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class GetUser(Base):
    """View para obter os dados do usuário autenticado."""

    permission_classes = [IsAuthenticated] # Garante que o usuário esteja autenticado

    def get(self, request):
        user = User.objects.filter(id=request.user.id).first() # Obtém o usuário autenticado
        enterprise = self.get_enterprise_user(user) # Obtém as informações da empresa e permissões do usuário

        serializer = UserSerializer(user) # Serializa os dados do usuário

        return Response({
            "user": serializer.data,
            "enterprise": enterprise
        }) # Retorna a resposta com os dados do usuário e empresa