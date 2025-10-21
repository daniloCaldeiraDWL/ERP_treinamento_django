from rest_framework.exceptions import APIException

class NotFoundEmployee(APIException):
    """Exceção para funcionário não encontrado."""

    status_code = 404
    default_detail = 'Funcionário não encontrado.'
    default_code = 'not_found_employee'

class NotFoundGroup (APIException):
    """Exceção para grupo não encontrado."""
    status_code = 404
    default_detail = 'Grupo não encontrado.'
    default_code = 'not_found_group'

class RequiredFields(APIException):
    """Exceção para campos obrigatórios não preenchidos."""
    status_code = 400
    default_detail = 'Envie os campos no padrão correto.'
    default_code = 'error_required_field'

class NotFoundTaskStatus(APIException):
    """Exceção para status de tarefa não encontrado. 
    Avisa ao cliente que consome a API que o status de tarefa requisitado não existe."""
    status_code = 404
    default_detail = 'Status de tarefa não foi encontrado.'
    default_code = 'not_found_task_status'

class NotFoundTask(APIException):
    """Exceção para tarefa não encontrada. 
    Avisa ao cliente que consome a API que a tarefa requisitada não existe."""
    status_code = 404
    default_detail = 'Tarefa não foi encontrada.'
    default_code = 'not_found_task'