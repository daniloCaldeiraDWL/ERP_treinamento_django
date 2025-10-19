from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups, GroupDetail
from companies.views.tasks import Tasks, TaskDetail

urlpatterns = [
    # employees endpoints
    path('employees', Employees.as_view()), # rota para listar e criar funcionários
    path('employees/<int:employee_id>', EmployeeDetail.as_view()), # rota para detalhes do funcionário específico, passando o id do funcionário

    # Groups And Permissions Endpoints
    path('groups', Groups.as_view()), # rota para listar e criar grupos de uma empresa
    path('groups/<int:group_id>', GroupDetail.as_view()), # rota para detalhes do grupo específico, passando o id do grupo, podendo atualizar ou deletar o grupo
    path('permissions', PermissionDetail.as_view()), # rota para detalhes das permissões dos grupos, podendo listar todas as permissões, criar novas permissões

    # tasks endpoints
    path('tasks', Tasks.as_view()), # rota para listar e criar tarefas de uma empresa
    path('tasks/<int:task_id>', TaskDetail.as_view()), # rota para detalhes da tarefa específica, passando o id da tarefa, podendo atualizar ou deletar a tarefa
]