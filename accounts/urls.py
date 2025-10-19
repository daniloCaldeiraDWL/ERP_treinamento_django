from accounts.views.signin import Signin
from accounts.views.signup import Signup
from accounts.views.user import GetUser

from django.urls import path

urlpatterns = [
    path('signin', Signin.as_view()), # rota para login de usuários
    path('signup', Signup.as_view()), # rota para cadastro de usuários
    path('user', GetUser.as_view()), # rota para obter informações do usuário autenticado
]