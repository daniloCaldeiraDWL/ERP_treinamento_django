from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from accounts.models import User_Groups, Group_Permissions

from companies.models import Enterprise, Employee

class Base(APIView):
    """Classe base para as views de empresas."""

    def get_enterprise_user(self, user_id):
        """Obtém informações da empresa e permissões do usuário."""

        enterprise = {
            "is_owner": False,
            "permissions": []
        } # inicializa o dicionário de empresa

        enterprise['is_owner'] = Enterprise.objects.filter(user_id=user_id).exists() # Verifica se o usuário é dono da empresa

        if enterprise['is_owner']: 
            return enterprise # Retorna se for dono da empresa
        
        # se não for dono, obtém as permissões como funcionário

        # Permissions, Get Employee
        employee = Employee.objects.filter(user_id=user_id).first() # Obtém o funcionário associado ao usuário

        if not employee: 
                raise APIException("Este usuário não é um funcionário") # Lança exceção se o usuário não for funcionário

        groups = User_Groups.objects.filter(user_id=user_id).all() # Obtém os grupos do usuário

        for g in groups:
            group = g.group # Obtém o grupo associado

            permissions = Group_Permissions.objects.filter(group_id=group.id).all() # Obtém as permissões do grupo

            for p in permissions:
                enterprise['permissions'].append({
                    "id": p.permission.id,
                    "label": p.permission.name,
                    "codename": p.permission.codename
                }) # Adiciona as permissões ao dicionário de empresa

        return enterprise  # Retorna o dicionário de empresa