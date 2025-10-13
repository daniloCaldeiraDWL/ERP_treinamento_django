from rest_framework import serializers
from accounts.models import User  # Importe o modelo User personalizado

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']