from rest_framework.views import APIView

from companies.utils.exceptions import NotFoundEmployee, NotFoundGroup, NotFoundTask, NotFoundTaskStatus
from companies.models import Employee, Enterprise, Task, TaskStatus

from accounts.models import Group

class Base(APIView):
    """Classe base para as views do app companies, fornecendo métodos utilitários comuns."""

    def get_enterprise_id(self, user_id):
        """Obtém o ID da empresa associada a um usuário."""

        employee = Employee.objects.filter(user_id=user_id).first()
        owner = Enterprise.objects.filter(user_id=user_id).first()

        if employee:
            return employee.enterprise_id

        return owner.id
        
    def get_employee(self, employee_id, user_id):
        """Obtém um funcionário pelo ID."""

        enterprese_id = self.get_enterprise_id(user_id)

        employee = Employee.objects.filter(id=employee_id, enterprise_id=enterprese_id).first()

        if not employee:
            raise NotFoundEmployee()
        
        return employee
    
    def get_group(self, group_id, enterprise_id):
        """Obtém um grupo pelo ID."""

        group = Group.objects.values('name').filter(id=group_id, enterprise_id=enterprise_id).first()

        if not group:
            raise NotFoundGroup()

        return group
    
    def get_status(self, status_id):
        """Obtém o status da tarefa pelo ID."""

        status = TaskStatus.objects.filter(id=status_id).first()

        if not status:
            raise NotFoundTaskStatus()

        return status
    
    def get_task(self, task_id, enterprise_id):
        """Obtém a tarefa pelo ID."""

        task = Task.objects.filter(id=task_id, enterprise_id=enterprise_id).first()

        if not task:
            raise NotFoundTask()

        return task