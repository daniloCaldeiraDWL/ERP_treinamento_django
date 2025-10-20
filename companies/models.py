"""Models do app companies."""

from django.db import models

# tradução Enterprise = Empresa
# tradução Employee = Funcionário

class Enterprise(models.Model):
    name = models.CharField(max_length=175)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
class Employee(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)

class TaskStatus(models.Model):
    name = models.CharField(max_length=155)
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'campanies_task_status'

class Task(models.Model):
    title = models.TextField(max_length=175)
    description = models.TextField(null=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True) # seta automaticamente a data de criação da tarefa
    updated_at = models.DateTimeField(null=True) # seta automaticamente a data de atualização da tarefa, podendo ser nula (ao criar a tarefa)
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE) # relacionamento com o status da tarefa
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE) # relacionamento com a empresa
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE) # relacionamento com o funcionário