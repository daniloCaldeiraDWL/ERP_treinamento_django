from rest_framework import permissions
from accounts.models import User_Groups, Group_Permissions
from django.contrib.auth.models import Permission

def check_permission(user, method, permissions_to) -> bool:
    """Verifica se o usuário possui a permissão especificada.
    
    Args:
        user: Usuário autenticado.
        method: Método HTTP da requisição (GET, POST, PUT, DELETE). Pode ser 'add', 'change', 'delete', 'view'.
        permissions_to: Permissão necessária para o método. Pode ser 'task', 'employee', etc.
        
    Returns:
        bool: True se o usuário possui a permissão, False caso contrário."""
    
    # verificar se o usuário está autenticado
    if not user.is_authenticated:
        return False
    
    # se ele for o dono da empresa, ele tem acesso a todas as permissões
    if user.is_owner:
        return True
    
    required_permission = 'view_' + permissions_to

    # se o método for POST, a permissão necessária é 'add_<permissions_to>'
    # POST = criar
    # PUT = atualizar
    # DELETE = deletar
    if method == 'POST':
        required_permission = 'add_' + permissions_to
    elif method in ['PUT', 'PATCH']:
        required_permission = 'change_' + permissions_to
    elif method == 'DELETE':
        required_permission = 'delete_' + permissions_to

    groups = User_Groups.objects.values('group_id').filter(user_id=user.id).all() # Pega todos os grupos que o usuário pertence

    for group in groups:
        permissions = Group_Permissions.objects.values('permission_id').filter(group_id=group['group_id']).all() # Pega todas as permissões do usuário do grupo
        for permission in permissions:
            if Permission.objects.filter(id=permission['permission_id'], codename=required_permission).exists(): # Verifica se a permissão necessária está entre as permissões do grupo
                return True # Retorna True se a permissão for encontrada
                # Se a permissão não for encontrada em nenhum grupo, retorna False por padrão


class EmployeesPermission(permissions.BasePermission):
    """Classe personalizada para verificar se o usuário tem permissão para acessar funcionários."""

    message = 'Usuário não tem permissão para gerenciar os funcionários.'

    def has_permission(self, request, _view) -> bool | None:
        return check_permission(request.user, request.method, permissions_to='employee')
    
class GroupsPermission(permissions.BasePermission):
    """Classe personalizada para verificar se o usuário tem permissão para acessar grupos."""

    message = 'Usuário não tem permissão para gerenciar os grupos.'

    def has_permission(self, request, _view) -> bool | None:
        return check_permission(request.user, request.method, permissions_to='group')
    
class GroupsPermissionsPermission(permissions.BasePermission):
    """Classe personalizada para verificar se o usuário tem permissão para gerenciar as permissões dos grupos."""

    message = 'Usuário não tem permissão para gerenciar os grupos de permissões.'

    def has_permission(self, request, _view) -> bool | None:
        return check_permission(request.user, request.method, permissions_to='permission')
    
class TaskPermission(permissions.BasePermission):
    """Classe personalizada para verificar se o usuário tem permissão para acessar tarefas."""

    message = 'O funcionário não tem permissão para gerenciar as tarefas de todos os funcionários'

    def has_permission(self, request, _view) -> bool | None:
        return check_permission(request.user, request.method, permissions_to='task')