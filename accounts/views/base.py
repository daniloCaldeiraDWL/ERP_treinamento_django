from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from accounts.models import UserGroup, GroupPermission
from companies.models import Enterprise, Employee

class Base(APIView):

    # método para obter uma empresa baseado em um usuário
    def get_enterprise_user(self, user_id):
        enterprise = {
            "is_owner": False,
            "permissions": []
        }

        enterprise['is_owner'] = Enterprise.objects.filter(user_id=user_id).exists()

        if enterprise['is_owner']: return enterprise

        employee = Enterprise.objects.filter(employee__user_id=user_id).first()

        if not employee: raise APIException("Este usuário não é um funcionário!")

        groups = UserGroup.objects.filter(user_id=user_id).all()

        for g in groups:
            group = g.group
            permissions = GroupPermission.objects.filter(group_id=group.id).all()

            for p in permissions:
                enterprise['permissions'].append({
                    "id": p.permission.id,
                    "name": p.permission.name,
                    "codename": p.permission.codename
                })

        return enterprise

