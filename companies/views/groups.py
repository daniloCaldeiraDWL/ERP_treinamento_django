from companies.views.base import Base
from companies.utils.exceptions import RequiredFields
from companies.utils.permissions import GroupsPermission
from companies.serializers import GroupsSerializer

from accounts.models import Group, Group_Permissions

from rest_framework.views import Response
from rest_framework.exceptions import APIException

from django.contrib.auth.models import Permission

class Groups(Base):
    """View para gerenciar grupos dentro de uma empresa."""
    
    permission_classes = [GroupsPermission]

    def get(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário
        groups = Group.objects.filter(enterprise_id=enterprise_id).all() # Filtra os grupos pela empresa, pegando todos os grupos

        serializer = GroupsSerializer(groups, many=True) # Serializa os dados dos grupos, indicando que são múltiplos objetos com many=True

        return Response({"groups": serializer.data}) # Retorna a resposta com os dados serializados de todos os grupos cadastrados na empresa que consequentemente, estão cadastrados também no meu banco de dados.

    def post(self, request):
        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário

        name = request.data.get('name') # Obtém o nome do grupo a partir dos dados da requisição
        permissions = request.data.get('permissions') # Obtém as permissões do grupo a partir dos dados da requisição

        if not name:
            raise RequiredFields # Levanta uma exceção se o nome não for fornecido 
        
        create_group = Group.objects.create(
            name=name,
            enterprise_id=enterprise_id
        ) # Cria um novo grupo com o nome e ID da empresa fornecidos

        if permissions:
            permissions = permissions.split(',') # Divide a string de permissões em uma lista, assumindo que estão separadas por vírgulas
            # recebe "1, 2, 3" e transforma em [1, 2, 3] (uma lista iterável)

            try:
                for item in permissions:
                    # verifica se a permissão existe realmente no banco de dados
                    permission =  Permission.objects.filter(id=int(item)).exists()

                    if not permission:
                        create_group.delete()  # Deleta o grupo criado anteriormente em caso de erro
                        raise APIException(f'Permissão {item} não existe.') # Levanta uma exceção se a permissão não existir

                    # verifica se a permissão já está associada ao grupo
                    if not Group_Permissions.objects.filter(group_id=create_group.id, permission_id=int(item)).exists():
                        Group_Permissions.objects.create(
                            group_id=create_group.id,
                            permission_id=int(item)
                        ) # Cria uma associação entre o grupo recém-criado e cada permissão fornecida

                    Group_Permissions.objects.create(
                        group_id=create_group.id,
                        permission_id=int(item)
                    ) # Cria uma associação entre o grupo recém-criado e cada permissão fornecida

            except ValueError:
                create_group.delete()  # Deleta o grupo criado anteriormente em caso de erro
                raise APIException('Envie as permissões no padrão correto') # Levanta uma exceção se houver um erro de conversão de tipo
            
        return Response({"success": True}, status=201) # Retorna uma resposta de sucesso com status HTTP 201 (Criado)
    
class GroupDetail(Base):
    """View para gerenciar detalhes de um grupo específico dentro de uma empresa."""
    
    permission_classes = [GroupsPermission]

    def get(self, request, group_id):
        """Obtém os detalhes de um grupo específico pelo ID."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário

        self.get_group(group_id, enterprise_id) # Verifica se o grupo existe na empresa

        group = Group.objects.filter(id=group_id).first() # Obtém o grupo específico pelo ID e empresa

        serializer = GroupsSerializer(group) # Serializa os dados do grupo

        return Response({"group": serializer.data}) # Retorna a resposta com os dados serializados do grupo
    
    def put(self, request, group_id):
        """Atualiza os detalhes de um grupo específico pelo ID."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário

        self.get_group(group_id, enterprise_id) # Verifica se o grupo existe na empresa

        name = request.data.get('name') # Obtém o novo nome do grupo a partir dos dados da requisição
        permissions = request.data.get('permissions') # Obtém as novas permissões do grupo a

        if name:
            Group.objects.filter(id=group_id).update(
                name=name
            ) # Atualiza o nome do grupo se fornecido

        Group_Permissions.objects.filter(group_id=group_id).delete() # Remove todas as permissões associadas ao grupo antes de adicionar as novas

        if permissions:
            permissions = permissions.split(',') # Divide a string de permissões em uma lista, assumindo que estão separadas por vírgulas
            # recebe "1, 2, 3" e transforma em [1, 2, 3] (uma lista iterável)

            try:
                for item in permissions:
                    # verifica se a permissão existe realmente no banco de dados
                    permission =  Permission.objects.filter(id=int(item)).exists()

                    if not permission:
                        raise APIException(f'Permissão {item} não existe.') # Levanta uma exceção se a permissão não existir

                    # verifica se a permissão já está associada ao grupo
                    if not Group_Permissions.objects.filter(group_id=group_id, permission_id=int(item)).exists():
                        Group_Permissions.objects.create(
                            group_id=group_id,
                            permission_id=int(item)
                        ) # Cria uma associação entre o grupo recém-criado e cada permissão fornecida

                    Group_Permissions.objects.create(
                        group_id=group_id,
                        permission_id=int(item)
                    ) # Cria uma associação entre o grupo recém-criado e cada permissão fornecida

            except ValueError:
                raise APIException('Envie as permissões no padrão correto') # Levanta uma exceção se houver um erro de conversão de tipo
            
    def delete(self, request, group_id):
        """Deleta um grupo específico pelo ID."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário

        Group.objects.filter(id=group_id, enterprise_id=enterprise_id).delete() # Deleta o grupo específico pelo ID e empresa

        return Response({"success": True}) # Retorna uma resposta de sucesso
    
