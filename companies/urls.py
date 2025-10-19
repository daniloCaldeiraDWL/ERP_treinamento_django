from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups, GroupDetail

urlpatterns = [
    # employees endpoints
    path('employees', Employees.as_view()), # rota para listar e criar funcionários
    path('employees/<int:employee_id>', EmployeeDetail.as_view()), # rota para detalhes do funcionário específico, passando o id do funcionário

    # Groups And Permissions Endpoints
    path('groups', Groups.as_view()), # rota para listar e criar grupos
    path('groups/<int:group_id>', GroupDetail.as_view()), # rota para detalhes do grupo específico, passando o id do grupo
    path('permissions', PermissionDetail.as_view()), # rota para detalhes das permissões dos grupos
]