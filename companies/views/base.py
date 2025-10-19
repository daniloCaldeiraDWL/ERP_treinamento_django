from rest_framework.views import APIView

from companies.utils.exceptions import NotFoundEmployee, NotFoundGroup, NotFoundTask, NotFoundTaskStatus
from companies.models import Employee, Enterprise, Task, TaskStatus

from accounts.models import Group

class Base(APIView):
    """Classe base para as views do app companies, fornecendo métodos utilitários comuns."""

    def get_enterprise_id(self, user_id):
        """Obtém o ID da empresa associada a um usuário."""

        employee = Employee.objects.filter(user_id=user_id).first() # Obtém o funcionário associado ao usuário
        owner = Enterprise.objects.filter(user_id=user_id).first() # Obtém o dono da empresa associado ao usuário

        if employee: # se for funcionário
            return employee.enterprise_id # Retorna o ID da empresa do funcionário

        return owner.id # Retorna o ID da empresa do dono
        
    def get_employee(self, employee_id, user_id):
        """Obtém um funcionário pelo ID."""

        enterprise_id = self.get_enterprise_id(user_id) # Obtém o ID da empresa do usuário autenticado

        employee = Employee.objects.filter(id=employee_id, enterprise_id=enterprise_id).first() # Obtém o funcionário pelo ID e empresa

        if not employee: # Se não encontrar o funcionário
            raise NotFoundEmployee() # Lança exceção de funcionário não encontrado
        
        return employee # Retorna o funcionário encontrado
    
    def get_group(self, group_id, enterprise_id):
        """Obtém um grupo pelo ID."""

        group = Group.objects.values('name').filter(id=group_id, enterprise_id=enterprise_id).first() # Obtém o grupo pelo ID e empresa

        if not group: # Se não encontrar o grupo
            raise NotFoundGroup() # Lança exceção de grupo não encontrado

        return group # Retorna o grupo encontrado
    
    def get_status(self, status_id):
        """Obtém o status da tarefa pelo ID."""

        status = TaskStatus.objects.filter(id=status_id).first() # Obtém o status da tarefa pelo ID

        if not status: # Se não encontrar o status
            raise NotFoundTaskStatus() # Lança exceção de status não encontrado

        return status # Retorna o status encontrado
    
    def get_task(self, task_id, enterprise_id):
        """Obtém a tarefa pelo ID.""" 

        task = Task.objects.filter(id=task_id, enterprise_id=enterprise_id).first() # Obtém a tarefa pelo ID e empresa

        if not task: # Se não encontrar a tarefa
            raise NotFoundTask() # Lança exceção de tarefa não encontrada
 
        return task # Retorna a tarefa encontrada