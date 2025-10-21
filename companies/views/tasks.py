from companies.views.base import Base
from companies.utils.permissions import TaskPermission
from companies.serializers import TaskSerializer, TasksSerializer
from companies.models import Task

from rest_framework.response import Response
from rest_framework.exceptions import APIException

import datetime

class Tasks(Base):
    """View para gerenciar tarefas dentro da empresa do usuário autenticado."""

    permission_classes = [TaskPermission]

    def get(self, request):
        """Obtém todas as tarefas associadas à empresa do usuário autenticado.
        Args:
            request: Objeto de requisição HTTP."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário autenticado

        tasks = Task.objects.filter(enterprise_id=enterprise_id).all() # Filtra as tarefas pela empresa

        serializer = TasksSerializer(tasks, many=True) # Serializa a lista de tarefas da empresa

        return Response({"tasks": serializer.data}) # Retorna a resposta com as tarefas serializadas
    
    def post(self, request):
        """Cria uma nova tarefa dentro da empresa do usuário autenticado.
        Args:
            request: Objeto de requisição HTTP."""

        employee_id = request.data.get('employee_id') # Obtém o ID do funcionário associado ao usuário autenticado
        title = request.data.get('title') # Obtém o título da tarefa a partir dos dados da requisição
        description = request.data.get('description') # Obtém a descrição da tarefa a partir dos dados da requisição
        status_id = request.data.get('status_id') # Obtém o ID do status da tarefa a partir dos dados da requisição
        due_date = request.data.get('due_date') # Obtém a data de vencimento da tarefa a partir dos dados da requisição

        employee = self.get_employee(employee_id, request.user.id) # Obtém o funcionário associado ao usuário autenticado       
        _status = self.get_status(status_id) # Obtém o status da tarefa pelo ID

        # Validadores
        if not title or len(title) > 175:
            raise APIException('O título é obrigatório e deve ter no máximo 175 caracteres.') # Levanta uma exceção se o título não for fornecido ou exceder o limite de caracteres

        if due_date:
            try:
                due_date = datetime.datetime.strptime(
                    due_date, "%d/%m/%Y %H:%M") # Converte a string da data de vencimento para um objeto date
            except ValueError:
                raise APIException('Data de vencimento inválida. Use o formato DD/MM/AAAA HH:MM.', 'date_invalid') # Levanta uma exceção se a data de vencimento estiver em um formato inválido

        task = Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            employee_id=employee_id,
            enterprise_id=employee.enterprise.id,
            status_id=status_id
        ) # Cria uma nova tarefa com os dados fornecidos

        serializer = TaskSerializer(task) # Serializa os dados da tarefa criada

        return Response({"task": serializer.data}) # Retorna a resposta com os dados da tarefa criada
    
class TaskDetail(Base):
    """View para gerenciar detalhes de uma tarefa específica."""

    permission_classes = [TaskPermission]

    def get(self, request, task_id):
        """Obtém os detalhes de uma tarefa específica pelo ID.
        Args:
            request: Objeto de requisição HTTP.
            task_id: ID da tarefa a ser obtida."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário autenticado

        task = self.get_task(task_id, enterprise_id) # Obtém a tarefa pelo ID e empresa

        serializer = TaskSerializer(task) # Serializa os dados da tarefa

        return Response(serializer.data) # Retorna a resposta com os dados serializados da tarefa
    
    def put(self, request, task_id):
        """Atualiza parcialmente os detalhes de uma tarefa específica pelo ID.
        Args:
            request: Objeto de requisição HTTP.
            task_id: ID da tarefa a ser atualizada."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário autenticado
        task = self.get_task(task_id, enterprise_id) # Obtém a tarefa pelo ID e empresa

        title = request.data.get('title', task.title) # Obtém o título da tarefa a partir dos dados da requisição ou mantém o título atual
        employee_id = request.data.get('employee_id', task.employee.id) # Obtém o ID do funcionário associado à tarefa a partir dos dados da requisição ou mantém o ID atual
        description = request.data.get('description', task.description) # Obtém a descrição da tarefa a partir dos dados da requisição ou mantém a descrição atual
        status_id = request.data.get('status_id', task.status.id) # Obtém o ID do status da tarefa a partir dos dados da requisição ou mantém o ID atual
        due_date = request.data.get('due_date', task.due_date) # Obtém a data de vencimento da tarefa a partir dos dados da requisição ou mantém a data atual

        # Validators
        self.get_status(status_id) # Verifica se o status existe
        self.get_employee(employee_id, request.user.id) # Verifica se o funcionário existe

        if due_date and due_date != task.due_date:
            try:
                due_date = datetime.datetime.strptime(
                    due_date, "%d/%m/%Y %H:%M")
            except ValueError:
                raise APIException(
                    "A data deve ter o padrão: d/m/Y H:M", "date_invalid")

        data = {
            "title": title,
            "description": description,
            "due_date": due_date
        } # Dados a serem atualizados na tarefa

        serializer = TaskSerializer(task, data=data, partial=True) # Serializa os dados da tarefa para atualização parcial

        if not serializer.is_valid():
            raise APIException("Não foi possível editar a tarefa")

        serializer.update(task, serializer.validated_data) # Atualiza os dados da tarefa com os dados validados

        task.status_id = status_id
        task.employee_id = employee_id # Atualiza o ID do funcionário associado à tarefa
        task.save() # Salva as alterações na tarefa

        return Response({"task": serializer.data}) # Retorna a resposta com os dados atualizados da tarefa
    
    def delete(self, request, task_id):
        """Deleta uma tarefa específica pelo ID.
        Args:
            request: Objeto de requisição HTTP.
            task_id: ID da tarefa a ser deletada."""

        enterprise_id = self.get_enterprise_id(request.user.id) # Obtém o ID da empresa associada ao usuário autenticado

        task = self.get_task(task_id, enterprise_id) # Obtém a tarefa pelo ID e empresa

        task.delete() # Deleta a tarefa

        return Response({"success": True}) # Retorna uma resposta de sucesso
