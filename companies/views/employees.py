from .base import Base
from companies.utils.permissions import EmployeesPermission, GroupsPermission
from companies.models import Employee, Enterprise
from companies.serializers import EmployeeSerializer, EmployeesSerializer

from accounts.auth import Authentication
from accounts.models import User, User_Groups

from rest_framework.views import Response, status
from rest_framework.exceptions import APIException


class Employees(Base):
    """View para gerenciar funcionários dentro da empresa do usuário autenticado."""

    permission_classes = [EmployeesPermission]

    def get(self, request):
        """Obtém todos os funcionários associados à empresa do usuário autenticado, exceto o dono da empresa.
        Args:
            request: Objeto de requisição HTTP."""

        enterprise_id = self.get_enterprise_id(request.user.id) 

        owner_id = Enterprise.objects.values('user_id').filter(id=enterprise_id).first()['user_id'] # Obtém o ID do dono da empresa

        employees = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner_id).all() # Obtém todos os funcionários, exceto o dono

        serializer = EmployeesSerializer(employees, many=True) # Serializa os dados dos funcionários

        return Response({"employees": serializer.data}) # Retorna a resposta com os dados dos funcionários
    
    def post(self, request):
        """Cria um novo funcionário dentro da empresa do usuário autenticado.
        Args:
            request: Objeto de requisição HTTP."""

        name = request.data.get('name') # Obtém o nome do corpo da requisição
        email = request.data.get('email') # Obtém o email do corpo da requisição
        password = request.data.get('password') # Obtém a senha do corpo da requisição

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa do usuário autenticado

        signup_user = Authentication.signup(
            self,
            name=name,
            email=email,
            password=password,
            type_account='employee',
            company_id=enterprise_id
        )   # Realiza o cadastro do funcionário

        if isinstance(signup_user, User): # Se o cadastro for bem-sucedido
            return Response({"success": True}, status=status.HTTP_201_CREATED) # Retorna a resposta de sucesso
        
        return Response(signup_user, status=status.HTTP_400_BAD_REQUEST) # Senão, Retorna a resposta de erro


class EmployeeDetail(Base):
    """View para gerenciar um funcionário específico dentro da empresa do usuário autenticado."""

    permission_classes = [EmployeesPermission] # Permissões para gerenciar funcionários

    def get(self, request, employee_id): 
        """Obtém os detalhes de um funcionário específico dentro da empresa do usuário autenticado."""

        employee = self.get_employee(employee_id, request.user.id)  # Obtém o funcionário pelo ID e empresa

        serializer = EmployeeSerializer(employee) # Serializa os dados do funcionário

        return Response(serializer.data) # Retorna a resposta com os dados do funcionário
    
    def put(self, request, employee_id):
        """Atualiza os dados de um funcionário específico dentro da empresa do usuário autenticado.
        Args:
            request: Objeto de requisição HTTP.
            employee_id: ID do funcionário a ser atualizado.
        """

        groups = request.data.get('groups') # Obtém os grupos do corpo da requisição

        employee = self.get_employee(employee_id, request.user.id) # Obtém o funcionário pelo ID e empresa

        name = request.data.get('name') or employee.user.name # Obtém o nome do corpo da requisição ou mantém o atual
        email = request.data.get('email') or employee.user.email # Obtém o email do corpo da requisição ou mantém o atual

        if email != employee.user.email and User.objects.filter(email=email).exists(): # Se o email for alterado e já existir
            raise APIException("Esse email já está em uso", code="email_already_use") # Levanta uma exceção se o email já estiver em uso
        
        User.objects.filter(id=employee.user.id).update(
            name=name,
            email=email
        ) # Atualiza os dados do usuário associado ao funcionário

        User_Groups.objects.filter(user_id=employee.user.id).delete() # Remove os grupos atuais do funcionário

        if groups:
            # 1,2,3,4 -> [1, 2, 3, 4]
            groups = groups.split(',') # Divide a string de grupos em uma lista, assumindo que estão separadas por vírgulas

            for group_id in groups:
                self.get_group(group_id, employee.enterprise.id)
                User_Groups.objects.create(
                    group_id=group_id,
                    user_id=employee.user.id
                ) # Adiciona os novos grupos ao funcionário

        return Response({"success": True}) # Retorna a resposta de sucesso

    def delete(self, request, employee_id):
        """Remove um funcionário específico da empresa do usuário autenticado.
        Args:
            request: Objeto de requisição HTTP.
            employee_id: ID do funcionário a ser removido.
        """

        employee = self.get_employee(employee_id, request.user.id) # Obtém o funcionário pelo ID e empresa

        check_if_owner = User.objects.filter(id=employee.user.id, is_owner=1).exists() # Verifica se o funcionário é o dono da empresa

        if check_if_owner: # Se for o dono da empresa
            raise APIException('Você não pode demitir o dono da empresa') # Levanta uma exceção se tentar remover o dono da empresa
        
        employee.delete() # Remove o funcionário
        
        User.objects.filter(id=employee.user.id).delete() # Remove o usuário associado ao funcionário

        return Response({"success": True}) # Retorna a resposta de sucesso