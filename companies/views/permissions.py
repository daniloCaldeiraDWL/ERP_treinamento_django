from companies.views.base import Base
from companies.utils.permissions import GroupsPermission
from companies.serializers import PermissionSerializer

from rest_framework.views import Response

from django.contrib.auth.models import Permission

class PermissionDetail(Base):
    """View para obter todos os grupos disponíveis para a empresa do usuário autenticado."""

    permission_classes = [GroupsPermission] # Garante que o usuário tenha permissão para acessar os grupos

    def get(self, request):
        """Obtém todos os grupos disponíveis para a empresa do usuário autenticado."""

        permissions = Permission.objects.filter(content_type_id__in=[2, 7, 11, 13]).all() # Obtém todas as permissões relevantes

        serializer = PermissionSerializer(permissions, many=True) # Serializa os dados dos grupos

        return Response({"permissions": serializer.data}) # Retorna a resposta com os dados dos grupos