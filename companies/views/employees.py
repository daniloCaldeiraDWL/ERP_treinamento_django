from companies.views.base import Base
from companies.utils.permissions import EmployeePermission, GroupPermission
from companies.models import Employee, Enterprise
from serializers import EmployeeSerializer, EmployeesSerializer

from accounts.auth import Authentication
from accounts.models import User, User_Groups

from rest_framework.views import Response, status
from rest_framework.exceptions import APIException

class Employees(Base):
    """View para gerenciar funcionários da empresa."""

    permission_classes = [EmployeePermission]

    def get(self, request):
        """Obtém a lista de funcionários da empresa, exceto o dono.

        Args:
            request: Requisição HTTP feita pelo cliente.

        Returns:
            Response: Resposta HTTP com a lista de funcionários serializados.
        """

        enterprise_id = self.get_enterprise_id(request.user.id)

        # obter o dono da empresa
        owner = Enterprise.objects.values('user_id').filter(id=enterprise_id).first(['user_id'])

        # obter todos os funcionários da empresa, exceto o dono
        employee = Employee.objects.filter(enterprise_id=enterprise_id).exclude(user_id=owner['user_id']).all()

        serializer = EmployeesSerializer(employee, many=True) # serializar múltiplos objetos, por isso many=True

        return Response("employees", serializer.data) # retornar a lista de funcionários serialized
        # Response significa que a requisição foi bem sucedida e retorna os dados solicitados

    def post(self, request):
        """Cria um novo funcionário na empresa.
        Args:
            request: Requisição HTTP contendo os dados do novo funcionário.
        Returns:
            Response: Resposta HTTP com os dados do funcionário criado ou mensagem de erro.
        """

        nome = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        enterprise_id = self.get_enterprise_id(request.user.id) # obtém o ID da empresa do usuário autenticado
        signup_user = Authentication.signup(self, nome=nome, email=email, password=password, type_account='employee', enterprise_id=enterprise_id) # cria um novo usuário

        # verifica se o usuário foi criado com sucesso
        if isinstance(signup_user, User):
            return Response({"success": True}, status=status.HTTP_201_CREATED) # retorna mensagem de sucesso se o usuário foi criado
        
        return Response(signup_user, status=status.HTTP_400_BAD_REQUEST) # retorna mensagem de erro se o usuário não foi criado
    
class EmployeeDetail(Base):
    """View para gerenciar detalhes de um funcionário específico."""

    permission_classes = [EmployeePermission]

    def get(self, request, employee_id):
        """Obtém os detalhes de um funcionário específico.

        Args:
            request: Requisição HTTP feita pelo cliente.
            employee_id: ID do funcionário a ser obtido.

        Returns:
            Response: Resposta HTTP com os detalhes do funcionário serializados.
        """

        employee = self.get_employee(employee_id, request.user.id)

        serializer = EmployeeSerializer(employee)

        return Response(serializer.data)
    
    def put(self, request, employee_id):
        """Atualiza os detalhes de um funcionário específico.

        Args:
            request: Requisição HTTP contendo os dados atualizados do funcionário.
            employee_id: ID do funcionário a ser atualizado.

        Returns:
            Response: Resposta HTTP com os dados atualizados do funcionário ou mensagem de erro.
        """

        groups = request.data.get('groups')  # obtém a lista de grupos do corpo da requisição

        employee = self.get_employee(employee_id, request.user.id) # obtém o funcionário a ser atualizado

        name = request.data.get('name') or employee.user.name # se não for fornecido um novo nome, mantém o nome atual
        email = request.data.get('email') or employee.user.email # se não for fornecido um novo email, mantém o email atual

        if email != employee.user.email and User.objects.filter(email=email).exists():
            # verifica se o novo email já está em uso por outro usuário
            raise APIException("Email já está em uso por outro usuário.", code="email_already_use")
        
        User.objects.filter(id=employee.user.id).update(
            name=name, 
            email=email
        ) # atualiza os dados do usuário associado ao funcionário
        
        User_Groups.objects.filter(user_id=employee.user.id).delete() # remove todos os grupos atuais do usuário
        # busca eliminar os grupos para não acumular grupos antigos com os novos

        if groups: # se houver grupos fornecidos na requisição
            groups = groups.split(',')  # divide a string em uma lista de IDs de grupos, cria uma lista separada por vírgulas
            # veio: "1,2,3" -> virou: ["1", "2", "3"]

            for group_id in groups:
                self.get_group(group_id, employee.enterprise.id)  # verifica se o grupo existe na empresa
                User_Groups.objects.create(
                    group_id=group_id,
                    user_id=employee.user.id
                )  # adiciona o usuário ao novo grupo

        return Response({"success": True})  # retorna mensagem de sucesso
    
    def delete(self, request, employee_id):
        """Remove um funcionário específico da empresa.

        Args:
            request: Requisição HTTP feita pelo cliente.
            employee_id: ID do funcionário a ser removido.

        Returns:
            Response: Resposta HTTP indicando o sucesso da remoção.
        """

        employee = self.get_employee(employee_id, request.user.id) # obtém o funcionário a ser removido
        # o método get_employee já verifica se o funcionário pertence à empresa do usuário autenticado
        # se não pertencer, uma exceção NotFoundEmployee será levantada, já finalizando a execução do método
 
        check_if_owner = User.objects.filter(id=employee.user.id, is_owner=1).exists() # verifica se o funcionário é o dono da empresa

        if check_if_owner:
            # se o funcionário for o dono da empresa, não é possível removê-lo
            raise APIException("Não é possível remover o dono da empresa.", code="cannot_delete_owner")
        
        employee.user.delete()  # remove o usuário associado ao funcionário, o que também remove o funcionário devido à relação de chave estrangeira
        User.objects.filter(id=employee.user.id).delete()  # remove o usuário associado ao funcionário

        return Response({"success": True})  # retorna mensagem de sucesso