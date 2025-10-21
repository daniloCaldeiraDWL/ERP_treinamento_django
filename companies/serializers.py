"""Serializers do app companies.

Definição de serializers: conversão de dados complexos (como querysets e instâncias de modelos) em tipos de dados nativos do Python que podem ser facilmente renderizados em JSON, XML ou outros formatos de conteúdo.

"""
from rest_framework import serializers

from companies.models import Employee, Task
from accounts.models import User, User_Groups, Group, Group_Permissions

from django.contrib.auth.models import Permission

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Employee. Inclui campos personalizados para nome e email do usuário associado."""

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email']

    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self, obj):
        return obj.user.email
    
class EmployeesSerializer (serializers.ModelSerializer):
    """Serializer para o modelo Employee. Inclui campos personalizados para nome e email do usuário associado."""

    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'groups']

    def get_name(self, obj):
        return obj.user.name
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_groups(self, obj):
        groupsDB = User_Groups.objects.filter(user_id=obj.user.id).all()
        groupsDATA =  []


        for group in groupsDB:
            groupsDATA.append({
                "id": group.group_id,
                "name": group.group.name,
            })

        return groupsDATA
    
class GroupsSerializer (serializers.ModelSerializer):
    """Serializer para o modelo Group. Inclui campos personalizados para permissões associadas ao grupo."""

    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def get_permissions(self, obj):
        groups = Group_Permissions.objects.filter(group_id=obj.id).all()
        permissions =  []

        for group in groups:
            permissions.append({
                "id": group.permission.id,
                "name": group.permission.name,
                "codename": group.permission.codename,
            })

        return permissions
    
class PermissionSerializer (serializers.ModelSerializer):
    """Serializer para o modelo Permission."""

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class TasksSerializer (serializers.ModelSerializer):
    """Serializer para o modelo Task com várias tarefas."""
    status = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'status']

    def get_status(self, obj):
        return obj.status.name
    
class TaskSerializer (serializers.ModelSerializer):
    """Serializer para o modelo Task."""
    status = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'created_at', 'status', 'enterprise', 'employee']

    def get_status(self, obj):
        return obj.status.name
    
    def get_employee(self, obj):
        return EmployeeSerializer(obj.employee).data # reutilizado o serializer de Employee para retornar os dados do funcionário
    
    # método de uptdade para atualizar o status da tarefa
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.status = validated_data.get('status', instance.status)

        instance.save()
        
        return instance